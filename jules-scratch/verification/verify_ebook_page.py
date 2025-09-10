from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    page.goto("http://localhost:8000/ebook.html?slug=chess-mastery")

    # Wait for the page to be fully loaded
    page.wait_for_load_state('networkidle')

    page.screenshot(path="jules-scratch/verification/ebook_page.png")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)
