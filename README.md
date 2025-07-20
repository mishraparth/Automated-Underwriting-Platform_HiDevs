# Automated Underwriting Platform

This project is automatically generated.

## Installation

```sh
pip install -r requirements.txt
```

# 🤖 Automated Underwriting Platform

This project is an AI-powered platform designed to automate the property risk assessment process for the insurance industry. It leverages a Retrieval-Augmented Generation (RAG) pipeline to analyze property appraisal reports against a set of underwriting guidelines, delivering an instant and justified risk assessment.

This project was built for the Level 3 Hi Devs Skillathon.

---

## ✨ Features

* **Automated Document Analysis:** Extracts and understands text from PDF appraisal reports.
* **AI-Powered Risk Assessment:** Uses a Large Language Model (LLM) to compare property conditions against underwriting rules.
* **Instant Decision Making:** Provides a clear, final decision (**APPROVE**, **REJECT**, or **REVIEW REQUIRED**) with a detailed justification.
* **Simple Web Interface:** Easy-to-use interface built with Streamlit for uploading documents and viewing results.

---

## 🛠️ Tech Stack

* **Backend:** Python
* **Web Framework:** Streamlit
* **AI/LLM:** LangChain, Llama 3 (via Groq API)
* **Vector Database:** FAISS
* **Embeddings:** Sentence-Transformers

---

## 🚀 Setup and Installation

To run this project locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/mishraparth/Automated-Underwriting-Platform_HiDevs.git
    cd Automated-Underwriting-Platform_HiDevs
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up environment variables:**
    * Create a file named `.env` in the root directory.
    * Add your Groq API key to the `.env` file:
        ```env
        GROQ_API_KEY="your-secret-api-key"
        ```

4.  **Run the application:**
    ```bash
    streamlit run app.py
    ```

---

## 📖 How to Use

1.  Launch the application.
2.  Upload a property appraisal report (as a PDF).
3.  Upload a text file containing the underwriting guidelines.
4.  Click the **"Analyze Property Risk"** button.
5.  Review the generated assessment in the main window.
