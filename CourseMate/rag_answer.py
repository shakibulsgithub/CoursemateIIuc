
import os
import requests

from dotenv import load_dotenv

from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
    ChatGoogleGenerativeAI
)


# 1. Load API credentials
load_dotenv()

GEMINI_KEY = os.getenv("GEMINI_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL").rstrip("/")
QDRANT_KEY = os.getenv("QDRANT_API_KEY")


# 2. Initialize embedding model
embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    google_api_key=GEMINI_KEY,
    task_type="RETRIEVAL_QUERY"
)


# 3. Initialize Gemini AI
llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    google_api_key=GEMINI_KEY,
    temperature=0
)


# 4. Connect to Qdrant
collection = "coursemate_cse"

headers = {
    "api-key": QDRANT_KEY,
    "Content-Type": "application/json"
}


# 5. Take student question
question = input("Student: ")


# 6. Convert question into vector
query_vector = embeddings.embed_query(question)


# 7. Retrieve relevant documents
response = requests.post(
    f"{QDRANT_URL}/collections/{collection}/points/query",
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


# 8. Prepare context
context = ""

for result in results:

    data = result["payload"]

    context += f"""
    Page: {data['page']}
    Source: {data['source']}
    Content: {data['text']}

    """


# 9. Create RAG prompt
prompt = f"""
You are CourseMate, a university academic assistant.

Answer the student's question using only the
provided academic context.

Rules:
1. Do not invent information.
2. If information is unavailable, say so.
3. Keep answers simple and clear.
4. Mention the source page number.
5. Do not treat unrelated information as relevant.

Academic Context:
{context}

Student Question:
{question}
"""


# 10. Generate final answer
answer = llm.invoke(prompt)


# 11. Display response
print("\nCourseMate:")
content = answer.content

if isinstance(content, list):
    for item in content:
        if isinstance(item, dict) and item.get("type") == "text":
            print(item["text"])
else:
    print(content)
