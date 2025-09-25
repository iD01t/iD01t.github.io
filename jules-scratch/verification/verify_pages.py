import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Listen for all console events and print them
        page.on("console", lambda msg: print(f"Browser Console: {msg.text}"))

        # Verify ebooks.html
        print("Navigating to ebooks.html...")
        await page.goto("http://localhost:8000/ebooks.html", wait_until="networkidle")
        try:
            await page.wait_for_selector("#ebooksGrid article", timeout=15000) # Increased timeout
            print("Ebooks page loaded successfully.")
            await page.screenshot(path="jules-scratch/verification/ebooks_page.png")
        except Exception as e:
            print(f"Error verifying ebooks.html: {e}")
            await page.screenshot(path="jules-scratch/verification/ebooks_error.png")

        # Verify audiobooks.html
        print("\nNavigating to audiobooks.html...")
        await page.goto("http://localhost:8000/audiobooks.html", wait_until="networkidle")
        try:
            await page.wait_for_selector("#audiobooksGrid article", timeout=15000) # Increased timeout
            print("Audiobooks page loaded successfully.")
            await page.screenshot(path="jules-scratch/verification/audiobooks_page.png")
        except Exception as e:
            print(f"Error verifying audiobooks.html: {e}")
            await page.screenshot(path="jules-scratch/verification/audiobooks_error.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())