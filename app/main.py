import streamlit as st
from langchain_community.llms import Ollama

st.title('🦜🔗 Quickstart App')

def generate_response(input_text):
    llm = Ollama(model="llama3",base_url="http://ollama-container:11434", verbose=True) 
    st.info(llm.invoke(input_text))

with st.form('my_form'):
    text = st.text_area('Enter text:', 'What are the three key pieces of advice for learning how to code?')
    submitted = st.form_submit_button('Submit')
    if submitted:
        generate_response(text)