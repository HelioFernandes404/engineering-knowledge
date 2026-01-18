import { test } from '@playwright/test';
import { EMAIL_CLIENT, SENHA_CLIENT } from '@src/constants/constants';
import { LoginPage } from '@pages/login/LoginPage';
import { ToastOBJ } from 'support/actions/Componentes';
import { toastrLogin } from '@pages/login/ui/en/LoginUI';

test('deve acessar no sistema com credenciais válidas', async ({ page }) => {
  const loginPage = new LoginPage(page)
  const toastOBJ = new ToastOBJ(page)

  await loginPage.visit()
  await loginPage.preencherFormularioLogin(EMAIL_CLIENT, SENHA_CLIENT)
  await loginPage.submitLogin()

  await toastOBJ.toastHaveText(toastrLogin.localElementoToastr, 
    toastrLogin.sucesso
  )

});

test('deve sair do sistema', async ({ page }) => {
  const loginPage = new LoginPage(page)
  const toastOBJ = new ToastOBJ(page)

  await loginPage.visit()
  await loginPage.preencherFormularioLogin(EMAIL_CLIENT, SENHA_CLIENT)
  await loginPage.submitLogin()

  await toastOBJ.toastHaveText(toastrLogin.localElementoToastr, 
    toastrLogin.sucesso
  )

  await loginPage.logout();

  await toastOBJ.toastHaveText(toastrLogin.localElementoToastr, 
    toastrLogin.logout
  )

})

test('não deve acessar no sistema com login com email inválido', async ({ page }) => {
  const loginPage = new LoginPage(page)
  const toastOBJ = new ToastOBJ(page)

  await loginPage.visit()
  await loginPage.preencherFormularioLogin('client.com.br', SENHA_CLIENT)

  await loginPage.alertHaveText(" Invalid email, please enter a valid email. ")
});

test('não deve acessar no sistema com senha incorreta', async ({ page }) => {
  const loginPage = new LoginPage(page)
  const toastOBJ = new ToastOBJ(page)

  await loginPage.visit()
  await loginPage.preencherFormularioLogin(EMAIL_CLIENT, 'senhaErrada')
  await loginPage.submitLogin()

  await toastOBJ.toastHaveText(toastrLogin.localElementoToastr, 
    toastrLogin.error
  )
});

test('não deve acessar no sistema Login usuário não registrado', async ({ page }) => {
  const loginPage = new LoginPage(page)
  const toastOBJ = new ToastOBJ(page)

  await loginPage.visit()
  await loginPage.preencherFormularioLogin('SorrisoRonaldo@gmail.com', '123123')
  await loginPage.submitLogin()

  await toastOBJ.toastHaveText(toastrLogin.localElementoToastr, 
    toastrLogin.error
  )
});



