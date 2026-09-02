import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_MODEL = "openai/gpt-oss-20b"

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_answer(question, context):

    prompt = f"""
You are a helpful UTeM student information assistant.

Answer the user's question using ONLY the provided context.

If the answer cannot be found in the context, say that you
do not have enough information to answer the question.

Rules:
- Give a direct answer first.
- Use simple, natural language.
- Do not copy the context verbatim.
- Do not reproduce Markdown tables unless the user specifically asks for a table.
- Do not include unnecessary headings.
- Do not include source text, page numbers, or document formatting unless requested.
- Use bullet points only when they make the answer clearer.
- If the context does not contain enough information, say: "I don't have enough information in the provided UTeM documents to answer that."


Context:
{context}

Question:
{question}

Answer:
"""

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content