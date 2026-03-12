import { Page, Locator, expect } from '@playwright/test'

/**
 * TeleFlow UI Automation Helpers
 * Common utilities for browser automation and UI validation
 */

export class UIAutomation {
  constructor(private page: Page) {}

  /**
   * Wait for page to be fully loaded
   */
  async waitForPageLoad() {
    await this.page.waitForLoadState('networkidle')
    await this.page.waitForLoadState('domcontentloaded')
  }

  /**
   * Check if element is visible
   */
  async isElementVisible(selector: string): Promise<boolean> {
    try {
      const element = this.page.locator(selector)
      await element.waitFor({ state: 'visible', timeout: 5000 })
      return true
    } catch {
      return false
    }
  }

  /**
   * Check if element contains expected text
   */
  async verifyTextContent(selector: string, expectedText: string): Promise<boolean> {
    try {
      const element = this.page.locator(selector)
      await element.waitFor({ state: 'visible', timeout: 5000 })
      const text = await element.textContent()
      return text?.includes(expectedText) ?? false
    } catch {
      return false
    }
  }

  /**
   * Validate form field
   */
  async validateFormField(inputSelector: string, errorSelector: string): Promise<boolean> {
    try {
      const input = this.page.locator(inputSelector)
      await input.fill('')
      await input.blur()
      
      const error = this.page.locator(errorSelector)
      await error.waitFor({ state: 'visible', timeout: 3000 })
      return true
    } catch {
      return false
    }
  }

  /**
   * Fill form fields from object
   */
  async fillForm(fields: Record<string, string>) {
    for (const [selector, value] of Object.entries(fields)) {
      await this.page.fill(selector, value)
    }
  }

  /**
   * Submit form and wait for response
   */
  async submitFormAndWait(submitSelector: string, successSelector?: string, timeout = 5000) {
    await this.page.click(submitSelector)
    
    if (successSelector) {
      await this.page.waitForSelector(successSelector, { timeout })
    }
  }

  /**
   * Check modal is open
   */
  async isModalOpen(): Promise<boolean> {
    return this.isElementVisible('.tf-modal')
  }

  /**
   * Close modal
   */
  async closeModal() {
    const closeButton = this.page.locator('.tf-modal-close, button:has-text("Cancel")')
    await closeButton.click()
    await this.page.waitForSelector('.tf-modal', { state: 'hidden', timeout: 3000 })
  }

  /**
   * Switch tab by name
   */
  async switchTab(tabName: string) {
    await this.page.click(`text=${tabName}`)
    await this.page.waitForTimeout(500)
  }

  /**
   * Verify table has data
   */
  async verifyTableHasData(): Promise<boolean> {
    try {
      const table = this.page.locator('.tf-table')
      await table.waitFor({ state: 'visible', timeout: 5000 })
      
      const rows = table.locator('tbody tr')
      const count = await rows.count()
      return count > 0
    } catch {
      return false
    }
  }

  /**
   * Get table row count
   */
  async getTableRowsCount(): Promise<number> {
    const table = this.page.locator('.tf-table')
    const rows = table.locator('tbody tr')
    return await rows.count()
  }

  /**
   * Click table action button
   */
  async clickTableAction(actionText: string, rowIndex = 0) {
    const table = this.page.locator('.tf-table')
    const row = table.locator('tbody tr').nth(rowIndex)
    const button = row.locator(`button:has-text("${actionText}")`)
    await button.click()
  }

  /**
   * Verify toast notification
   */
  async verifyToast(message: string): Promise<boolean> {
    try {
      const toast = this.page.locator(`text=${message}`)
      await toast.waitFor({ state: 'visible', timeout: 5000 })
      return true
    } catch {
      return false
    }
  }

  /**
   * Wait for toast to appear
   */
  async waitForToast(message: string, timeout = 5000) {
    await this.page.waitForSelector(`text=${message}`, { timeout })
  }

  /**
   * Check page URL
   */
  async verifyURL(expectedURL: string): Promise<boolean> {
    const currentURL = this.page.url()
    return currentURL.includes(expectedURL)
  }

  /**
   * Navigate to section
   */
  async navigateToSection(section: string) {
    const navLink = this.page.locator(`.sidebar__link:has-text("${section}")`)
    await navLink.click()
    await this.waitForPageLoad()
  }

  /**
   * Get all navigation items
   */
  async getNavigationItems(): Promise<string[]> {
    const items = this.page.locator('.sidebar__link-label')
    const count = await items.count()
    const labels: string[] = []
    
    for (let i = 0; i < count; i++) {
      const text = await items.nth(i).textContent()
      if (text) labels.push(text.trim())
    }
    
    return labels
  }

  /**
   * Verify sidebar is collapsed/expanded
   */
  async isSidebarCollapsed(): Promise<boolean> {
    const sidebar = this.page.locator('.sidebar')
    const classes = await sidebar.getAttribute('class')
    return classes?.includes('sidebar--collapsed') ?? false
  }

