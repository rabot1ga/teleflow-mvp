# TeleFlow E2E Tests

End-to-end tests for TeleFlow Platform using Playwright.

## 📋 Overview

This test suite covers all major user flows in the TeleFlow Platform:

- **Authentication** - Login, Register, Logout
- **Content Module** - Sources, Articles, Moderation
- **Publishing Module** - Targets, Templates, Calendar
- **Funnels Module** - Funnels, Lead Magnets, Broadcasts
- **Promotion Module** - Parse, Invite, Masslook, Comment tasks
- **Analytics Module** - Overview, Content, Funnels, Broadcasts

## 🚀 Quick Start

### Install Dependencies

```bash
npm install
npx playwright install
```

### Run Tests

```bash
# Run all tests
npm run test:e2e

# Run tests in headed mode (see browser)
npm run test:e2e:headed

# Run tests with UI mode
npm run test:e2e:ui

# Run tests in debug mode
npm run test:e2e:debug

# Run specific test file
npx playwright test e2e/auth/auth.spec.ts

# Run tests by tag
npx playwright test --grep @smoke
npx playwright test --grep @critical
```

### View Report

```bash
npm run test:e2e:report
```

## 📁 Test Structure

```
e2e/
├── auth/
│   └── auth.spec.ts          # Login, Register, Logout tests
├── content/
│   └── content.spec.ts       # Sources, Articles, Moderation tests
├── publishing/
│   └── publishing.spec.ts    # Targets, Templates, Calendar tests
├── funnels/
│   └── funnels.spec.ts       # Funnels, Broadcasts tests
├── promotion/
│   └── promotion.spec.ts     # Promotion tasks tests
├── analytics/
│   └── analytics.spec.ts     # Analytics dashboard tests
└── fixtures/
    └── fixtures.ts           # Shared test fixtures
```

## 🎯 Test Coverage

### Authentication (8 tests)
- ✅ Display login page
- ✅ Form validation
- ✅ Navigation to register
- ✅ Navigation to forgot password
- ✅ Login with valid credentials
- ✅ Login with invalid credentials
- ✅ Display register page
- ✅ Password validation
- ✅ Logout functionality

### Content Module (15 tests)
- ✅ Display content page with tabs
- ✅ Switch between tabs
- ✅ Open add source modal
- ✅ Create RSS source
- ✅ Validate source form
- ✅ Select different source types
- ✅ Display sources table
- ✅ Fetch source manually
- ✅ Edit source
- ✅ Delete source
- ✅ Display articles tab
- ✅ Display moderation tab
- ✅ Approve article
- ✅ Reject article

### Publishing Module (12 tests)
- ✅ Display publishing page
- ✅ Switch between tabs
- ✅ Open add target modal
- ✅ Create target
- ✅ Display targets table
- ✅ Edit target
- ✅ Delete target
- ✅ Open create template modal
- ✅ Create template
- ✅ Display templates table
- ✅ Show template variables help

### Funnels Module (8 tests)
- ✅ Display funnels page
- ✅ Open create funnel modal
- ✅ Create funnel
- ✅ Display funnels table
- ✅ Delete funnel
- ✅ Toggle funnel status

### Promotion Module (9 tests)
- ✅ Display promotion page
- ✅ Open create task modal
- ✅ Select task type
- ✅ Create parse task
- ✅ Display tasks table
- ✅ Filter tasks by type
- ✅ Start task
- ✅ View task results

### Analytics Module (12 tests)
- ✅ Display analytics page
- ✅ Switch between tabs
- ✅ Change time period
- ✅ Display overview stats
- ✅ Display recent activity
- ✅ Content performance
- ✅ Approval rate
- ✅ Funnel conversion
- ✅ Conversion rate

## 🔧 Configuration

### playwright.config.ts

```typescript
export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  retries: process.env.CI ? 2 : 0,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
})
```

## 📊 Best Practices

### 1. Test Isolation
Each test should be independent and not rely on other tests.

### 2. Page Object Model (Future)
Consider implementing POM for better maintainability:

```typescript
// e2e/pages/LoginPage.ts
export class LoginPage {
  constructor(private page: Page) {}

  async goto() {
    await this.page.goto('/login')
  }

  async login(email: string, password: string) {
    await this.page.fill('input[type="email"]', email)
    await this.page.fill('input[type="password"]', password)
    await this.page.click('button[type="submit"]')
  }
}
```

### 3. Test Data Management
Use fixtures for test data:

```typescript
// e2e/fixtures/test-data.ts
export const testData = {
  user: {
    email: 'test@example.com',
    password: 'password123',
  },
  source: {
    name: 'Test RSS',
    url: 'https://example.com/rss',
  },
}
```

### 4. Selectors
Use stable selectors (data-testid):

```typescript
// In your component
<button data-testid="create-button">Create</button>

// In test
await page.click('[data-testid="create-button"]')
```

## 🐛 Debugging

### Run in Debug Mode
```bash
npx playwright test --debug
```

### Run Specific Test
```bash
npx playwright test -g "should create funnel"
```

### Run with Headed Browser
```bash
npx playwright test --headed
```

### Trace Viewer
```bash
npx playwright show-trace trace.zip
```

## 📈 CI/CD Integration

### GitHub Actions Example

```yaml
name: E2E Tests
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18
      - run: npm ci
      - run: npx playwright install --with-deps
      - run: npm run test:e2e
      - uses: actions/upload-artifact@v3
        if: failure()
        with:
          name: playwright-report
          path: playwright-report/
```

## 🎯 Future Enhancements

- [ ] API mocking for backend-independent tests
- [ ] Visual regression testing
- [ ] Performance testing
- [ ] Accessibility testing
- [ ] Mobile viewport testing
- [ ] Page Object Model implementation
- [ ] Test data factories
- [ ] Parallel test execution optimization

## 📝 Tags

Use tags to organize tests:

```typescript
test('should login successfully', async ({ page }) => {
  // ... test code
})
test.describe('Critical Flows', { tag: '@critical' }, () => {
  // ... critical tests
})
```

Run tests by tag:
```bash
npx playwright test --grep @critical
npx playwright test --grep @smoke
npx playwright test --grep @auth
```

## 📞 Support

For issues or questions, please refer to:
- [Playwright Documentation](https://playwright.dev)
- [Playwright GitHub](https://github.com/microsoft/playwright)

---

**Last Updated:** March 12, 2026
