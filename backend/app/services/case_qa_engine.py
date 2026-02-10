from langchain_groq import ChatGroq

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.0
)

def answer_case_question(case_id, question, documents, issues):
    context = f"""
CASE ID: {case_id}

DOCUMENTS:
{documents}

ISSUES:
{issues}

Answer the user's question clearly, accurately, and in simple language.
If the question is about approval, do NOT give final approval — only risk guidance.
"""

    prompt = f"""
Context:
{context}

User Question:
{question}

Answer:
"""

    response = llm.invoke(prompt)
    return response.content
