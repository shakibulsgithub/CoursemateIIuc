
import os
from dotenv import load_dotenv
from google import genai

# Load API Key
load_dotenv()

# Check API Key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("API Key not found!")

# Connect with Gemini
client = genai.Client(api_key=api_key)

# CourseMate instruction
system_prompt = """
You are CourseMate, a university academic assistant.

You help students with:
1. Academic rules
2. Course information
3. Course prerequisites

Give simple and clear answers.
"""

# Take input from student
question = input("Student: ")

# Send question to AI
response = client.models.generate_content(
    model="gemini-3.1-flash-lite",
    contents=system_prompt + "\nStudent question: " + question
)

# Display answer
print("\nCourseMate:", response.text)
