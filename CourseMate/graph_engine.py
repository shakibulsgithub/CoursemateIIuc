
from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from agent import ask_agent


# 1. Define Graph State
class CourseMateState(TypedDict):
    question: str
    answer: str


# 2. Create Agent Node
def agent_node(state: CourseMateState):

    answer = ask_agent(state["question"])

    return {
        "answer": answer
    }


# 3. Create Graph
workflow = StateGraph(CourseMateState)


# 4. Add Node
workflow.add_node("agent", agent_node)


# 5. Add Edges
workflow.add_edge(START, "agent")
workflow.add_edge("agent", END)


# 6. Compile Graph
coursemate_graph = workflow.compile()


# 7. Reusable Function
def ask_graph(question):

    result = coursemate_graph.invoke({
        "question": question
    })

    return result["answer"]
