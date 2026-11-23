import os
import pytest
from playwright.sync_api import expect
from ai.healing import heal_click

needs_key = pytest.mark.skipif(
    not os.environ.get("GEMINI_API_KEY"),
    reason="needs GEMINI_API_KEY",
)


@needs_key
def test_login_with_broken_locator(page):
    page.goto("http://localhost:8000/app/login.html")
    page.fill("#mobile-number", "9876543210")
    page.fill("#password", "Test@123")
    heal_click(page, "#login-btn", "the Login button")
    expect(page.locator("h2")).to_have_text("Choose a Prepaid Plan")