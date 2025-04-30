# Multilingual RAG
This application is a multilingual Retrieval-Augmented Generation (RAG) system built with FastAPI. It supports querying and generating responses across multiple languages using a simple API interface.

## Features

- **File Processing**: Supports file uploads, chunking, and metadata management.
- **LLM Integration**: Works with Cohere and OpenAI for text generation and embeddings.
- **Vector Database**: Uses Qdrant for vector-based data storage and retrieval.
- **Prometheus Metrics**: Integrated for monitoring application performance.
- **MongoDB Support**: Stores metadata and file-related information.

## Prerequisites

- **Python**: Version 3.10 or higher.
- **Docker**: Installed and running.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/MohamedSameh410/Multilingual-RAG.git
   cd Multilingual-RAG/src
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Setup the environment variables:
   ```bash
   cp .env.example .env
   ```
   for ```OPENAI_API_KEY``` & ```COHERE_API_KEY``` variables replace "YOUR API KEY" with your API keys, optionally set your environment variables.
   
   ---
   - To run the application through the local environment setup go to [here](#local-environment-setup).
   - To run the application through the Docker compose file go to [here](#dockerized-deployment).
   ---
   ### Local environment setup
   4- Run the MongoDB service:
   ```bash
   docker compose -f '../docker/docker-compose.yml' up -d --build mongodb
   ```
   5- Run the FastAPI server:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
   ---
   ### Dockerized deployment
   4- Setup the environment variables for Docker:
   ```bash
   cd ../docker/env
   cp .env.example.app .env.app
   cp .env.example.grafana .env.grafana
   ```
   - in the ```.env.app``` file replace ```OPENAI_API_KEY``` & ```COHERE_API_KEY``` variables with your API keys.
   - in the ```.env.grafana``` file add your preferred username & password for Grafana logging.
     
   5- Run Docker Compose Services:
   ```bash
   docker compose -f '../docker/docker-compose.yml' up -d --build
   ```
   **Notes**:
   - The docker compose file includes a Dockerfile to build the FastAPI image.
   - Make sure that all services are running, then you can access the FastAPI server through ```localhost``` or ```localhost:8000```.

## API Endpoints
- **File Uploading**:
  - POST ```/uploadfile```: Upload a single file.
- **File Processing**:
  - POST ```/processfile```: Process a single file.
  - POST ```/processAllFiles```: Process multiple files.
- **Data Retrieval**:
  - GET ```/getChunks_byFileId/{file_id}```: Retrieve data chunks by file ID.
- **Indexing**:
  - POST ```/index/push/{file_id}```: Push file data into the vector database.
  - GET ```/index/info/{file_id}```: Get indexing information for a file.
  - POST ```/index/search/{file_id}```: GET the most relevant chunks to the user query.
  - POST ```/index/answer/{file_id}```: Generate answer based on retrieved data.

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue if you find any bugs or have suggestions for improvements.
