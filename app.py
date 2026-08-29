from flask import Flask, render_template, request, jsonify
from retriever import retrieve_documents
#from llm.gemini_llm import generate_answer
from llm.groq_llm import generate_answer
#from llm.openai_llm import generate_answer

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    documents = retrieve_documents(user_message)

    context = "\n\n".join(
        [doc.page_content for doc in documents]
    )
    
    reply = generate_answer(
        user_message,
        context
    )

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)