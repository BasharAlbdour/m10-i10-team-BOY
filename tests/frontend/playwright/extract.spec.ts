import { test, expect } from '@playwright/test';

test('extract page renders and returns entities', async ({ page }) => {
  await page.goto('/extract');
  await expect(page.getByRole('heading', { name: /extract/i })).toBeVisible();

  await page.getByPlaceholder(/paste text/i).fill(
    'Add ginger and garlic to the wok over high heat.'
  );
  await page.getByRole('button', { name: /extract/i }).click();

  await expect(page.getByTestId('entity-span').first()).toBeVisible({ timeout: 15_000 });
});
