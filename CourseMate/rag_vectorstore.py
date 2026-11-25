
import os
import re
import requests

from dotenv import load_dotenv

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings


# 1. Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL", "").rstrip("/")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

if not GEMINI_API_KEY or not QDRANT_URL or not QDRANT_API_KEY:
    raise ValueError("Missing API credentials in .env")


# 2. Read extracted text
with open(
    "documents/extracted_text.txt",
    "r",
    encoding="utf-8"
) as file:
    text = file.read()


# 3. Recreate page-wise documents
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


# 5. Initialize Gemini Embeddings
embedding_model = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    google_api_key=GEMINI_API_KEY,
    task_type="RETRIEVAL_DOCUMENT"
)


# 6. Generate vectors
texts = [chunk.page_content for chunk in chunks]

vectors = embedding_model.embed_documents(texts)

print("Total vectors:", len(vectors))


# 7. Qdrant REST API configuration
collection_name = "coursemate_cse"

headers = {
    "api-key": QDRANT_API_KEY,
    "Content-Type": "application/json"
}

collection_url = f"{QDRANT_URL}/collections/{collection_name}"


# 8. Check collection
check = requests.get(
    collection_url,
    headers=headers,
    timeout=30
)

if check.status_code == 404:

    response = requests.put(
        collection_url,
        headers=headers,
        json={
            "vectors": {
                "size": 3072,
                "distance": "Cosine"
            }
        },
        timeout=30
    )

    response.raise_for_status()

    print("Qdrant collection created!")

elif check.status_code == 200:

    print("Qdrant collection already exists.")

else:

    check.raise_for_status()


# 9. Prepare and upload points
points = []

for i, (chunk, vector) in enumerate(zip(chunks, vectors)):

    points.append({
        "id": i,
        "vector": vector,
        "payload": {
            "text": chunk.page_content,
            "source": chunk.metadata["source"],
            "page": chunk.metadata["page"]
        }
    })


# 10. Upload in batches
upload_url = f"{collection_url}/points?wait=true"

for start in range(0, len(points), 10):

    batch = points[start:start + 10]

    response = requests.put(
        upload_url,
        headers=headers,
        json={"points": batch},
        timeout=120
    )

    response.raise_for_status()

    print(f"Uploaded {len(batch)} points.")


# 11. Verify storage
info_response = requests.get(
    collection_url,
    headers=headers,
    timeout=30
)

info_response.raise_for_status()

info = info_response.json()["result"]

print("\nUpload successful!")
print("Stored vectors:", info["points_count"])
print("Collection:", collection_name)
