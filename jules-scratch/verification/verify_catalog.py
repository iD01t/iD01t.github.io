
from playwright.sync_api import sync_playwright, expect

def run_verification():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # 1. Verify eBooks Page
        print("Navigating to eBooks page...")
        page.goto("http://localhost:8000/ebooks.html")

        # Wait for the catalog grid to have at least one book card visible.
        catalog_grid = page.locator("#catalogGrid")
        expect(catalog_grid.locator("article").first).to_be_visible(timeout=10000)

        print("eBooks page loaded. Taking screenshot...")
        page.screenshot(path="jules-scratch/verification/ebooks_page.png")

        # 2. Verify Audiobooks Page (Empty State)
        print("Navigating to Audiobooks page...")
        page.goto("http://localhost:8000/audiobooks.html")

        # Wait for the "No Audiobooks found" message.
        result_count = page.locator("#resultCount")
        expect(result_count).to_contain_text("0 Audiobooks found")

        print("Audiobooks page (empty state) loaded. Taking screenshot...")
        page.screenshot(path="jules-scratch/verification/audiobooks_page_empty.png")

        # 3. Verify Book Detail Page
        print("Navigating back to eBooks page to select a book...")
        page.goto("http://localhost:8000/ebooks.html")

        # Wait for the grid and click the first book.
        expect(catalog_grid.locator("article").first).to_be_visible(timeout=10000)
        first_book = catalog_grid.locator("article").first
        first_book.click()

        # Wait for the detail page to load by checking for the title.
        detail_container = page.locator("#detailContainer")
        expect(detail_container.locator("h1")).not_to_be_empty(timeout=10000)

        print("Book detail page loaded. Taking screenshot...")
        page.screenshot(path="jules-scratch/verification/book_detail_page.png")

        browser.close()
        print("Verification complete. Screenshots saved.")

if __name__ == "__main__":
    run_verification()
