import streamlit as st
import tempfile
import shutil
import os
from langchain.vectorstores import Chroma
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOllama
from langchain.chains import RetrievalQA


def rag_ita_pdf():
    template = """Sei un assistente che risponde alle domande. Utilizza i seguenti elementi di contesto forniti per rispondere alla domanda. Se non conosci la risposta, dì semplicemente che non la conosci. Utilizza al massimo tre frasi e mantieni la risposta concisa.
    Domanda: {question} 
    Contesto: {context} 
    Risposta:
    """
    prompt = ChatPromptTemplate.from_template(template)
    model = ChatOllama(model="llama3")
    embeddings = (OllamaEmbeddings(model="llama3"))


    uploaded_file = st.file_uploader("Carica un file pdf", type="pdf")

    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
            shutil.copyfileobj(uploaded_file, tmpfile)
            file_path = tmpfile.name
        loader = PyMuPDFLoader(file_path)
        document = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        chunks = text_splitter.split_documents(document)
        vectorstore = Chroma.from_documents(chunks, embeddings)
        retriever = vectorstore.as_retriever()
        chain = (
                {"contesto": retriever, "domanda": RunnablePassthrough()}
                | prompt
                | model
                | StrOutputParser()
        )
    # get question from user
    question = st.text_input("Fai la tua domanda")
    if st.button('Ottieni la risposta'):
        result = chain.invoke(question)
        answer = result["risposta"]
        st.write("Risposta:", result)

    if file_path:
        os.unlink(file_path)
    
    return 


def generate_response(uploaded_file,query_text):
    # Load document if file is uploaded
    if uploaded_file is not None:
        #documents = [uploaded_file.read().decode()]
         with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
            shutil.copyfileobj(uploaded_file, tmpfile)
            file_path = tmpfile.name
        
            loader = PyMuPDFLoader(file_path)
            document = loader.load()
            # Split documents into chunks
            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
            texts = text_splitter.create_documents(document)
            # Select embeddings
            embeddings = (OllamaEmbeddings(model="llama3"))
            # Create a vectorstore from documents
            db = Chroma.from_documents(texts, embeddings)
            # Create retriever interface
            retriever = db.as_retriever()
            # Choose model
            llm = ChatOllama(model="llama3")
            # Create QA chain
            qa = RetrievalQA.from_chain_type(llm=llm, chain_type='stuff', retriever=retriever)
            
            answer = qa.run(query_text)
        
            if file_path:
                os.unlink(file_path)

    return answer

# Page title
st.set_page_config(page_title='🦜🔗 Ask the Doc App')
st.title('🦜🔗 Ask the Doc App')

# File upload
uploaded_file = st.file_uploader('Upload an article', type='pdf')
# Query text
query_text = st.text_input('Enter your question:', placeholder = 'Please provide a short summary.', disabled=not uploaded_file)

# Form input and query
result = []
with st.form('myform', clear_on_submit=True):
    submitted = st.form_submit_button('Submit', disabled=not(uploaded_file and query_text))
    if submitted:
        with st.spinner('Calculating...'):
            response = generate_response(uploaded_file, query_text)
            result.append(response)

if len(result):
    st.info(response)