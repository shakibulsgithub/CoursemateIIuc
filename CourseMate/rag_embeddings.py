
import os
import re

from dotenv import load_dotenv

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings


# 1. Load API Key
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Gemini API key not found!")


# 2. Read extracted text
with open(
    "documents/extracted_text.txt",
    "r",
    encoding="utf-8"
) as file:
    text = file.read()


# 3. Separate pages
parts = re.split(r"--- Page (\d+) ---", text)

documents = []

for i in range(1, len(parts), 2):

    page_number = int(parts[i])
    page_text = parts[i + 1].strip()

    if page_text:
        documents.append(
            Document(
                page_content=page_text,
                metadata={
                    "source": "documents/cse.pdf",
                    "page": page_number
                }
            )
        )


# 4. Create chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = splitter.split_documents(documents)

print("Total chunks:", len(chunks))


# 5. Initialize embedding model
embedding_model = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    google_api_key=api_key,
    task_type="RETRIEVAL_DOCUMENT"
)


# 6. Convert chunks into vectors
texts = [chunk.page_content for chunk in chunks]

vectors = embedding_model.embed_documents(texts)


# 7. Display results
print("\nEmbedding completed!")

print("Total vectors:", len(vectors))

print("Vector dimensions:", len(vectors[0]))

print("\nFirst vector (first 10 values):")
print(vectors[0][:10])
