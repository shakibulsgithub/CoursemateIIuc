
from langchain.tools import tool
from rag_engine import ask_coursemate


@tool
def search_cse_information(question: str) -> str:
    """
    Search the IIUC CSE curriculum and answer academic
    questions about courses, credits, semesters and
    other information available in the curriculum.
    """

    result = ask_coursemate(question)

    answer = result["answer"]

    sources = result["sources"]

    source_text = ""

    for source in sources:
        source_text += (
            f"\nSource: Page {source['page']}"
        )

    return answer + source_text
