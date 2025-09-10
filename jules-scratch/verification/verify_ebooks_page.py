from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    page.goto("http://localhost:8000/ebooks.html")

    # Wait for the grid to be populated
    page.wait_for_selector("#grid article")

    page.screenshot(path="jules-scratch/verification/ebooks_page.png")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)
