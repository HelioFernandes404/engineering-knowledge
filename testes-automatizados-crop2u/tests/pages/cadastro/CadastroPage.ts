import { expect, type Page } from '@playwright/test';
import { BACKEND_BASE_URL } from '@src/constants/constants';
import { TCadastroUsuarioBR, TCadastroUsuarioEstrangeiro } from '@src/mocks/usuario/types';

export class Cadastro {

  readonly page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  async goto() {
    await this.page.goto('/');
    await this.page.getByTestId('btnCriarContaLogin').click();
  }

  async getPreencherFormularioCadastro(dataEmpresaBR : TCadastroUsuarioBR) {
    await this.page.getByTestId('inputRazaoSocial').fill(dataEmpresaBR.razaoSocial)
    await this.page.getByTestId('inputCnpj').fill(dataEmpresaBR.cnpj)
    await this.page.getByTestId('inputCnae').fill(dataEmpresaBR.cnae)
    await this.page.getByTestId('inputEmail').fill(dataEmpresaBR.email)
    await this.page.getByTestId('inputTelefone').fill(dataEmpresaBR.telefone)
    await this.page.getByTestId('inputConfirmarEmail').fill(dataEmpresaBR.confirmarEmail)
    await this.page.getByTestId('inputSenha').fill(dataEmpresaBR.senha)
    await this.page.getByTestId('inputConfirmacaoSenha').fill(dataEmpresaBR.confirmarSenha)

    await this.page.getByTestId('btnSalvarCadastroPequeno').click()
  }
  
  async getPreencherFormularioEstragerio(
        dataEmpresaEstr: TCadastroUsuarioEstrangeiro
  ) {
    ;
    await this.page.getByTestId('checkBoxEstrangeiro').click()

    await this.page.getByTestId('inputRazaoSocial').fill(dataEmpresaEstr.razaoSocial)
    await this.page.getByTestId('inputAtividade').fill(dataEmpresaEstr.atividade)
    await this.page.getByTestId('inputEmail').fill(dataEmpresaEstr.email)
    
    await this.page.getByTestId('inputTelefone').fill(dataEmpresaEstr.telefone)
    await this.page.getByTestId('inputConfirmarEmail').fill(dataEmpresaEstr.confirmarEmail)
    
    await this.page.getByTestId('inputSenha').fill(dataEmpresaEstr.senha)
    await this.page.getByTestId('inputConfirmacaoSenha').fill(dataEmpresaEstr.confirmarSenha)
    await this.page.getByTestId('inputDocumento').fill('1234567')

    await this.page.getByTestId('1').click();
    // País
    await this.page.getByLabel('Selecione').locator('div').first().click()
    await this.page.getByText('África do Sul').click()
    
    // Tipo do documento estrangeiro
    await this.page.getByTestId('btnSalvarCadastro').click()
  }
  
  async getCamposEmBrancos() {
    await this.page.getByTestId('inputRazaoSocial').fill('')
    await this.page.getByTestId('inputCnpj').fill('')
    await this.page.getByTestId('inputCnae').fill('')
    await this.page.getByTestId('inputEmail').fill('')
    await this.page.getByTestId('inputTelefone').fill('')
    await this.page.getByTestId('inputConfirmarEmail').fill('')
    await this.page.getByTestId('inputSenha').fill('')
    await this.page.getByTestId('inputConfirmacaoSenha').fill('')
    await this.page.getByTestId('btnSalvarCadastroPequeno').click()
  }

  async getVerificarAlert(alertsArray) {
    await expect(this.page.locator('.alert')).toHaveText(alertsArray);
  }

  async getVerificarCadastro() {
    // Espera resposta do backend devolvendo o status da resposta
    const [responseStatus] = await Promise.all([
      this.page
        .waitForResponse(`${BACKEND_BASE_URL}/api/v1/usuarios`)
        .then(res => res.status()),

      //this.page.click(),
    ]).finally(async () => {

    });

    expect(responseStatus).toBe(200);
  }
}
