import numpy as np
import pandas as pd
import fitz
from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
import pdfplumber
import textwrap
import streamlit as st


st.set_page_config(page_title="PDF Question Answering and Summarizer", layout= "wide")
st.title("PDF Question Answering and Summarizer")

uploaded_file = st.file_uploader("Upload your PDF File", type='pdf')


def load_models():
    embedder = SentenceTransformer("all-mpnet-base-v2")                                     # or ----> multi-qa-mpnet-base-dot-v1
    qa_model = pipeline("question-answering", model="google/flan-t5-base")                  # or ----> deepset/roberta-base-squad2
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")                 # or ----> sshleifer/distilbart-cnn-12-6
    return embedder, qa_model, summarizer


embedder, qa_pipeline, summarizer = load_models()


def extract_text_from_pdf(file):
    full_text = ""  
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"
    return full_text


def split_into_chunks(text, min_len = 30):
    chunks = [para.strip() for para in text.split("\n") if len(para.strip()) > min_len]
    return chunks

def chunk_text_for_summarizer(text, max_len = 500):
    return textwrap.wrap(text, width= max_len)




if uploaded_file:
    st.info("Extracting and Indexing texts")
    
    full_text = extract_text_from_pdf(uploaded_file)
    if not full_text.strip():
        st.error("No Text found in the uploaded PDF")
        st.stop()
        
    text_chunks = split_into_chunks(full_text)
    if len(text_chunks) == 0:
        st.error("Could not find valid chunks in PDF, Try a different file")
        st.stop()
    
    
    tabs = st.tabs(["Summarize PDF", "Ask Questions"])


# Summary Code

    with tabs[0]:
        st.subheader("PDF Summary")
        if st.button("Summarize PDF"):

            with st.spinner("Summarizing PDF"):
                summary_chunks = chunk_text_for_summarizer(full_text)
                summaries = []
                for chunk in summary_chunks:
                    result = summarizer(chunk, max_length = 150, min_length = 30, do_sample = False)
                    summaries.append(result[0]['summary_text'])

                final_summary = " ".join(summaries)

            st.success("Summary generated")
            st.write(final_summary)


# Q & A Code

    with tabs[1]:
        st.subheader("Ask a Question from PDF: ")
        with st.spinner("Indexing Content"):
            corpus_embeddings = embedder.encode(text_chunks, convert_to_tensor=True)

        question = st.text_input("Ask your Question from the PDF: ")

        if question:
            question_embedding = embedder.encode(question, convert_to_tensor=True)
            scores = util.cos_sim(question_embedding, corpus_embeddings)
            best_index = scores.argmax().item()
            best_context = text_chunks[best_index]

            answer = qa_pipeline(question = question, context = best_context)

            st.subheader("Answer: ")
            st.write(answer['answer'])

            with st.expander("Context Used"):
                st.write(best_context)
        









