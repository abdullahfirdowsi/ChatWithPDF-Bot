

import streamlit as st
import fitz  # PyMuPDF
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from fpdf import FPDF
import tempfile
import os
from googletrans import Translator
import warnings

# Suppress specific warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# Function to extract text from the PDF
def extract_text_from_pdf(pdf_path):
    document = ""
    with fitz.open(pdf_path) as pdf:
        for page in pdf:
            document += page.get_text()
    return document

# Function to summarize the document using BART
@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text, summarizer):
    summary = summarizer(text, max_length=150, min_length=40, do_sample=False)
    return summary[0]['summary_text']

# Function to translate the document to a selected language
@st.cache_resource
def load_translator():
    return Translator()

def translate_text(text, target_language, translator):
    translated = translator.translate(text, dest=target_language)
    return translated.text

# Function to answer questions from the document using a QA model
@st.cache_resource
def load_qa_model():
    return pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

def answer_question(context, question, qa_model):
    answer = qa_model(question=question, context=context)
    return answer['answer']

# Function to generate MCQs from the document
# @st.cache_resource
# def load_mcq_generator():
#     model_name = "valhalla/t5-base-qa-qg-hl"
#     tokenizer = AutoTokenizer.from_pretrained(model_name,legacy=False)
#     model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
#     return tokenizer, model

# def generate_mcqs(text, tokenizer, model, num_questions=5):
#     num_beams = max(num_questions, 5)  # Ensure num_beams is at least as large as num_questions
#     input_text = f"generate questions: {text}"
#     inputs = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)
#     outputs = model.generate(inputs, max_length=512, num_beams=num_beams, early_stopping=True, num_return_sequences=num_questions)
    
#     questions = []
#     for output in outputs:
#         decoded_output = tokenizer.decode(output, skip_special_tokens=True,legacy=False)
#         questions.append(decoded_output)

#     return questions

# Function to create a PDF with summarized content
def create_summary_pdf(summary_text, output_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, summary_text)
    pdf.output(output_path)

# Function to create a text file with content
def create_text_file(content, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

def create_pdf(content, output_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, content)
    pdf.output(output_path)

# def create_mcq_pdf(mcqs, output_path):
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("Arial", size=12)
#     for i, mcq in enumerate(mcqs, 1):
#         pdf.multi_cell(0, 10, f"Q{i}: {mcq}\n")
#     pdf.output(output_path)

def get_download_link(file_path, text):
    with open(file_path, "r", encoding="utf-8") as f:
        data = f.read()
    href = f'<a href="data:text/plain;charset=utf-8,{data}" download="{file_path}">{text}</a>'
    return href

# Streamlit sidebar
st.sidebar.title("PDF Processing App")
option = st.sidebar.selectbox("Choose an option", ("Summarizer", "Translator", "Question Answering Bot"))

uploaded_file = st.file_uploader("Upload a PDF file less than 12 MB", type=["pdf"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_file_path = tmp_file.name

    document = extract_text_from_pdf(tmp_file_path)

    if option == "Summarizer":
        st.header("Summarized Content")
        summarizer = load_summarizer()
        summary = summarize_text(document, summarizer)
        st.write(summary)
        
        # Save summarized text as a new PDF
        output_pdf_path = "summary_output.pdf"
        create_summary_pdf(summary, output_pdf_path)
        
        # Provide a download link for the new PDF
        with open(output_pdf_path, "rb") as f:
            st.download_button("Download Summarized PDF", f, file_name=output_pdf_path, mime="application/pdf")
    
    elif option == "Translator":
        st.header("Translate Document")
        languages = {
            "English": "en", "Hindi": "hi", "French": "fr", "German": "de", "Spanish": "es",
            "Italian": "it", "Portuguese": "pt", "Russian": "ru", "Chinese": "zh", "Japanese": "ja",
            "Arabic": "ar", "Korean": "ko", "Turkish": "tr", "Dutch": "nl", "Swedish": "sv",
            "Polish": "pl", "Vietnamese": "vi", "Finnish": "fi", "Norwegian": "no", "Danish": "da",
            "Czech": "cs", "Greek": "el", "Thai": "th", "Romanian": "ro", "Hungarian": "hu",
            "Indonesian": "id", "Hebrew": "he"
        }

        target_language = st.selectbox("Select target language", list(languages.keys()))
        if st.button("Translate"):
            target_lang_code = languages[target_language]
            translator = load_translator()
            translated_text = translate_text(document, target_lang_code, translator)
            st.write(translated_text)

            # Save translated text as a new text file
            output_text_path = "translated_text.txt"
            create_text_file(translated_text, output_text_path)
            
            # Provide a download link for the translated text file
            with open(output_text_path, "rb") as f:
                st.download_button("Download Translated Text", f, file_name=output_text_path, mime="text/plain")
    
    elif option == "Question Answering Bot":
        st.header("Question Answering Bot")
        question = st.text_input("Ask a question about the document:")
        if question:
            qa_model = load_qa_model()
            answer = answer_question(document, question, qa_model)
            st.write(f"Answer: {answer}")
    
    # elif option == "MCQ Generator":
    #     st.header("MCQs Generated from the Document")
    #     tokenizer, model = load_mcq_generator()
    #     mcqs = generate_mcqs(document, tokenizer, model, num_questions=5)
    #     if mcqs:
    #         for mcq in mcqs:
    #             st.write(f"Question: {mcq}")
            
    #         # Save MCQs as a new PDF
    #         output_pdf_path = "mcq_output.pdf"
    #         create_mcq_pdf(mcqs, output_pdf_path)
            
    #         # Provide a download link for the new PDF
    #         with open(output_pdf_path, "rb") as f:
    #             st.download_button("Download MCQ PDF", f, file_name=output_pdf_path, mime="application/pdf")
        # else:
        #     st.write("No MCQs generated.")
