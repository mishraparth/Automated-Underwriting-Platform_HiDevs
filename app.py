import streamlit as st
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter # CHANGED
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA

# --- Load API Key from .env file ---
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")


# --- Main App Interface ---
st.set_page_config(page_title="Automated Underwriting AI", layout="wide")
st.title("🤖 Automated Underwriting Platform")
st.write("This app uses your GROQ_API_KEY from the .env file.")
st.write("Upload a property appraisal (PDF) and underwriting guidelines (TXT) to get an automated risk assessment.")


# File Uploaders
report_file = st.file_uploader("Upload Property Appraisal Report (PDF)", type="pdf")
guidelines_file = st.file_uploader("Upload Underwriting Guidelines (TXT)", type="txt")

# Analyze Button
if st.button("Analyze Property Risk"):
    # --- Input Validation ---
    if not groq_api_key:
        st.error("GROQ_API_KEY not found in .env file. Please make sure your .env file is set up correctly.")
    elif not report_file:
        st.warning("Please upload a property appraisal report.")
    elif not guidelines_file:
        st.warning("Please upload the underwriting guidelines.")
    else:
        try:
            with st.spinner("Processing documents and analyzing risk... this may take a moment."):
                # --- File Handling ---
                if not os.path.exists("temp"):
                    os.makedirs("temp")
                
                report_path = os.path.join("temp", report_file.name)
                with open(report_path, "wb") as f:
                    f.write(report_file.getbuffer())

                guidelines_path = os.path.join("temp", guidelines_file.name)
                with open(guidelines_path, "wb") as f:
                    f.write(guidelines_file.getbuffer())

                # --- 1. Load Documents ---
                report_loader = PyPDFLoader(report_path)
                guidelines_loader = TextLoader(guidelines_path)
                report_docs = report_loader.load()
                guidelines_docs = guidelines_loader.load()
                all_docs = report_docs + guidelines_docs

                # --- 2. Split Text into Chunks ---
                # CHANGED to use CharacterTextSplitter
                text_splitter = CharacterTextSplitter(
                    separator="\n",
                    chunk_size=1000,
                    chunk_overlap=200,
                    length_function=len
                )
                chunks = text_splitter.split_documents(all_docs)

                if not chunks:
                    st.error("Could not extract any text from the documents. Please check the files.")
                    st.stop()

                # --- 3. Create Embeddings and Vector Store ---
                embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
                vectorstore = FAISS.from_documents(documents=chunks, embedding=embeddings)

                # --- 4. Initialize AI Model and Retrieval Chain ---
                llm = ChatGroq(temperature=0, groq_api_key=groq_api_key, model_name="llama3-70b-8192")
                qa_chain = RetrievalQA.from_chain_type(
                    llm=llm,
                    chain_type="stuff",
                    retriever=vectorstore.as_retriever(),
                    return_source_documents=True
                )

                # --- 5. Run the Query and Get the Assessment ---
                query = """
                You are an expert insurance underwriter. Your task is to provide a risk assessment of the property based on the provided appraisal report and the official underwriting guidelines.
                
                Perform the following actions:
                1.  **Summary of Findings:** Briefly summarize the key conditions of the property (roof, foundation, electrical, etc.) as described in the report.
                2.  **Guideline Compliance Check:** For each finding, explicitly compare it against the provided underwriting guidelines. State whether it complies or violates a rule.
                3.  **Final Decision:** Based on your analysis, provide a clear, final decision: **APPROVE**, **REJECT**, or **REVIEW REQUIRED**.
                4.  **Justification:** Provide a concise justification for your final decision, referencing the specific findings and guidelines that led to it.
                
                Present the entire analysis in a clear, structured format using Markdown.
                """
                
                result = qa_chain.invoke({"query": query})

                # --- Display the Result ---
                st.subheader("Automated Underwriting Assessment")
                st.markdown(result["result"])

                with st.expander("Show sources used for the assessment"):
                    st.write(result["source_documents"])

        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.error("Please check that your API key is valid and has credits.")
        
        finally:
            if 'report_path' in locals() and os.path.exists(report_path):
                os.remove(report_path)
            if 'guidelines_path' in locals() and os.path.exists(guidelines_path):
                os.remove(guidelines_path)