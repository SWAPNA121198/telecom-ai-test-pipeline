import time
from datetime import datetime
from playwright.sync_api import sync_playwright
from ai.healing import ask_ai_for_locator

BASE = "http://localhost:8000/app/"


def go_login(page):
    page.goto(BASE + "login.html")


def go_plans(page):
    go_login(page)
    page.fill("#mobile-number", "9876543210")
    page.fill("#password", "Test@123")
    page.click("#login-btn")
    page.wait_for_selector("#plan-basic")


def go_recharge(page):
    go_plans(page)
    page.click("#select-standard-btn")
    page.wait_for_selector("#recharge-btn")


# (page name, how to reach it, broken locator, element description, real id)
CASES = [
    ("Login", go_login, "#mobile", "the mobile number input box", "mobile-number"),
    ("Login", go_login, "#pwd", "the password input box", "password"),
    ("Login", go_login, "#login-button", "the Login button", "login-btn"),
    ("Plans", go_plans, "#basic-select", "the Select button of the Basic plan", "select-basic-btn"),
    ("Plans", go_plans, "#premium-select-button", "the Select button of the Premium plan", "select-premium-btn"),
    ("Recharge", go_recharge, "#mobile-input", "the mobile number to recharge input box", "recharge-mobile"),
    ("Recharge", go_recharge, "#card-input", "the card number input box", "card-number"),
    ("Recharge", go_recharge, "#recharge-now", "the Recharge Now button", "recharge-btn"),
    ("Recharge", go_recharge, "#result-message", "the message line shown under the Recharge Now button", "message"),
]


def is_correct(page, selector, real_id):
    # Correct = the AI's selector matches exactly one element, and it is the real one
    try:
        loc = page.locator(selector)
        return loc.count() == 1 and loc.evaluate("e => e.id") == real_id
    except Exception:
        return False


rows = []
correct = 0
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    for name, go, broken, desc, real_id in CASES:
        go(page)
        try:
            suggestion = ask_ai_for_locator(page.content(), broken, desc)
        except Exception as e:
            suggestion = f"ERROR: {str(e)[:40]}"
        ok = is_correct(page, suggestion, real_id)
        correct += ok
        rows.append((name, desc, broken, suggestion, "Yes" if ok else "No"))
        print(f"{name:9} {broken:24} -> {suggestion:40} {'OK' if ok else 'WRONG'}")
        time.sleep(8)  # stay within the free-tier rate limit
    browser.close()

total = len(CASES)
with open("ai/healing_accuracy.md", "w", encoding="utf-8") as f:
    f.write(f"# Healing accuracy ({datetime.now():%Y-%m-%d})\n\n")
    f.write(f"**Healed {correct} of {total} broken locators correctly ({correct / total:.0%}).**\n\n")
    f.write("| Page | Element | Broken locator | AI suggestion | Correct? |\n|---|---|---|---|---|\n")
    for r in rows:
        f.write("| " + " | ".join(r) + " |\n")
print(f"\nHealed {correct} of {total} correctly. Saved to ai/healing_accuracy.md")