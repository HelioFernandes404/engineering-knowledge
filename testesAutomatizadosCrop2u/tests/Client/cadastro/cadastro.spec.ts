import { deleteUser } from '@src/helpers/helpers';
import { Cadastro } from '@pages/cadastro/CadastroPage';
import test from '@src/fixtures/mongoDbWorkerFixture';

test('deve cadastrar com dados usuário brasileiro', async ({
    page,
    loginsRepository,
    usuariosRepository,
    usuarioMock,
}) => {
    const pageCadastro = new Cadastro(page);

    await pageCadastro.goto();

    const dadosUsuarioBR = usuarioMock.getDadosCadastroUsuarioBR();

    await pageCadastro.getPreencherFormularioCadastro(dadosUsuarioBR);

    try {
        await pageCadastro.getVerificarCadastro();
    } finally {
        await deleteUser(
            dadosUsuarioBR.email,
            loginsRepository,
            usuariosRepository
        );
    }
});

test('deve cadastrar com dados usuário estrangeiro', async ({
    page,
    loginsRepository,
    usuariosRepository,
    usuarioMock,
}) => {
    const pageCadastro = new Cadastro(page);

    const dadosUsuarioEstr = usuarioMock.getDadosUsuarioEstrangeiro();

    await pageCadastro.goto();
    await pageCadastro.getPreencherFormularioEstragerio(dadosUsuarioEstr);

    try {
        await pageCadastro.getVerificarCadastro();
    } finally {
        await deleteUser(
            dadosUsuarioEstr.email,
            loginsRepository,
            usuariosRepository
        );
    }
});

test('não deve cadastrar com campos em branco', async ({ page }) => {
    const pageCadastro = new Cadastro(page);
    await pageCadastro.goto();

    await pageCadastro.getCamposEmBrancos();

    const dataAlertsEn = {
        cnpj:" Invalid CNPJ, please enter a valid CNPJ. ",
        cnae: " Invalid CNAE, please enter a valid CNAE. ",
        email: " Invalid email, please enter a valid email. ",
        telefone:" Invalid phone, please enter a valid phone. ",
        senha:" Invalid password, please enter a valid password. ",
    }

   await page.getByText('Registration Error! Please').isVisible()
   const alertsArray = await Object.values(dataAlertsEn);
   await pageCadastro.getVerificarAlert(alertsArray)
});

test('não deve cadastra com formato de email inválido', async ({ page }) => {
    const pageCadastro = new Cadastro(page);
    await pageCadastro.goto();

    await pageCadastro.getCamposEmBrancos();
    await page
        .getByText(' Invalid email, please enter a valid email. ')
        .isVisible();
});
