import streamlit as st
from streamlit_pdf_viewer import pdf_viewer

uploaded_file = st.file_uploader('Choose your .pdf file', type="pdf")
if uploaded_file is not None:
    binary_data = uploaded_file.getvalue()
    pdf_viewer(binary_data)