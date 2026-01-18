import { expect, type Page } from '@playwright/test';


export class LoginPage {

  readonly page: Page;


  constructor(page: Page) {
    this.page = page;
  }

  async visit() {
    await this.page.goto('/');
  }

  async preencherFormularioLogin(email: string, senha: string) {
    await this.page.locator('#email').fill(email)
    await this.page.locator('#password').fill(senha)
  }

  async submitLogin() {
    await this.page.locator('button:has-text("ENTER")').click();
  }

  async alertHaveText(target) {
    await expect(this.page.locator('.alert')).toHaveText(target)
  }

  async logout() {
    await this.page.locator('#menu-colapsar > p').click();
    await this.page.locator('.listaAccountMenuOptions > :nth-child(4)').click();
  }
}
