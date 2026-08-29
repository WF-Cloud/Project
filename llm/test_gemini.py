import os
from google import genai
from dotenv import load_dotenv
load_dotenv()


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

print("Client created successfully")

response = client.models.generate_content(
    model="gemini-3.7-flash",
    contents="Say hello in one sentence."
)

print(response.text)