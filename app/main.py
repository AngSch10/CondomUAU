import os
import requests
import streamlit as st
#from llama_index import LlamaIndex

OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://ollama:8000')

st.title("Llama and Ollama App")

#if st.button('Query Llama'):
#    index = LlamaIndex()
#    response = index.query("Hello, Llama!")
#    st.write(response)

if st.button('Query Ollama'):
    response = requests.post(
        f"{OLLAMA_URL}/generate",
        json={"prompt": "Hello, Ollama!"}
    )
    st.write(response.json())