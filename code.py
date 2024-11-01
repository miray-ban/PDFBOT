import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space



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




if __name__ == '__main__':
    main()

