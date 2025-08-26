import { test, expect } from '@playwright/test';

test.describe('Core Navigation Flow', () => {
  test('should navigate from home to the first product page', async ({ page }) => {
    // 1. Start at the Home page
    await page.goto('/');

    // 2. Find the first product card and get its title
    const firstProductCard = page.locator('a[href^="/products/"]').first();
    await expect(firstProductCard).toBeVisible();
    const productTitle = await firstProductCard.locator('h3').innerText();

    // 3. Click the product card
    await firstProductCard.click();

    // 4. Verify the URL has changed to a product page
    await expect(page).toHaveURL(/.*\/products\/.+/);

    // 5. Verify the h1 on the product page matches the title from the card
    const pageTitle = page.locator('h1');
    await expect(pageTitle).toHaveText(productTitle);
  });

  test('should navigate to the catalog page from the header', async ({ page }) => {
    await page.goto('/');

    // Find and click the "Catalog" link in the header
    await page.getByRole('link', { name: 'Catalog' }).click();

    // Verify the URL and the page title
    await expect(page).toHaveURL(/.*\/catalog/);
    await expect(page.locator('h1')).toHaveText('Product Catalog');
  });
});
