
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

print("Connecting to Gemini...")

model = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0
)

print("Sending request...")

response = model.invoke("Say hello in one sentence.")

print("Gemini Response:", response.content)
print("Connection successful!")
