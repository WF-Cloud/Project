import json
import os
import time

from dotenv import load_dotenv
from groq import Groq
import chromadb


# ============================================================
# CONFIGURATION
# ============================================================

CHROMA_PATH = "chroma"
QUESTIONS_PATH = "evaluation/questions.json"
RESULTS_PATH = "evaluation/results_groq.json"

COLLECTION_NAME = "utem_documents"

TOP_K = 3

MODEL_NAME = "openai/gpt-oss-20b"


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError(
        "GROQ_API_KEY was not found. "
        "Check your .env file."
    )


# ============================================================
# CREATE GROQ CLIENT
# ============================================================

groq_client = Groq(
    api_key=api_key
)

print("Groq client created!")


# ============================================================
# CONNECT TO CHROMADB
# ============================================================

chroma_client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

collection = chroma_client.get_collection(
    name=COLLECTION_NAME
)

print("ChromaDB connected!")
print(f"Collection: {COLLECTION_NAME}")


# ============================================================
# LOAD QUESTIONS
# ============================================================

with open(
    QUESTIONS_PATH,
    "r",
    encoding="utf-8"
) as f:

    questions = json.load(f)

print(f"Loaded {len(questions)} questions.")


# ============================================================
# GENERATE ANSWER
# ============================================================

def generate_answer(question, context):

    prompt = f"""
You are a helpful UTeM student information assistant.

Answer the user's question using ONLY the provided context.

Rules:

- Give a direct answer first.
- Use simple, natural language.
- Do not copy the context verbatim.
- Do not reproduce Markdown tables unless the user specifically asks for a table.
- Use bullet points only when they improve clarity.
- Do not include unnecessary headings.
- Do not make assumptions.
- Do not invent information.
- If the answer cannot be found in the context, say:
  "I don't have enough information in the provided UTeM documents to answer that."

Context:
{context}

Question:
{question}

Answer:
"""

    response = groq_client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content


# ============================================================
# RUN EVALUATION
# ============================================================

results = []


for item in questions:

    question_id = item["id"]
    category = item["category"]
    question = item["question"]
    expected_answer = item["expected_answer"]

    print("\n" + "=" * 70)

    print(f"Question {question_id}")
    print(f"Category: {category}")
    print(f"Question: {question}")


    # --------------------------------------------------------
    # RETRIEVE RELEVANT DOCUMENTS
    # --------------------------------------------------------

    search_results = collection.query(
        query_texts=[question],
        n_results=TOP_K
    )

    documents = search_results["documents"][0]


    # Combine retrieved chunks
    context = "\n\n".join(documents)


    print(f"Retrieved {len(documents)} chunks.")


    # --------------------------------------------------------
    # GENERATE ANSWER
    # --------------------------------------------------------

    start_time = time.perf_counter()

    answer = generate_answer(
        question,
        context
    )

    end_time = time.perf_counter()

    response_time = end_time - start_time


    # --------------------------------------------------------
    # DISPLAY ANSWER
    # --------------------------------------------------------

    print("\nExpected answer:")
    print(expected_answer)

    print("\nModel answer:")
    print(answer)

    print(
        f"\nResponse time: "
        f"{response_time:.2f} seconds"
    )


    # --------------------------------------------------------
    # SAVE RESULT
    # --------------------------------------------------------

    result = {
        "id": question_id,
        "category": category,
        "question": question,
        "expected_answer": expected_answer,
        "model": MODEL_NAME,
        "model_answer": answer,
        "response_time": round(response_time, 3),
        "retrieved_context": documents
    }

    results.append(result)


# ============================================================
# SAVE RESULTS
# ============================================================

with open(
    RESULTS_PATH,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        results,
        f,
        indent=4,
        ensure_ascii=False
    )


# ============================================================
# FINISHED
# ============================================================

print("\n" + "=" * 70)

print("Evaluation completed!")

print(
    f"Results saved to: "
    f"{RESULTS_PATH}"
)

print(
    f"Total questions evaluated: "
    f"{len(results)}"
)