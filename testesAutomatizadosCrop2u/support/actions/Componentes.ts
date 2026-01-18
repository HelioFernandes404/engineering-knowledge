import { expect, type Page } from '@playwright/test';

export class ToastOBJ {
    readonly page: Page;
    constructor(page: Page) {
      this.page = page
    }

    async toastHaveText(locator,message) {
        const toast = this.page.locator(locator)
        await expect(toast).toHaveText(message)
        await expect(toast).toBeHidden({ timeout: 15000 });
    }
}

export class alertOBJ {
    readonly page: Page;
    constructor(page: Page) {
      this.page = page
    }
}