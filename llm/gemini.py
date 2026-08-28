import os
from google import genai
GEMINI_MODEL = "gemini-3.7-flash"


client = genai.Client(
    api_key=os.environ.get("AQ.Ab8RN6KvzdH71posjJIN9dQNI5cCdmZ09XZwRbpbpLEtuA9OmA")
)



def generate_answer(question, context):

    prompt = f"""
You are a helpful UTeM student information assistant.

Answer the user's question using ONLY the provided context.

If the answer cannot be found in the context, say that you
do not have enough information to answer the question.

Context:
{context}

Question:
{question}

Answer:
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    return response.text