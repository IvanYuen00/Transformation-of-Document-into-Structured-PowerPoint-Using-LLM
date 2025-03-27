from langchain.embeddings import HuggingFaceInstructEmbeddings
import os

# Environment variable for transformer models
os.environ["SENTENCE_TRANSFORMERS_HOME"] = "/path/to/transformers"  # Masked

model_name = "hkunlp/instructor-xl"
encode_kwargs = {'normalize_embeddings': True, 'batch_size': 1}
instructor_model = HuggingFaceInstructEmbeddings(
    model_name=model_name,
    encode_kwargs=encode_kwargs,
    embed_instruction="Represent the source for retrieval;",
    query_instruction="Represent the source for retrieving relevant document;",
)
