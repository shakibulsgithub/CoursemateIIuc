
import os

from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent

from tools import check_prerequisites
from rag_tools import search_cse_information


load_dotenv()


# 1. Gemini Model
model = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0
)


# 2. Available Tools
tools = [
    check_prerequisites,
    search_cse_information
]


# 3. Create CourseMate Agent
agent = create_agent(
    model=model,
    tools=tools,
    system_prompt="""
    You are CourseMate, an IIUC CSE academic assistant.

    You have two tools:

    1. search_cse_information:
       Use for questions about courses, curriculum,
       semesters, credits and academic information.

    2. check_prerequisites:
       Use when students ask whether they are eligible
       to take a particular course.

    Always use the appropriate tool.

    Never invent academic information.
    Explain answers in simple language.
    Include source information when available.
    If required information is missing, ask the student.
    """
)


# 4. Reusable Agent Function
def ask_agent(question):

    result = agent.invoke({
        "messages": [
            {"role": "user", "content": question}
        ]
    })

    content = result["messages"][-1].content

    if isinstance(content, list):

        return "\n".join(
            item["text"]
            for item in content
            if isinstance(item, dict)
            and item.get("type") == "text"
        )

    return str(content)
