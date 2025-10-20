
from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch()
    page = browser.new_page()

    # Create a directory for the screenshots if it doesn't exist
    import os
    os.makedirs("jules-scratch/verification", exist_ok=True)

    # Verify index page
    page.goto("http://localhost:8000/index.html")
    page.wait_for_selector("text='DJ iD01t New Album Available Now!'")
    page.screenshot(path="jules-scratch/verification/index.png")

    # Verify music page
    page.goto("http://localhost:8000/music.html")
    page.wait_for_selector("text='DJ iD01t New Album Available Now!'")
    page.screenshot(path="jules-scratch/verification/music.png")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)
