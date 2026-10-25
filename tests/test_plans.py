from playwright.sync_api import expect


def login(page):
    page.goto("http://localhost:8000/app/login.html")
    page.fill("#mobile-number", "9876543210")
    page.fill("#password", "Test@123")
    page.click("#login-btn")


def test_plans_page_shows_three_plans(page):
    login(page)
    expect(page.locator("#plan-basic")).to_contain_text("AED 50")
    expect(page.locator("#plan-standard")).to_contain_text("AED 100")
    expect(page.locator("#plan-premium")).to_contain_text("AED 200")
    expect(page.locator("#select-basic-btn")).to_be_visible()
    expect(page.locator("#select-standard-btn")).to_be_visible()
    expect(page.locator("#select-premium-btn")).to_be_visible()


def test_select_plan_opens_recharge_page(page):
    login(page)
    page.click("#select-standard-btn")
    expect(page.locator("#plan-summary")).to_have_text("Selected plan: Standard - AED 100")