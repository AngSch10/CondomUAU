import streamlit as st
from langchain_community.llms import Ollama

st.title('🦜🔗 Quickstart App')

def generate_response(input_text):
    #llm = Ollama(model="llama3",base_url="http://ollama-container:11434", verbose=True) # for Docker
    llm = Ollama(model="llama3")
    st.info(llm.invoke(input_text))

with st.form('my_form'):
    text = st.text_area('Enter text:', 'Ask what you want!')
    submitted = st.form_submit_button('Submit')
    if submitted:
        generate_response(text)