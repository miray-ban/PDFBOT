import streamlit as st
import os
import pickle
from dotenv import load_dotenv
from streamlit_extras.add_vertical_space import add_vertical_space
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import time

load_dotenv()

with st.sidebar:
    st.title('LLM Chat App')
    st.markdown('''  
       ## About  
       This app is an LLM-powered chatbot built using:  
       - Streamlit  
       - Langchain  
       - OpenAI  
    ''')
    add_vertical_space(5)
    st.write('Made with love by Kaoutar')

def main():
    st.write("Chat with PDF")
    
    # File uploader for PDF
    pdf = st.file_uploader("Upload your PDF", type='pdf')

    # Check if a file was uploaded
    if pdf is not None:
        st.write(f"Processing file: {pdf.name}")

        # Read the PDF
        pdf_reader = PdfReader(pdf)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""

        # Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(text=text)

        # Embeddings
        store_name = pdf.name[:-4]

        # Check if embeddings already exist
        if os.path.exists(f"{store_name}.pkl"):
            with open(f"{store_name}.pkl", "rb") as f:
                VectorStore = pickle.load(f)
            st.write('Embeddings loaded successfully.')
        else:
            attempt = 0
            success = False
            while attempt < 3 and not success:  # Retry logic
                try:
                    embeddings = OpenAIEmbeddings()
                    VectorStore = FAISS.from_texts(chunks, embedding=embeddings)
                    with open(f"{store_name}.pkl", "wb") as f:
                        pickle.dump(VectorStore, f)
                    st.write("Embeddings created and saved.")
                    success = True
                except Exception as e:
                    if 'quota' in str(e).lower():
                        st.error("You have exceeded your OpenAI API quota. Please check your plan and usage.")
                        return
                    else:
                        st.error(f"Error with embeddings: {e}")
                        attempt += 1
                        time.sleep(2)  # Wait before retrying

        # Query input
        query = st.text_input("Ask a question about your PDF file:")

        if query:
            docs = VectorStore.similarity_search(query=query)
            for doc in docs:
                st.write(doc)

    else:
        st.write("Please upload a PDF file.")

if __name__ == '__main__':
    main()
