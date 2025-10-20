
from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch()
    page = browser.new_page()

    # Create a directory for the screenshots if it doesn't exist
    import os
    os.makedirs("jules-scratch/verification", exist_ok=True)


    # Verify ebooks page
    page.goto("http://localhost:8000/ebooks.html")
    page.wait_for_selector("#catalogGrid .card-hover")
    page.screenshot(path="jules-scratch/verification/ebooks.png")

    # Verify audiobooks page
    page.goto("http://localhost:8000/audiobooks.html")
    page.screenshot(path="jules-scratch/verification/audiobooks.png")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)
