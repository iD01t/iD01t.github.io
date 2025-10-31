from playwright.sync_api import Page, expect
import os

def test_book_page_verification(page: Page):
    """
    This test verifies that the landing-enhancer.js script is injected correctly.
    """
    # 1. Arrange: Go to the book.html page with a book ID.
    page.goto(f"file://{os.getcwd()}/book.html?id=NT1UEQAAQBAJ")

    # 2. Assert: Confirm that the landing-enhancer.js script is present.
    script_tag = page.locator('script[src="/assets/js/landing-enhancer.js"]')
    expect(script_tag).to_be_visible()

    # 3. Screenshot: Capture the final result for visual verification.
    page.screenshot(path="jules-scratch/verification/book-page.png")
