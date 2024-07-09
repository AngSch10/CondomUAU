# Use the official Python base image from the Docker Hub
FROM python:3.10-slim

# Set environment variables
ENV POETRY_VERSION=1.8.3

# Install dependencies for Poetry and Streamlit
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Ensure poetry installs packages in the virtual environment
ENV PATH="/root/.local/bin:$PATH"

# Set work directory
WORKDIR /app

# Copy only the dependency files first
COPY pyproject.toml poetry.lock ./

# Install project dependencies
RUN poetry install --no-root

# Copy the rest of the application files
COPY . .

# Install the project in editable mode (optional, if you want to modify code without rebuilding)
RUN poetry install

# Expose Streamlit port
EXPOSE 8501

# Command to run the Streamlit app
CMD ["poetry", "run", "streamlit", "run", "app/main.py"]