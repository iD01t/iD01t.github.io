import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Listen for console events
        page.on('console', lambda msg: print(f"Browser console: {msg.text()}"))

        # Verify ebooks page
        await page.goto('http://localhost:8000/ebooks.html')
        try:
            await page.wait_for_selector('#catalogGrid .catalog-card', timeout=10000)
            await page.screenshot(path='jules-scratch/verification/ebooks-fixed.png')
            print("Ebooks page verified successfully.")
        except Exception as e:
            print(f"Error verifying ebooks page: {e}")
            await page.screenshot(path='jules-scratch/verification/ebooks-error.png')


        # Verify audiobooks page
        await page.goto('http://localhost:8000/audiobooks.html')
        try:
            await page.wait_for_selector('#catalogGrid')
            await page.screenshot(path='jules-scratch/verification/audiobooks-fixed.png')
            print("Audiobooks page verified successfully.")
        except Exception as e:
            print(f"Error verifying audiobooks page: {e}")
            await page.screenshot(path='jules-scratch/verification/audiobooks-error.png')


        await browser.close()

asyncio.run(main())
