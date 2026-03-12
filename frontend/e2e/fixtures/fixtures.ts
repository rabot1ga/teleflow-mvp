import { test as base } from '@playwright/test'
import { UIAutomation, createUIAutomation } from '../utils/ui-automation'

/**
 * Test Data Fixtures
 */
export const testData = {
  auth: {
    email: 'test@example.com',
    password: 'password123',
    firstName: 'Test',
    lastName: 'User',
  },
  source: {
    rss: {
      name: 'Test RSS Feed',
      url: 'https://example.com/rss',
      interval: 30,
    },
    telegram: {
      name: 'Test Channel',
      username: '@testchannel',
    },
    jsonApi: {
      name: 'JSON API Source',
      url: 'https://api.example.com/articles',
      interval: 60,
    },
  },
  funnel: {
    name: 'Test Welcome Funnel',
    triggerType: 'command',
    triggerValue: '/start',
  },
  target: {
    name: 'Test Channel',
    chatId: '@testchannel',
    type: 'channel',
  },
  template: {
    name: 'Default Template',
    content: '{{title}}\n\n{{content}}\n\n#{{tags}}',
  },
  promotion: {
    parse: {
      name: 'Parse Users Test',
      type: 'parse',
    },
    invite: {
      name: 'Invite Users Test',
      type: 'invite',
    },
  },
}

/**
 * Extended test fixture with UI Automation
 */
export const test = base.extend<{
  ui: UIAutomation
}>({
  ui: async ({ page }, use) => {
    const uiAutomation = createUIAutomation(page)
    await use(uiAutomation)
  },
})

export { expect } from '@playwright/test'
