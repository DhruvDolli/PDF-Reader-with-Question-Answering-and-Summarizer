# PDF Question Answering and Summarizer App

This project is an interactive Streamlit-based web application that allows users to:

- Upload a PDF file
- Ask questions based on the PDF content using a **QA model**
- Summarize the entire PDF using a **state-of-the-art summarization model**

Built using **HuggingFace Transformers**, **pdfplumber**, and **Streamlit**.

---

## Features

- **PDF Text Extraction** – Handles multi-page PDFs
- **Question Answering** – Uses `flan-t5-basefor` detailed, generative answers
- **Summarization** – Summarizes long documents in chunks
- Uses **state-of-the-art NLP models** (e.g. `all-mpnet-base-v2`, `bart-large-cnn`)
- Clean and interactive **Streamlit web app**


## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| [Streamlit](https://streamlit.io) | Web UI |
| [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/) | PDF parsing |
| [Transformers](https://huggingface.co/transformers/) | NLP models |
| [HuggingFace Pipelines](https://huggingface.co/docs/transformers/main_classes/pipelines) | Easy access to QA/Summarization |

---

## 📦 Installation

```bash
git clone https://github.com/yourusername/PDF-Reader-with-Question-Answering-and-Summarizer.git
pip install -r requirements.txt
run streamlit run app.py 
