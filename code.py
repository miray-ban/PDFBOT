import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter

with st.sidebar :
    st.title(' llm chat app ')
    st.markdown('''
       ## About
       this app is an llm-powered chatbot build using:
       - stramlit
       - langchain 
       - openai
    ''')

    add_vertical_space(5)
    st.write('made with love by kaoutar')



def main():
    st.write("chto PDF")
    
    pdf=st.file_uploader("Upload your PDF", type='pdf')

    #st.write(pdf)
    if pdf is not None:
        pdf_reader = PdfReader(pdf)

        text = ""
        for page in pdf_reader.pages:
            text+=page.extract_text()
        

        text_splitter=RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )

        #st.write(text)




if __name__ == '__main__':
    main()

