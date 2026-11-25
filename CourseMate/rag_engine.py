
import os
import requests

from dotenv import load_dotenv

from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
    ChatGoogleGenerativeAI
)

load_dotenv()

# Initialize embedding model
embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    task_type="RETRIEVAL_QUERY"
)

# Initialize Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0
)


def ask_coursemate(question):

    qdrant_url = os.getenv("QDRANT_URL").rstrip("/")
    qdrant_key = os.getenv("QDRANT_API_KEY")

    headers = {
        "api-key": qdrant_key,
        "Content-Type": "application/json"
    }

    # Convert question into vector
    query_vector = embeddings.embed_query(question)

    # Search Qdrant
    response = requests.post(
        f"{qdrant_url}/collections/coursemate_cse/points/query",
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

    if not results:
        return {
            "answer": "I could not find relevant information.",
            "sources": []
        }

    # Prepare context and sources
    context = ""
    sources = []

    for result in results:

        data = result["payload"]

        context += f"""
        Page: {data['page']}
        Content: {data['text']}
        """

        source = {
            "page": data["page"],
            "file": data["source"]
        }

        if source not in sources:
            sources.append(source)

    # Generate answer
    prompt = f"""
    You are CourseMate, an IIUC CSE academic assistant.

    Answer using only the provided academic context.

    Rules:
    - Give simple and clear answers.
    - Never invent information.
    - If the answer is unavailable, say so.
    - Do not assume missing academic rules.

    Academic Context:
    {context}

    Student Question:
    {question}
    """

    answer = llm.invoke(prompt)

    content = answer.content

    if isinstance(content, list):
        answer_text = "\n".join(
            item["text"]
            for item in content
            if isinstance(item, dict)
            and item.get("type") == "text"
        )
    else:
        answer_text = str(content)

    return {
        "answer": answer_text,
        "sources": sources
    }
