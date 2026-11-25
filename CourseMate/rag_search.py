
import os
import requests

from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# 1. Load API credentials
load_dotenv()

qdrant_url = os.getenv("QDRANT_URL").rstrip("/")
qdrant_key = os.getenv("QDRANT_API_KEY")

# 2. Connect embedding model for questions
embedding_model = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    task_type="RETRIEVAL_QUERY"
)

# 3. Connect to Qdrant REST API
collection = "coursemate_cse"

headers = {
    "api-key": qdrant_key,
    "Content-Type": "application/json"
}

# 4. Ask student
question = input("Student: ")

# 5. Convert question into vector
query_vector = embedding_model.embed_query(question)

# 6. Search relevant information
response = requests.post(
    f"{qdrant_url}/collections/{collection}/points/query",
    headers=headers,
    json={
        "query": query_vector,
        "limit": 3,
        "with_payload": True
    },
    timeout=60
)

response.raise_for_status()

results = response.json()["result"]["points"]

# 7. Display search results
print("\nRelevant Information:\n")

for result in results:

    payload = result["payload"]

    print("Similarity score:", result["score"])
    print("Page:", payload["page"])
    print("Text:", payload["text"])
    print("-" * 50)
