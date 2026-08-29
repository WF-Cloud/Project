import os
from dotenv import load_dotenv
from google import genai
GEMINI_MODEL = "gemini-3.7-flash"

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)
print("Gemini client created!")

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