  /**
   * Toggle sidebar
   */
  async toggleSidebar() {
    const toggle = this.page.locator('.sidebar__toggle, .main-header__toggle')
    await toggle.click()
    await this.page.waitForTimeout(300)
  }

  /**
   * Check user menu is open
   */
  async isUserMenuOpen(): Promise<boolean> {
    return this.isElementVisible('.user-menu__dropdown')
  }

  /**
   * Open user menu
   */
  async openUserMenu() {
    await this.page.click('.user-menu__trigger')
    await this.page.waitForTimeout(300)
  }

  /**
   * Get stat card value
   */
  async getStatCardValue(title: string): Promise<string> {
    const card = this.page.locator('.tf-stat-card', { hasText: title })
    const value = card.locator('.tf-stat-card__value')
    return await value.textContent() || ''
  }

  /**
   * Verify stat card trend
   */
  async verifyStatCardTrend(title: string, isPositive: boolean): Promise<boolean> {
    const card = this.page.locator('.tf-stat-card', { hasText: title })
    const trend = card.locator('.tf-stat-card__trend')
    const classes = await trend.getAttribute('class')
    
    if (isPositive) {
      return classes?.includes('tf-stat-card__trend--positive') ?? false
    } else {
      return classes?.includes('tf-stat-card__trend--negative') ?? false
    }
  }

  /**
   * Wait for loading state to disappear
   */
  async waitForLoadingToDisappear(timeout = 10000) {
    await this.page.waitForSelector('.tf-spinner, .tf-skeleton, .loading', { 
      state: 'hidden', 
      timeout 
    })
  }

  /**
   * Check if page is in loading state
   */
  async isLoading(): Promise<boolean> {
    const spinner = this.page.locator('.tf-spinner, .tf-skeleton')
    return await spinner.isVisible()
  }

  /**
   * Retry action until success
   */
  async retryAction(action: () => Promise<void>, maxRetries = 3) {
    for (let i = 0; i < maxRetries; i++) {
      try {
        await action()
        return
      } catch (error) {
        if (i === maxRetries - 1) throw error
        await this.page.waitForTimeout(1000 * (i + 1))
      }
    }
  }

  /**
   * Scroll element into view
   */
  async scrollToElement(selector: string) {
    const element = this.page.locator(selector)
    await element.scrollIntoViewIfNeeded()
  }

  /**
   * Get all text from elements
   */
  async getAllTexts(selector: string): Promise<string[]> {
    const elements = this.page.locator(selector)
    return await elements.allTextContents()
  }

  /**
   * Verify badge variant
   */
  async verifyBadgeVariant(expectedVariant: string): Promise<boolean> {
    const badge = this.page.locator('.tf-badge')
    const classes = await badge.getAttribute('class')
    return classes?.includes(`tf-badge--${expectedVariant}`) ?? false
  }

  /**
   * Check button is disabled
   */
  async isButtonDisabled(selector: string): Promise<boolean> {
    const button = this.page.locator(selector)
    return await button.isDisabled()
  }

  /**
   * Verify input placeholder
   */
  async verifyInputPlaceholder(selector: string, expectedPlaceholder: string): Promise<boolean> {
    const input = this.page.locator(selector)
    const placeholder = await input.getAttribute('placeholder')
    return placeholder === expectedPlaceholder
  }

  /**
   * Get error message
   */
  async getErrorMessage(): Promise<string | null> {
    const error = this.page.locator('.auth-alert--error, .tf-input__error')
    const isVisible = await error.isVisible()
    if (!isVisible) return null
    
    return await error.textContent()
  }

  /**
   * Verify page header
   */
  async verifyPageHeader(expectedTitle: string): Promise<boolean> {
    const title = this.page.locator('h1, .tf-page-header__title')
    const text = await title.textContent()
    return text?.includes(expectedTitle) ?? false
  }

  /**
   * Check responsive layout
   */
  async verifyResponsiveLayout() {
    const viewports = [
      { width: 375, height: 667, name: 'mobile' },    // iPhone SE
      { width: 768, height: 1024, name: 'tablet' },   // iPad
      { width: 1920, height: 1080, name: 'desktop' }, // Desktop
    ]

    const results = []
    
    for (const viewport of viewports) {
      await this.page.setViewportSize({ width: viewport.width, height: viewport.height })
      await this.waitForPageLoad()
      
      const isLayoutValid = await this.isElementVisible('.dashboard-layout, .auth-layout')
      results.push({ ...viewport, isValid: isLayoutValid })
    }
    
    return results
  }
}

/**
 * Create UI Automation instance
 */
export function createUIAutomation(page: Page): UIAutomation {
  return new UIAutomation(page)
}
