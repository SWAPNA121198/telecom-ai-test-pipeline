import json
from datetime import datetime
from google import genai

MODEL = "gemini-3.5-flash-lite"  # change here if Google retires this name


def ask_ai_for_locator(html, old_locator, description):
    prompt = f"""You are a QA automation engineer.
A test could not find this element: {old_locator}
The element is: {description}
Here is the page HTML:
{html}
Reply with ONLY one CSS selector that finds that single element.
No explanation, no quotes, no code fences."""
    client = genai.Client()
    response = client.models.generate_content(model=MODEL, contents=prompt)
    return response.text.strip().strip("`")


def heal_click(page, locator, description):
    # 1. Try the original locator first
    try:
        page.click(locator, timeout=3000)
        return
    except Exception:
        pass

    # 2. It failed, so ask the AI for a new locator
    new_locator = ask_ai_for_locator(page.content(), locator, description)

    # 3. Check the suggestion matches exactly one element
    if page.locator(new_locator).count() != 1:
        raise AssertionError(f"AI suggested '{new_locator}', which does not match exactly one element")

    # 4. Use it for this run only
    page.click(new_locator, timeout=3000)

    # 5. Save the suggestion as PENDING, for a human to review
    record = {
        "time": f"{datetime.now():%Y-%m-%d %H:%M}",
        "old": locator,
        "new": new_locator,
        "element": description,
    }
    with open("ai/healing_pending.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
        print(f"\n[self-healing] '{locator}' not found -> AI suggested '{new_locator}'")