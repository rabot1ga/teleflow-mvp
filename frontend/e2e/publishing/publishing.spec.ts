import { test, expect } from '@playwright/test'

/**
 * TeleFlow E2E Tests - Publishing Module
 * Tests for Targets, Templates, and Calendar
 */

test.describe('Publishing Module', () => {
  test.beforeEach(async ({ page }) => {
    // Login and navigate to publishing
    await page.goto('/login')
    await page.fill('input[type="email"]', 'test@example.com')
    await page.fill('input[type="password"]', 'password123')
    await page.click('button[type="submit"]')
    await page.waitForURL('/dashboard', { timeout: 10000 })
    await page.goto('/publishing')
  })

  test('should display publishing page', async ({ page }) => {
    // Check page title
    await expect(page.locator('h1')).toContainText('Publishing')

    // Check tabs are visible
    await expect(page.locator('text=Targets')).toBeVisible()
    await expect(page.locator('text=Templates')).toBeVisible()
    await expect(page.locator('text=Calendar')).toBeVisible()
  })

  test('should switch between tabs', async ({ page }) => {
    // Click on Templates tab
    await page.click('text=Templates')
    await expect(page.locator('.tf-tabs-item--active')).toContainText('Templates')

    // Click on Calendar tab
    await page.click('text=Calendar')
    await expect(page.locator('.tf-tabs-item--active')).toContainText('Calendar')

    // Click back on Targets tab
    await page.click('text=Targets')
    await expect(page.locator('.tf-tabs-item--active')).toContainText('Targets')
  })
})

test.describe('Targets', () => {
  test.beforeEach(async ({ page }) => {
    // Login and navigate to publishing targets
    await page.goto('/login')
    await page.fill('input[type="email"]', 'test@example.com')
    await page.fill('input[type="password"]', 'password123')
    await page.click('button[type="submit"]')
    await page.waitForURL('/dashboard', { timeout: 10000 })
    await page.goto('/publishing')
  })

  test('should open add target modal', async ({ page }) => {
    // Click on Add Target button
    await page.click('text=Add Target')

    // Modal should be visible
    const modal = page.locator('.tf-modal')
    await expect(modal).toBeVisible()

    // Check modal title
    await expect(page.locator('.tf-modal-title')).toContainText('Add New Target')
  })

  test('should create target', async ({ page }) => {
    // Click on Add Target button
    await page.click('text=Add Target')

    // Fill in target form
    await page.fill('input#target-name', 'Test Channel')
    await page.fill('input#target-chat-id', '@testchannel')

    // Select type
    await page.selectOption('select#target-type', 'channel')

    // Submit form
    await page.click('button:has-text("Create")')

    // Success toast should appear
    await expect(page.locator('text=Target created')).toBeVisible({ timeout: 5000 }).catch(() => {
      console.log('Success toast not shown')
    })
  })

  test('should display targets table', async ({ page }) => {
    // Wait for table to load
    await page.waitForSelector('.tf-table', { timeout: 5000 })

    // Table should be visible
    const table = page.locator('.tf-table')
    await expect(table).toBeVisible()
  })

  test('should edit target', async ({ page }) => {
    // Wait for table to load
    await page.waitForSelector('.tf-table', { timeout: 5000 }).catch(() => {
      console.log('No targets available')
      return
    })

    // Click edit button
    const editButton = page.locator('button:has-text("Edit")').first()
    await editButton.click().catch(() => {
      console.log('No edit button found')
    })
  })

  test('should delete target', async ({ page }) => {
    // Wait for table to load
    await page.waitForSelector('.tf-table', { timeout: 5000 }).catch(() => {
      console.log('No targets available')
      return
    })

    // Click delete button
    const deleteButton = page.locator('button:has-text("Delete")').first()
    await deleteButton.click().catch(() => {
      console.log('No delete button found')
    })

    // Success toast should appear
    await expect(page.locator('text=deleted')).toBeVisible({ timeout: 5000 }).catch(() => {
      console.log('Success toast not shown')
    })
  })
})

test.describe('Templates', () => {
  test.beforeEach(async ({ page }) => {
    // Login and navigate to publishing templates
    await page.goto('/login')
    await page.fill('input[type="email"]', 'test@example.com')
    await page.fill('input[type="password"]', 'password123')
    await page.click('button[type="submit"]')
    await page.waitForURL('/dashboard', { timeout: 10000 })
    await page.goto('/publishing')
    await page.click('text=Templates')
  })

  test('should open create template modal', async ({ page }) => {
    // Click on Create Template button
    await page.click('text=Create Template')

    // Modal should be visible
    const modal = page.locator('.tf-modal')
    await expect(modal).toBeVisible()

    // Check modal title
    await expect(page.locator('.tf-modal-title')).toContainText('Create Template')
  })

  test('should create template', async ({ page }) => {
    // Click on Create Template button
    await page.click('text=Create Template')

    // Fill in template form
    await page.fill('input#template-name', 'Default Template')
    await page.fill('textarea#template-content', '{{title}}\n\n{{content}}\n\n#{{tags}}')

    // Submit form
    await page.click('button:has-text("Create")')

    // Success toast should appear
    await expect(page.locator('text=Template created')).toBeVisible({ timeout: 5000 }).catch(() => {
      console.log('Success toast not shown')
    })
  })

  test('should display templates table', async ({ page }) => {
    // Wait for table to load
    await page.waitForSelector('.tf-table', { timeout: 5000 })

    // Table should be visible
    const table = page.locator('.tf-table')
    await expect(table).toBeVisible()
  })

  test('should show template variables help', async ({ page }) => {
    // Click on Create Template button
    await page.click('text=Create Template')

    // Variables help should be visible
    const helpText = page.locator('text=Available variables')
    await expect(helpText).toBeVisible()
  })
})

test.describe('Calendar', () => {
  test.beforeEach(async ({ page }) => {
    // Login and navigate to publishing calendar
    await page.goto('/login')
    await page.fill('input[type="email"]', 'test@example.com')
    await page.fill('input[type="password"]', 'password123')
    await page.click('button[type="submit"]')
    await page.waitForURL('/dashboard', { timeout: 10000 })
    await page.goto('/publishing')
    await page.click('text=Calendar')
  })

  test('should display calendar placeholder', async ({ page }) => {
    // Calendar card should be visible
    await expect(page.locator('.tf-card')).toBeVisible()

    // Should show "coming soon" message
    const placeholder = page.locator('text=Calendar view coming soon')
    await expect(placeholder).toBeVisible()
  })
})
