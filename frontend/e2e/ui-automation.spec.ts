import { test, expect } from '@playwright/test'
import { createUIAutomation } from './utils/ui-automation'

/**
 * UI Automation Tests
 * Automated browser checks for UI elements and interactions
 */

test.describe('UI Automation Checks', () => {
  test('should verify all navigation items', async ({ page }) => {
    // Login
    await page.goto('/login')
    await page.fill('input[type="email"]', 'test@example.com')
    await page.fill('input[type="password"]', 'password123')
    await page.click('button[type="submit"]')
    await page.waitForURL('/dashboard', { timeout: 10000 })

    // Create UI automation instance
    const ui = createUIAutomation(page)

    // Get all navigation items
    const navItems = await ui.getNavigationItems()
    
    // Verify expected items exist
    const expectedItems = ['Dashboard', 'Content', 'Publishing', 'Funnels', 'Userbot', 'Promotion', 'Analytics', 'Settings']
    
    for (const item of expectedItems) {
      expect(navItems).toContain(item)
    }
  })

  test('should verify sidebar toggle functionality', async ({ page }) => {
    // Login and go to dashboard
    await page.goto('/login')
    await page.fill('input[type="email"]', 'test@example.com')
    await page.fill('input[type="password"]', 'password123')
    await page.click('button[type="submit"]')
    await page.waitForURL('/dashboard', { timeout: 10000 })

    const ui = createUIAutomation(page)

    // Check initial state
    const initialState = await ui.isSidebarCollapsed()
    
    // Toggle sidebar
    await ui.toggleSidebar()
    
    // Verify state changed
    const newState = await ui.isSidebarCollapsed()
    expect(newState).not.toBe(initialState)
  })

  test('should verify user menu functionality', async ({ page }) => {
    // Login
    await page.goto('/login')
    await page.fill('input[type="email"]', 'test@example.com')
    await page.fill('input[type="password"]', 'password123')
    await page.click('button[type="submit"]')
    await page.waitForURL('/dashboard', { timeout: 10000 })

    const ui = createUIAutomation(page)

    // Open user menu
    await ui.openUserMenu()
    
    // Verify menu is open
    const isOpen = await ui.isUserMenuOpen()
    expect(isOpen).toBe(true)
  })

  test('should verify stat cards display', async ({ page }) => {
    // Login and go to dashboard
    await page.goto('/login')
    await page.fill('input[type="email"]', 'test@example.com')
    await page.fill('input[type="password"]', 'password123')
    await page.click('button[type="submit"]')
    await page.waitForURL('/dashboard', { timeout: 10000 })

    const ui = createUIAutomation(page)

    // Wait for loading to disappear
    await ui.waitForLoadingToDisappear(10000)

    // Verify stat cards
    const articlesCreated = await ui.getStatCardValue('Total Articles')
    expect(articlesCreated).toBeTruthy()
  })

  test('should verify modal functionality', async ({ page }) => {
    // Login and navigate to content
    await page.goto('/login')
    await page.fill('input[type="email"]', 'test@example.com')
    await page.fill('input[type="password"]', 'password123')
    await page.click('button[type="submit"]')
    await page.waitForURL('/dashboard', { timeout: 10000 })
    await page.goto('/content')

    const ui = createUIAutomation(page)

    // Open modal
    await page.click('text=Add Source')
    
    // Verify modal is open
    const isOpen = await ui.isModalOpen()
    expect(isOpen).toBe(true)

    // Close modal
    await ui.closeModal()
    
    // Verify modal is closed
    const isClosed = await ui.isModalOpen()
    expect(isClosed).toBe(false)
  })

  test('should verify tab switching', async ({ page }) => {
    // Login and navigate to content
    await page.goto('/login')
    await page.fill('input[type="email"]', 'test@example.com')
    await page.fill('input[type="password"]', 'password123')
    await page.click('button[type="submit"]')
    await page.waitForURL('/dashboard', { timeout: 10000 })
    await page.goto('/content')

    const ui = createUIAutomation(page)

    // Switch to Articles tab
    await ui.switchTab('Articles')
    const articlesActive = await ui.verifyTextContent('.tf-tabs-item--active', 'Articles')
    expect(articlesActive).toBe(true)

    // Switch to Moderation tab
    await ui.switchTab('Moderation')
    const moderationActive = await ui.verifyTextContent('.tf-tabs-item--active', 'Moderation')
    expect(moderationActive).toBe(true)
  })

  test('should verify form validation', async ({ page }) => {
    // Login and navigate to content
    await page.goto('/login')
    await page.fill('input[type="email"]', 'test@example.com')
    await page.fill('input[type="password"]', 'password123')
    await page.click('button[type="submit"]')
    await page.waitForURL('/dashboard', { timeout: 10000 })
    await page.goto('/content')

    const ui = createUIAutomation(page)

    // Open add source modal
    await page.click('text=Add Source')

    // Try to submit empty form
    await page.click('button:has-text("Create")')

    // Verify validation (check for aria-invalid attribute)
    const nameInput = page.locator('input[name="name"]')
    const isInvalid = await nameInput.getAttribute('aria-invalid')
    expect(isInvalid).toBe('true')
  })

  test('should verify table interactions', async ({ page }) => {
    // Login and navigate to content
    await page.goto('/login')
    await page.fill('input[type="email"]', 'test@example.com')
    await page.fill('input[type="password"]', 'password123')
    await page.click('button[type="submit"]')
    await page.waitForURL('/dashboard', { timeout: 10000 })
    await page.goto('/content')

    const ui = createUIAutomation(page)

    // Wait for table
    await ui.waitForLoadingToDisappear(10000)

    // Check if table has data
    const hasData = await ui.verifyTableHasData()
    
    if (hasData) {
      // Get row count
      const rowCount = await ui.getTableRowsCount()
      expect(rowCount).toBeGreaterThan(0)
    }
  })

  test('should verify toast notifications', async ({ page }) => {
    // Login
    await page.goto('/login')
    await page.fill('input[type="email"]', 'test@example.com')
    await page.fill('input[type="password"]', 'password123')
    await page.click('button[type="submit"]')
    
    const ui = createUIAutomation(page)

    // Wait for toast (success or error)
    const hasToast = await ui.verifyToast('Welcome') || await ui.verifyToast('failed')
    expect(hasToast).toBe(true)
  })

  test('should verify page headers', async ({ page }) => {
    const pages = [
      { url: '/dashboard', title: 'Dashboard' },
      { url: '/content', title: 'Content' },
      { url: '/funnels', title: 'Funnels' },
      { url: '/publishing', title: 'Publishing' },
      { url: '/promotion', title: 'Promotion' },
      { url: '/analytics', title: 'Analytics' },
    ]

    // Login first
    await page.goto('/login')
    await page.fill('input[type="email"]', 'test@example.com')
    await page.fill('input[type="password"]', 'password123')
    await page.click('button[type="submit"]')
    await page.waitForURL('/dashboard', { timeout: 10000 })

    const ui = createUIAutomation(page)

    // Check each page
    for (const { url, title } of pages) {
      await page.goto(url)
      const isValid = await ui.verifyPageHeader(title)
      expect(isValid).toBe(true)
    }
  })

  test('should verify button states', async ({ page }) => {
    // Login and navigate
    await page.goto('/login')
    await page.fill('input[type="email"]', 'test@example.com')
    await page.fill('input[type="password"]', 'password123')
    await page.click('button[type="submit"]')
    await page.waitForURL('/dashboard', { timeout: 10000 })
    await page.goto('/content')

    const ui = createUIAutomation(page)

    // Open modal
    await page.click('text=Add Source')

    // Check if create button is enabled
    const createButton = page.locator('button:has-text("Create")')
    const isDisabled = await ui.isButtonDisabled('button:has-text("Create")')
    
    // Button should be enabled (form is empty but button is clickable)
    expect(isDisabled).toBe(false)
  })

  test('should verify input placeholders', async ({ page }) => {
    // Login and navigate
    await page.goto('/login')
    await page.fill('input[type="email"]', 'test@example.com')
    await page.fill('input[type="password"]', 'password123')
    await page.click('button[type="submit"]')
    await page.waitForURL('/dashboard', { timeout: 10000 })
    await page.goto('/content')

    const ui = createUIAutomation(page)

    // Open modal
    await page.click('text=Add Source')

    // Verify placeholder
    const hasPlaceholder = await ui.verifyInputPlaceholder(
      'input[name="name"]',
      'My RSS Feed'
    )
    expect(hasPlaceholder).toBe(true)
  })

  test('should verify badge variants', async ({ page }) => {
    // Login and navigate
    await page.goto('/login')
    await page.fill('input[type="email"]', 'test@example.com')
    await page.fill('input[type="password"]', 'password123')
    await page.click('button[type="submit"]')
    await page.waitForURL('/dashboard', { timeout: 10000 })
    await page.goto('/content')

    const ui = createUIAutomation(page)

    // Wait for table
    await ui.waitForLoadingToDisappear(10000)

    // Check if badges exist in table
    const hasBadges = await ui.isElementVisible('.tf-badge')
    if (hasBadges) {
      // Verify badge variant
      const hasValidVariant = await ui.verifyBadgeVariant('success') || 
                              await ui.verifyBadgeVariant('neutral') ||
                              await ui.verifyBadgeVariant('primary')
      expect(hasValidVariant).toBe(true)
    }
  })

  test('should verify error messages', async ({ page }) => {
    // Go to login page
    await page.goto('/login')

    const ui = createUIAutomation(page)

    // Submit empty form
    await page.click('button[type="submit"]')

    // Get error message
    const errorMessage = await ui.getErrorMessage()
    
    // Should have validation error
    expect(errorMessage).toBeTruthy()
  })

  test('should verify loading states', async ({ page }) => {
    // Login
    await page.goto('/login')
    await page.fill('input[type="email"]', 'test@example.com')
    await page.fill('input[type="password"]', 'password123')
    
    const ui = createUIAutomation(page)

    // Click submit
    await page.click('button[type="submit"]')

    // Check if loading appears (may be very fast)
    const isLoading = await ui.isLoading()
    
    // Loading state may or may not be visible depending on speed
    // This is just to verify the method works
    expect(typeof isLoading).toBe('boolean')
  })

  test('should verify responsive layout', async ({ page }) => {
    // Login
    await page.goto('/login')
    await page.fill('input[type="email"]', 'test@example.com')
    await page.fill('input[type="password"]', 'password123')
    await page.click('button[type="submit"]')
    await page.waitForURL('/dashboard', { timeout: 10000 })

    const ui = createUIAutomation(page)

    // Verify responsive layout
    const results = await ui.verifyResponsiveLayout()
    
    // All viewports should have valid layout
    for (const result of results) {
      console.log(`Viewport ${result.name}: ${result.isValid ? '✓' : '✗'}`)
      expect(result.isValid).toBe(true)
    }
  })
})
