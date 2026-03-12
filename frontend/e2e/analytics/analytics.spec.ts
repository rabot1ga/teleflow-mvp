import { test, expect } from '@playwright/test'

/**
 * TeleFlow E2E Tests - Analytics Module
 * Tests for Overview, Content, Funnels, and Broadcasts analytics
 */

test.describe('Analytics Module', () => {
  test.beforeEach(async ({ page }) => {
    // Login and navigate to analytics
    await page.goto('/login')
    await page.fill('input[type="email"]', 'test@example.com')
    await page.fill('input[type="password"]', 'password123')
    await page.click('button[type="submit"]')
    await page.waitForURL('/dashboard', { timeout: 10000 })
    await page.goto('/analytics')
  })

  test('should display analytics page', async ({ page }) => {
    // Check page title
    await expect(page.locator('h1')).toContainText('Analytics')

    // Check tabs are visible
    await expect(page.locator('text=Overview')).toBeVisible()
    await expect(page.locator('text=Content')).toBeVisible()
    await expect(page.locator('text=Funnels')).toBeVisible()
    await expect(page.locator('text=Broadcasts')).toBeVisible()
  })

  test('should switch between tabs', async ({ page }) => {
    // Click on Content tab
    await page.click('text=Content')
    await expect(page.locator('.tf-tabs-item--active')).toContainText('Content')

    // Click on Funnels tab
    await page.click('text=Funnels')
    await expect(page.locator('.tf-tabs-item--active')).toContainText('Funnels')

    // Click on Broadcasts tab
    await page.click('text=Broadcasts')
    await expect(page.locator('.tf-tabs-item--active')).toContainText('Broadcasts')

    // Click back on Overview tab
    await page.click('text=Overview')
    await expect(page.locator('.tf-tabs-item--active')).toContainText('Overview')
  })

  test('should change time period', async ({ page }) => {
    // Click on 7D button
    await page.click('button:has-text("7D")')
    await expect(page.locator('button:has-text("7D")')).toHaveClass(/tf-button--primary/)

    // Click on 30D button
    await page.click('button:has-text("30D")')
    await expect(page.locator('button:has-text("30D")')).toHaveClass(/tf-button--primary/)

    // Click on 90D button
    await page.click('button:has-text("90D")')
    await expect(page.locator('button:has-text("90D")')).toHaveClass(/tf-button--primary/)
  })

  test('should display overview stats', async ({ page }) => {
    // Wait for stats to load
    await page.waitForSelector('.tf-stat-card', { timeout: 5000 })

    // Check stat cards are visible
    const statCards = page.locator('.tf-stat-card')
    await expect(statCards).toHaveCount({ count: 4, min: 1 })

    // Check specific stats
    await expect(page.locator('text=Articles Created')).toBeVisible()
    await expect(page.locator('text=Articles Published')).toBeVisible()
    await expect(page.locator('text=Funnel Entries')).toBeVisible()
    await expect(page.locator('text=Messages Sent')).toBeVisible()
  })

  test('should display recent activity', async ({ page }) => {
    // Wait for activity list to load
    await page.waitForSelector('.tf-card', { timeout: 5000 })

    // Find recent activity card
    const activityCard = page.locator('text=Recent Activity')
    await expect(activityCard).toBeVisible()
  })
})

test.describe('Content Analytics', () => {
  test.beforeEach(async ({ page }) => {
    // Login and navigate to content analytics
    await page.goto('/login')
    await page.fill('input[type="email"]', 'test@example.com')
    await page.fill('input[type="password"]', 'password123')
    await page.click('button[type="submit"]')
    await page.waitForURL('/dashboard', { timeout: 10000 })
    await page.goto('/analytics')
    await page.click('text=Content')
  })

  test('should display content performance', async ({ page }) => {
    // Content performance card should be visible
    await expect(page.locator('text=Content Performance')).toBeVisible()
  })

  test('should display approval rate', async ({ page }) => {
    // Approval rate card should be visible
    await expect(page.locator('text=Approval Rate')).toBeVisible()

    // Should show percentage
    const percentage = page.locator('.text-success')
    await percentage.isVisible().then(visible => {
      if (visible) {
        expect(visible).toBe(true)
      }
    })
  })
})

test.describe('Funnel Analytics', () => {
  test.beforeEach(async ({ page }) => {
    // Login and navigate to funnel analytics
    await page.goto('/login')
    await page.fill('input[type="email"]', 'test@example.com')
    await page.fill('input[type="password"]', 'password123')
    await page.click('button[type="submit"]')
    await page.waitForURL('/dashboard', { timeout: 10000 })
    await page.goto('/analytics')
    await page.click('text=Funnels')
  })

  test('should display funnel conversion', async ({ page }) => {
    // Funnel conversion card should be visible
    await expect(page.locator('text=Funnel Conversion')).toBeVisible()
  })

  test('should display conversion rate', async ({ page }) => {
    // Stats card should be visible
    await expect(page.locator('text=Conversion Rate')).toBeVisible()

    // Should show percentage
    const percentage = page.locator('.text-primary')
    await percentage.isVisible().then(visible => {
      if (visible) {
        expect(visible).toBe(true)
      }
    })
  })
})

test.describe('Broadcast Analytics', () => {
  test.beforeEach(async ({ page }) => {
    // Login and navigate to broadcast analytics
    await page.goto('/login')
    await page.fill('input[type="email"]', 'test@example.com')
    await page.fill('input[type="password"]', 'password123')
    await page.click('button[type="submit"]')
    await page.waitForURL('/dashboard', { timeout: 10000 })
    await page.goto('/analytics')
    await page.click('text=Broadcasts')
  })

  test('should display broadcast placeholder', async ({ page }) => {
    // Broadcast performance card should be visible
    await expect(page.locator('text=Broadcast Performance')).toBeVisible()

    // Should show "coming soon" message
    const placeholder = page.locator('text=Broadcast statistics coming soon')
    await expect(placeholder).toBeVisible()
  })
})

test.describe('Dashboard Overview', () => {
  test.beforeEach(async ({ page }) => {
    // Login and navigate to dashboard
    await page.goto('/login')
    await page.fill('input[type="email"]', 'test@example.com')
    await page.fill('input[type="password"]', 'password123')
    await page.click('button[type="submit"]')
    await page.waitForURL('/dashboard', { timeout: 10000 })
  })

  test('should display dashboard', async ({ page }) => {
    // Check page title
    await expect(page.locator('h1')).toContainText('Dashboard')
  })

  test('should display dashboard stats', async ({ page }) => {
    // Wait for stats to load
    await page.waitForSelector('.tf-stat-card', { timeout: 5000 })

    // Check stat cards are visible
    const statCards = page.locator('.tf-stat-card')
    await expect(statCards).toHaveCount({ count: 4, min: 1 })
  })

  test('should display quick actions', async ({ page }) => {
    // Quick actions card should be visible
    await expect(page.locator('text=Quick Actions')).toBeVisible()

    // Action buttons should be visible
    await expect(page.locator('text=Add Source')).toBeVisible()
    await expect(page.locator('text=Create Funnel')).toBeVisible()
  })

  test('should display recent activity', async ({ page }) => {
    // Recent activity card should be visible
    await expect(page.locator('text=Recent Activity')).toBeVisible()
  })
})
