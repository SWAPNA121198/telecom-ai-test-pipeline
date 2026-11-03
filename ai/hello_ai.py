from google import genai

client = genai.Client()  # reads GEMINI_API_KEY from the environment

response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents="Say hello to a QA tester in one sentence.",
)
print(response.text)