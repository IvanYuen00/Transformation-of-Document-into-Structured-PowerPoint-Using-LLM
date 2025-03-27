# Transformation of Document into Structured PowerPoint Using LLM


This repository contains a FastAPI-based application for generating Markdown-formatted presentations from a list of pinned messages or document content. The generated Markdown can be converted into a PowerPoint presentation using `pandoc`. The app also supports querying document embeddings and converting documents to vectorstores.

---

## Features

- **Convert Documents to Vectorstores**: Upload `.docx` documents, convert them to embeddings using FAISS, and save them as vectorstores.
- **Query Document Embeddings**: Retrieve relevant document content based on a user query and summarize it in point form.
- **Generate Markdown Presentations**: Generate presentations in Markdown format based on pinned messages or summarized content, with strict formatting rules.
- **Convert Markdown to PowerPoint**: Use `pandoc` to convert generated Markdown into `.pptx` slides.

---

## Requirements

### Dependencies

- Python 3.8+
- Required Python libraries:
  - `fastapi`
  - `pydantic`
  - `pydub`
  - `numpy`
  - `langchain`
  - `whisper`
  - `requests`
  - `subprocess`
- `pandoc` installed on the system for Markdown-to-PPTX conversion.

### Environment Variables

- `XDG_CACHE_HOME`: Set to a directory to store cache files.
- `SENTENCE_TRANSFORMERS_HOME`: Directory for storing transformer model files.

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/speech-to-text-presentation.git
   cd speech-to-text-presentation
   ```

2. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Ensure `pandoc` is installed on your system:

   ```bash
   sudo apt install pandoc
   ```

4. Set the required environment variables:

   ```bash
   export XDG_CACHE_HOME=/path/to/cache
   export SENTENCE_TRANSFORMERS_HOME=/path/to/transformers
   ```

---

## Usage

### Running the FastAPI App

Start the FastAPI server:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### API Endpoints

#### 1. **Convert Document to Vectorstore**
   - **Endpoint**: `/document_to_vectorstore`
   - **Method**: `POST`
   - **Request Body**:
     ```json
     {
       "docx_path": "path/to/document.docx"
     }
     ```
   - **Response**: `"Successfully converted to Vectorstore"`

#### 2. **Query Document Embeddings**
   - **Endpoint**: `/query_to_response`
   - **Method**: `POST`
   - **Request Body**:
     ```json
     {
       "docx_name": "document_name",
       "query": "Your query here"
     }
     ```
   - **Response**: A concise summary of relevant content in point form.

#### 3. **Generate Markdown Presentation**
   - **Endpoint**: `/generate_ppt_md`
   - **Method**: `POST`
   - **Request Body**:
     ```json
     {
       "docx_name": "presentation_name",
       "list_pinned_message": ["Pinned message 1", "Pinned message 2"]
     }
     ```
   - **Response**: `"PPTX successfully generated"`

---

## Code Overview

### `ppt_generation.py`

This module generates Markdown-formatted presentations using the `TextGen` model from Langchain. Key constraints for the Markdown format include:
- Titles and text are concise.
- The presentation includes a table of contents, summary, and at least 5 slides.
- No images or links are included.
- Bullet points are used wisely.

**Function**:
- `ppt_md_generation(list_pinned)`: Sends the pinned messages to the model and returns the formatted Markdown.

---

### `main.py`

The main FastAPI application containing the following endpoints:
- `/document_to_vectorstore`: Converts `.docx` files into vectorstores using FAISS.
- `/query_to_response`: Retrieves and summarizes relevant content from vectorstores based on a query.
- `/generate_ppt_md`: Generates Markdown presentations and converts them into PowerPoint slides using `pandoc`.

---

### `instructor_model.py`

Defines the HuggingFace Instructor-based embedding model for query and document representation using the `langchain` library.

**Model**:
- `HuggingFaceInstructEmbeddings`: Configured with instructions for source and query embeddings.

---

## Example Workflow

1. **Convert Document to Vectorstore**:
   - Upload a document using `/document_to_vectorstore`.

2. **Query Document Embeddings**:
   - Query the vectorstore for relevant content using `/query_to_response`.

3. **Generate Presentation**:
   - Provide a list of pinned messages or summarized content to `/generate_ppt_md`.

4. **Convert to PowerPoint**:
   - The Markdown is automatically converted to `.pptx` using `pandoc`.

---


## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Acknowledgments

- [LangChain](https://www.langchain.com/) for the LLM-based integration.
- [HuggingFace](https://huggingface.co/) for the Instructor embeddings model.
- [Pandoc](https://pandoc.org/) for Markdown-to-PPTX conversion.
