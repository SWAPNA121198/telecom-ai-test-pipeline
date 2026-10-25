from playwright.sync_api import expect


def test_valid_login(page):
    page.goto("http://localhost:8000/app/login.html")
    page.fill("#mobile-number", "9876543210")
    page.fill("#password", "Test@123")
    page.click("#login-btn")
    expect(page.locator("h2")).to_have_text("Choose a Prepaid Plan")


def test_invalid_login(page):
    page.goto("http://localhost:8000/app/login.html")
    page.fill("#mobile-number", "1234567890")
    page.fill("#password", "wrong")
    page.click("#login-btn")
    expect(page.locator("#error-msg")).to_have_text("Invalid mobile number or password")

    

def test_empty_login(page):
    page.goto("http://localhost:8000/app/login.html")
    page.click("#login-btn")
    expect(page.locator("#error-msg")).to_have_text("Invalid mobile number or password")