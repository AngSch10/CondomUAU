# Locally
1. poetry shell
2. streamlit run app/main.py

# Docker
1. docker build -t streamlit-langchain-app .
2. docker run -p 8501:8501 streamlit-langchain-app

# Kill process locking PORT on Mac
lsof -i tcp:PORT
kill -9 <PID>