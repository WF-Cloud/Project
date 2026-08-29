import os
from openai import OpenAI

OPENAI_MODEL = "gpt-5"

client = OpenAI(
    api_key=os.environ.get("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")
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

    response = client.responses.create(
        model=OPENAI_MODEL,
        input=prompt
    )

    return response.output_text