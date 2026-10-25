from playwright.sync_api import expect


def open_recharge_page(page):
    # Log in, then choose the Standard plan
    page.goto("http://localhost:8000/app/login.html")
    page.fill("#mobile-number", "9876543210")
    page.fill("#password", "Test@123")
    page.click("#login-btn")
    page.click("#select-standard-btn")


def test_recharge_success(page):
    open_recharge_page(page)
    page.fill("#recharge-mobile", "9876543210")
    page.fill("#card-number", "1111222233334444")
    page.click("#recharge-btn")
    expect(page.locator("#message")).to_have_text("Recharge successful")


def test_invalid_mobile_number(page):
    open_recharge_page(page)
    page.fill("#recharge-mobile", "12345")
    page.fill("#card-number", "1111222233334444")
    page.click("#recharge-btn")
    expect(page.locator("#message")).to_have_text("Invalid mobile number")


def test_payment_failed(page):
    open_recharge_page(page)
    page.fill("#recharge-mobile", "9876543210")
    page.fill("#card-number", "0000000000000000")
    page.click("#recharge-btn")
    expect(page.locator("#message")).to_have_text("Payment failed. Please try another card")


def test_invalid_card_number(page):
    open_recharge_page(page)
    page.fill("#recharge-mobile", "9876543210")
    page.fill("#card-number", "123")
    page.click("#recharge-btn")
    expect(page.locator("#message")).to_have_text("Invalid card number")


def test_letters_in_mobile_number(page):
    open_recharge_page(page)
    page.fill("#recharge-mobile", "98765abcde")
    page.fill("#card-number", "1111222233334444")
    page.click("#recharge-btn")
    expect(page.locator("#message")).to_have_text("Invalid mobile number")

    