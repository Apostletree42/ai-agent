import os
import sys
from dotenv import load_dotenv
from google import genai

if len(sys.argv) < 2:
    print("Usage: python3 main.py \"Your prompt here\"")
    sys.exit(1)

prompt = sys.argv[1]

flag = sys.argv[2] if len(sys.argv) > 2 else None

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client  = genai.Client(api_key=api_key)
response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=prompt
)
print(response.text)
if(flag == "--verbose"):
    print(f"User prompt: {prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")