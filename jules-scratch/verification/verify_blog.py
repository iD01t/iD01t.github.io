from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch()
    page = browser.new_page()
    page.goto("http://localhost:8000/blog/")

    # Wait for the initial posts to load
    page.wait_for_selector(".blog-post")

    # Verify initial posts are visible
    initial_posts = page.query_selector_all(".blog-post")
    assert len(initial_posts) > 0, "No blog posts were loaded on the page."

    # Take a screenshot of the initial state of the blog page
    page.screenshot(path="jules-scratch/verification/blog_initial_state.png")

    # Test category filtering
    # Wait for category buttons to be dynamically created
    page.wait_for_selector("button[data-category='Technology']")

    # Click on the 'Technology' category filter
    page.click("button[data-category='Technology']")
    page.wait_for_timeout(500) # Wait for filtering to apply

    # Verify that only 'Technology' posts are visible
    filtered_posts = page.query_selector_all(".blog-post")
    for post in filtered_posts:
        category = post.query_selector(".text-gray-500").inner_text()
        assert "Technology" in category, "Category filter is not working correctly."

    # Take a screenshot of the filtered state
    page.screenshot(path="jules-scratch/verification/blog_filtered_state.png")

    # Test "Load More Articles" button
    # First, reset the filter to show all posts
    page.click("button[data-category='All']")
    page.wait_for_timeout(500)

    # Click the "Load More Articles" button
    load_more_button = page.query_selector("#load-more")
    if load_more_button:
        load_more_button.click()
        page.wait_for_timeout(1000) # Wait for more posts to load

    # Verify that more posts are now visible
    all_posts = page.query_selector_all(".blog-post")
    assert len(all_posts) > len(initial_posts), "Load More button did not load more articles."

    # Take the final screenshot
    page.screenshot(path="jules-scratch/verification/verification.png")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)
