import { test, expect } from '@playwright/test';

test('rag page renders cited answer', async ({ page }) => {
  await page.goto('/rag');
  await expect(page.getByRole('heading', { name: /rag/i })).toBeVisible();

  await page.getByPlaceholder(/recipe question/i).fill(
    'How do I prep ginger for stir-fry?'
  );
  await page.getByRole('button', { name: /ask/i }).click();

  await expect(page.getByTestId('rag-answer')).toBeVisible({ timeout: 30_000 });
  await expect(page.getByTestId('citation-marker').first()).toBeVisible();
});
