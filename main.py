from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from pydub import AudioSegment
import os
import numpy as np
from instructor_model import *
import whisper
from langchain.vectorstores import FAISS
from ppt_generation import *
import requests
from langchain.llms import TextGen
import subprocess

# Masked sensitive URLs
upload_api_url = 'http://<UPLOAD_SERVER_IP>:<PORT>/save_vectorstore'  
save_vectorstore_api_url = 'http://<SAVE_SERVER_IP>:<PORT>/save_vectorstore'
embed_query_api_url = 'http://<EMBED_SERVER_IP>:<PORT>/embed_query'

# Masked LLM server address
normal_llm = TextGen(model_url="http://<LLM_SERVER_IP>:<PORT>/", max_new_tokens=2048, seed=42, verbose=False)

# Environment variable for cache directory
os.environ["XDG_CACHE_HOME"] = "/path/to/cache/"  # Masked

# Define a Pydantic model to represent the request payload
class QueryRequest(BaseModel):
    docx_path: str

class QueryRequest2(BaseModel):
    docx_name: str
    query: str

class QueryRequest3(BaseModel):
    docx_name: str
    list_pinned_message: list

# Initialize FastAPI
app = FastAPI(
    title="Speech to Text",
    description='',
    summary="Deadpool's favorite app. Nuff said."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
)

@app.post("/document_to_vectorstore")
def embed_query(request: QueryRequest):
    docx_path = request.docx_path
    # API - upload file to API Data
    with open(docx_path, 'rb') as file:
        response = requests.post(upload_api_url, files={'file': file})
    docx_name = os.path.basename(docx_path)
    # API - Embed document to Vectorstore and save in FAISS
    query_payload = {'file_name': docx_name}
    response = requests.post(save_vectorstore_api_url, json=query_payload)
    return 'Successfully converted to Vectorstore'

@app.post("/query_to_response")
def query_to_response(request: QueryRequest2):
    similar_content = []
    # Masked FAISS path
    new_db = FAISS.load_local(os.path.join("/path/to/faiss/", request.docx_name), instructor_model)
    query_payload = {'query': request.query}
    response = requests.post(embed_query_api_url, json=query_payload)
    vector = response.json()
    similar_source = new_db.similarity_search_by_vector(vector, k=2)
    for content in similar_source:
        similar_content.append(content.page_content)
    ans = normal_llm(f"""[INST] <<SYS>>
Given the following text, write a concise summary of it. Do not leave out important information. Do not include any information that did not relate to user's query.
Give your answer in point form.
<</SYS>>

Text:

{similar_content}

User's query:

{request.query}
[/INST]
Summary: """)
    return ans

@app.post("/generate_ppt_md")
def generate_ppt_md(request: QueryRequest3):
    result = ppt_md_generation(request.list_pinned_message)
    # Masked directories for markdown and PPTX generation
    with open(os.path.join('/path/to/markdown/', str(request.docx_name) + '.md'), 'w') as md:
        md.write(result[3:-3])
    subprocess.run([
        "/path/to/pandoc_env/bin/pandoc", 
        './markdown/' + str(request.docx_name) + '.md', 
        "-o", 
        "./PPT/" + str(request.docx_name) + ".pptx", 
        "--slide-level=2"
    ])
    return 'PPTX successfully generated'
