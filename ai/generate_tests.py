from google import genai

MODEL = "gemini-3.5-flash-lite"   # if Google retires this name, change it here only

# 1. Read the requirements I wrote
with open("specs/telecom_requirements.txt", encoding="utf-8") as f:
    requirements = f.read()

# 2. Tell the AI what job to do
prompt = f"""You are a senior QA engineer testing a telecom prepaid recharge web app.

Read these requirements and write test cases for them.

Rules:
- Cover positive, negative and boundary scenarios.
- Use only what the requirements say. Do not invent features.
- Give each test case an ID like TC-01.
- Output a markdown table with these columns:
  ID | Requirement | Scenario | Type | Steps | Test data | Expected result

Requirements:
{requirements}
"""

# 3. Send it to the AI
client = genai.Client()
response = client.models.generate_content(model=MODEL, contents=prompt)

# 4. Show it and save it
print(response.text)
with open("ai/generated_test_cases.md", "w", encoding="utf-8") as f:
    f.write(response.text)
print("\nSaved to ai/generated_test_cases.md")