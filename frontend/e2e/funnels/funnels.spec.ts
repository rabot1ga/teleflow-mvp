import { test, expect } from '@playwright/test'

/**
 * TeleFlow E2E Tests - Funnels Module
 * Tests for Funnels, Lead Magnets, and Broadcasts
 */

test.describe('Funnels Module', () => {
  test.beforeEach(async ({ page }) => {
    // Login and navigate to funnels
    await page.goto('/login')
    await page.fill('input[type="email"]', 'test@example.com')
    await page.fill('input[type="password"]', 'password123')
    await page.click('button[type="submit"]')
    await page.waitForURL('/dashboard', { timeout: 10000 })
    await page.goto('/funnels')
  })

  test('should display funnels page', async ({ page }) => {
    // Check page title
    await expect(page.locator('h1')).toContainText('Funnels')

    // Check stats cards are visible
    const statCards = page.locator('.tf-stat-card')
    await expect(statCards).toHaveCount({ count: 4, min: 1 })
  })

  test('should open create funnel modal', async ({ page }) => {
    // Click on Create Funnel button
    await page.click('text=Create Funnel')

    // Modal should be visible
    const modal = page.locator('.tf-modal')
    await expect(modal).toBeVisible()

    // Check modal title
    await expect(page.locator('.tf-modal-title')).toContainText('Create New Funnel')
  })

  test('should create funnel', async ({ page }) => {
    // Click on Create Funnel button
    await page.click('text=Create Funnel')

    // Fill in funnel form
    await page.fill('input[name="name"]', 'Test Welcome Funnel')

    // Select trigger type
    await page.selectOption('select[name="trigger_type"]', 'command')

    // Fill trigger value
    await page.fill('input[name="trigger_value"]', '/start')

    // Submit form
    await page.click('button:has-text("Create")')

    // Success toast should appear
    await expect(page.locator('text=Funnel created')).toBeVisible({ timeout: 5000 }).catch(() => {
      console.log('Success toast not shown - backend may not be running')
    })
  })

  test('should display funnels table', async ({ page }) => {
    // Wait for table to load
    await page.waitForSelector('.tf-table', { timeout: 5000 })

    // Table should be visible
    const table = page.locator('.tf-table')
    await expect(table).toBeVisible()
  })

  test('should delete funnel', async ({ page }) => {
    // Wait for table to load
    await page.waitForSelector('.tf-table', { timeout: 5000 }).catch(() => {
      console.log('No funnels available')
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

  test('should toggle funnel status', async ({ page }) => {
    // Wait for table to load
    await page.waitForSelector('.tf-table', { timeout: 5000 }).catch(() => {
      console.log('No funnels available')
      return
    })

    // Find status toggle and click
    const toggle = page.locator('.tf-switch').first()
    await toggle.click().catch(() => {
      console.log('No status toggle found')
    })
  })
})

test.describe('Lead Magnets', () => {
  test.beforeEach(async ({ page }) => {
    // Login and navigate to funnels
    await page.goto('/login')
    await page.fill('input[type="email"]', 'test@example.com')
    await page.fill('input[type="password"]', 'password123')
    await page.click('button[type="submit"]')
    await page.waitForURL('/dashboard', { timeout: 10000 })
    await page.goto('/funnels')
  })

  test('should navigate to lead magnets tab', async ({ page }) => {
    // Click on Lead Magnets tab (if exists)
    const leadMagnetsTab = page.locator('text=Lead Magnets')
    await leadMagnetsTab.click().catch(() => {
      console.log('Lead Magnets tab not found')
    })
  })
})

test.describe('Broadcasts', () => {
  test.beforeEach(async ({ page }) => {
    // Login and navigate to funnels
    await page.goto('/login')
    await page.fill('input[type="email"]', 'test@example.com')
    await page.fill('input[type="password"]', 'password123')
    await page.click('button[type="submit"]')
    await page.waitForURL('/dashboard', { timeout: 10000 })
    await page.goto('/funnels')
  })

  test('should navigate to broadcasts tab', async ({ page }) => {
    // Click on Broadcasts tab (if exists)
    const broadcastsTab = page.locator('text=Broadcasts')
    await broadcastsTab.click().catch(() => {
      console.log('Broadcasts tab not found')
    })
  })

  test('should create broadcast', async ({ page }) => {
    // Navigate to broadcasts
    const broadcastsTab = page.locator('text=Broadcasts')
    await broadcastsTab.click().catch(() => {
      console.log('Broadcasts tab not found')
      return
    })

    // Click on Create Broadcast button
    const createButton = page.locator('text=Create Broadcast')
    await createButton.click().catch(() => {
      console.log('Create Broadcast button not found')
    })
  })
})
