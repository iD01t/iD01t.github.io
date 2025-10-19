from playwright.sync_api import sync_playwright
import time

def run_verification():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Increased timeout for the entire test
        page.set_default_timeout(60000)

        try:
            # Navigate to the local server URL
            page.goto("http://localhost:8000/blog/", wait_until="networkidle")
            print("Successfully navigated to the blog page.")

            # Wait for the blog posts to be loaded dynamically
            # This is a crucial step to ensure the JS has executed
            page.wait_for_selector(".blog-post", timeout=30000)
            print("Blog posts are visible.")

            # Wait for the category filter buttons to be dynamically populated
            # Check for a category that actually exists in posts.json, like "Programming"
            category_button_selector = "button[data-category='programming']"
            page.wait_for_selector(category_button_selector, timeout=30000)
            print("Category filter buttons are visible.")

            # Click the 'Programming' category filter
            page.click(category_button_selector)
            print("Clicked the 'Programming' category filter.")

            # Add a brief pause to allow the UI to update
            time.sleep(1)

            # Verify that only programming posts are visible
            posts = page.query_selector_all(".blog-post")
            print(f"Found {len(posts)} posts after filtering.")

            # Check if all visible posts have the 'Programming' category or related tags.
            # This is a more flexible check.
            all_match = True
            for post in posts:
                html_content = post.inner_html()
                # A simple check to see if text related to programming is in the card
                if 'programming' not in html_content.lower() and 'python' not in html_content.lower():
                    all_match = False
                    print(f"Post did not match filter: {post.inner_text()}")
                    break

            if all_match and len(posts) > 0:
                print("Verification successful: All visible posts are related to 'Programming'.")
            elif len(posts) == 0:
                raise Exception("Verification failed: No posts found after filtering for 'Programming'.")
            else:
                raise Exception("Verification failed: Not all visible posts were related to 'Programming'.")

            # Take a screenshot
            screenshot_path = "frontend_verification.png"
            page.screenshot(path=screenshot_path)
            print(f"Screenshot saved to {screenshot_path}")

        except Exception as e:
            print(f"An error occurred: {e}")
            # Take a screenshot on error for debugging
            page.screenshot(path="frontend_error.png")
            print("Error screenshot saved to frontend_error.png")
            raise  # Re-raise the exception to fail the script
        finally:
            browser.close()

if __name__ == "__main__":
    run_verification()
