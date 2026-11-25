import os
import streamlit as st

# ---------------------------
# Load Streamlit Cloud secrets
# ---------------------------
for key in [
    "GEMINI_API_KEY",
    "QDRANT_URL",
    "QDRANT_API_KEY"
]:
    if key in st.secrets:
        os.environ[key] = str(st.secrets[key])

from graph_engine import ask_graph


# ---------------------------
# Page config
# ---------------------------
st.set_page_config(
    page_title="CourseMate",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------
# Custom CSS
# ---------------------------
st.markdown("""
<style>
    /* Main app background */
    .stApp {
        background: linear-gradient(180deg, #0b0f19 0%, #111827 100%);
        color: #f9fafb;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #111827 0%, #0f172a 100%);
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    [data-testid="stSidebar"] * {
        color: #f9fafb;
    }

    /* Hero section */
    .hero-box {
        padding: 28px 24px;
        border-radius: 20px;
        background: linear-gradient(135deg, rgba(59,130,246,0.18), rgba(16,185,129,0.12));
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 10px 30px rgba(0,0,0,0.18);
        margin-bottom: 18px;
    }

    .hero-title {
        font-size: 42px;
        font-weight: 800;
        line-height: 1.1;
        color: #ffffff;
        margin-bottom: 8px;
    }

    .hero-subtitle {
        font-size: 16px;
        color: #d1d5db;
        margin-bottom: 16px;
    }

    .pill-row {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        margin-top: 8px;
    }

    .pill {
        padding: 8px 14px;
        border-radius: 999px;
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.08);
        font-size: 13px;
        color: #f3f4f6;
    }

    /* Cards */
    .info-card {
        padding: 16px 18px;
        border-radius: 16px;
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.07);
        margin-bottom: 12px;
    }

    .info-card h4 {
        margin: 0 0 6px 0;
        color: #ffffff;
    }

    .info-card p {
        margin: 0;
        color: #d1d5db;
        font-size: 14px;
    }

    /* Chat message styling */
    [data-testid="stChatMessage"] {
        border-radius: 18px;
        padding: 6px;
        margin-bottom: 10px;
    }

    /* Input box */
    [data-testid="stChatInputTextArea"] textarea {
        background-color: rgba(255,255,255,0.06) !important;
        color: white !important;
        border-radius: 14px !important;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.10);
        background: rgba(255,255,255,0.06);
        color: white;
        font-weight: 600;
    }

    .stButton > button:hover {
        border: 1px solid rgba(96,165,250,0.45);
        background: rgba(59,130,246,0.10);
        color: white;
    }

    /* Small muted text */
    .muted {
        color: #9ca3af;
        font-size: 13px;
    }

    /* Footer note */
    .footer-note {
        text-align: center;
        color: #9ca3af;
        font-size: 13px;
        margin-top: 20px;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------
# Sidebar
# ---------------------------
with st.sidebar:
    st.markdown("## 🎓 CourseMate")
    st.markdown("**IIUC CSE Academic Assistant**")

    st.markdown("---")

    st.markdown("### What this app can do")
    st.markdown("""
- Answer **IIUC CSE curriculum** questions  
- Check **course prerequisites**  
- Respond using **RAG + Tools + LangGraph**
""")

    st.markdown("---")

    st.markdown("### Example Questions")
    st.markdown("""
- Which course covers Data Structures?  
- Can I take CSE-2101? My student ID is S-014.  
- Tell me about the IIUC CSE curriculum.  
- What is the prerequisite of CSE-2421?
""")

    st.markdown("---")

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown(
        "<div class='muted'>Built with Streamlit, LangChain, LangGraph, Gemini and Qdrant.</div>",
        unsafe_allow_html=True
    )


# ---------------------------
# Session State
# ---------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None


# ---------------------------
# Hero Section
# ---------------------------
st.markdown("""
<div class="hero-box">
    <div class="hero-title">CourseMate</div>
    <div class="hero-subtitle">
        Your AI-powered IIUC CSE academic assistant for curriculum queries, course guidance and prerequisite checking.
    </div>
    <div class="pill-row">
        <div class="pill">RAG-powered</div>
        <div class="pill">Prerequisite Checker</div>
        <div class="pill">LangGraph Workflow</div>
        <div class="pill">IIUC CSE Focused</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ---------------------------
# Quick Prompt Buttons
# ---------------------------
st.markdown("### Try a quick question")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📘 Data Structures course", use_container_width=True):
        st.session_state.pending_prompt = "Which course covers Data Structures?"

with col2:
    if st.button("✅ Eligibility check", use_container_width=True):
        st.session_state.pending_prompt = "Can I take CSE-2101? My student ID is S-014."

with col3:
    if st.button("📚 About CSE curriculum", use_container_width=True):
        st.session_state.pending_prompt = "Tell me about the IIUC CSE curriculum."

st.markdown("")


# ---------------------------
# Optional info cards
# ---------------------------
info_col1, info_col2, info_col3 = st.columns(3)

with info_col1:
    st.markdown("""
    <div class="info-card">
        <h4>Curriculum Search</h4>
        <p>Ask about courses, semesters, credits and curriculum details from the IIUC CSE document.</p>
    </div>
    """, unsafe_allow_html=True)

with info_col2:
    st.markdown("""
    <div class="info-card">
        <h4>Eligibility Support</h4>
        <p>Check whether a student can take a specific course based on prerequisite completion.</p>
    </div>
    """, unsafe_allow_html=True)

with info_col3:
    st.markdown("""
    <div class="info-card">
        <h4>Simple Answers</h4>
        <p>CourseMate gives short, clear and student-friendly responses with academic relevance.</p>
    </div>
    """, unsafe_allow_html=True)


st.markdown("---")


# ---------------------------
# Render Chat History
# ---------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ---------------------------
# Input handling
# ---------------------------
user_input = st.chat_input("Ask about IIUC CSE courses...")

question = None

if user_input:
    question = user_input
elif st.session_state.pending_prompt:
    question = st.session_state.pending_prompt
    st.session_state.pending_prompt = None


# ---------------------------
# Process Question
# ---------------------------
if question:
    # Store user message
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("CourseMate is thinking..."):
            try:
                answer = ask_graph(question)

                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as e:
                error_msg = "Something went wrong. Please try again."
                st.error(error_msg)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg
                })

                print("CourseMate Error:", str(e))


# ---------------------------
# Footer
# ---------------------------
st.markdown(
    "<div class='footer-note'>CourseMate • IIUC CSE Academic Assistant</div>",
    unsafe_allow_html=True
)