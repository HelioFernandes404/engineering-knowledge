import { expect } from '@playwright/test';
import {
    BACKEND_BASE_URL,
    EMAIL_CLIENT,
    SENHA_CLIENT,
} from '@src/constants/constants';
import { HttpStatus, StatusProposta, TipoDeProposta } from '@src/enums/enums';
import Erro from '@src/handlers/Erro';
import { logErro, logInfo } from '@src/helpers/helpers';
import { DashboardPage } from '@pages/dashboard/DashboardPage';
import test from '@src/fixtures/mongoDbWorkerFixture';
import exp = require('constants');
import { ToastOBJ } from 'support/actions/Componentes';
import { toastrLogin } from '@pages/login/ui/en/LoginUI';

test.describe('Tabulação', () => {
    test('Deve haver uma tabulação de propostas exibida na tela', async ({
        page,
    }) => {
        const dashboardPage = new DashboardPage(page);

        await dashboardPage.visit();
        await dashboardPage.preencherFormularioLogin(
            EMAIL_CLIENT,
            SENHA_CLIENT
        );

        const response = await dashboardPage.obterRespostaDoBackend(
            'btnEntrarLogin',
            '/api/v1/dashboard'
        );

        await dashboardPage.verificarTabelaPropostas(response);
    });

    test('Deve haver um botão de overview para as propostas', async ({
        page,
    }) => {
        const dashboardPage = new DashboardPage(page);
        const toastOBJ = new ToastOBJ(page);

        await dashboardPage.visit();
        await dashboardPage.preencherFormularioLogin(
            EMAIL_CLIENT,
            SENHA_CLIENT
        );
        await dashboardPage.submitLogin();

        const response = await dashboardPage.obterRespostaDoBackend(
            'btnEntrarLogin',
            '/api/v1/dashboard'
        );
        //Acesse diretamente o primeiro objeto na lista 'propostasDashboard' e obtenha o valor da chave 'codigo'
        const codigoPrimeiraProposta =
            response.jsonRes.propostasDashboard[0].codigo;

        await toastOBJ.toastHaveText(
            toastrLogin.localElementoToastr,
            toastrLogin.sucesso
        );
        await dashboardPage.clickBtnOverviewById(codigoPrimeiraProposta);

        await dashboardPage.verificarOverviewProposta(codigoPrimeiraProposta);
    });

    test('Deve conseguir mostrar interesse em uma proposta', async ({
        page,
        usuarioMock,
        propostaMock,
        usuariosRepository,
        propostasRepository,
        negociacoesRepository,
    }) => {
        let codProposta: string = '';
        let codNegociacao: string = '';

        // Cria usuário dono da proposta que será criada em seguida
        const usuario = await usuarioMock.novoUsuarioAprovado();

        if (usuario instanceof Erro) {
            throw new Error(usuario.message);
        }

        // Cria uma proposta com status 'Aberto à negociações' (disponível)
        const proposta = await propostaMock.novaProposta(usuario.getEmail(), {
            status: StatusProposta.Aberto,
        });

        if (!(proposta instanceof Erro)) {
            codProposta = proposta.getCodigo();
        }

        try {
            const dashboardPage = new DashboardPage(page);
            await dashboardPage.visit();
            await dashboardPage.preencherFormularioLogin(
                EMAIL_CLIENT,
                SENHA_CLIENT
            );

            await dashboardPage.waitForTimeoutAnyTime(1000);
            await dashboardPage.clickBtnOverviewById(codProposta);
            //await page.getByTestId('btnOverview_'+ codProposta).click();

            await dashboardPage.preencherNegociationTerm(
                '#NegociationTerm',
                'Em resumo, um termo de negociação é um documento fundamental para estabelecer as bases de uma transação comercial.'
            );

            /*
            await page
                .locator('#NegociationTerm')
                .fill(
                    'Em resumo, um termo de negociação é um documento fundamental para estabelecer as bases de uma transação comercial.'
                );
            */

            // Espera retorno do backend e recupera o status e o json da resposta
            const [{ responseStatus, jsonRes }] = await Promise.all([
                page
                    .waitForResponse(
                        `${BACKEND_BASE_URL}/api/v1/propostas/${codProposta}/negociacoes`
                    )
                    .then(async res => {
                        const jsonRes = await res.json();
                        return { responseStatus: res.status(), jsonRes };
                    }),

                page.getByRole('button', { name: 'REGISTER | APPLY' }).click(),
            ]);

            // Tenta recuperar código da negociação criada a partir do json da resposta
            codNegociacao = jsonRes.negociacao?.codigo ?? '';

            expect(responseStatus).toBe(HttpStatus.Created);
        } finally {
            // Caso ocorra erro em qualquer uma das operações dentro do try {}
            // irá tentar remover a negociação e a proposta criadas, caso existam
            // Caso não ocorra erro, a negociação e a proposta também serão removidas
            if (codNegociacao) {
                logInfo(`Removendo negociação ${codNegociacao}`);
                await negociacoesRepository.deleteByCodigo(codNegociacao);
            }

            if (codProposta) {
                logInfo(`Removendo proposta ${codProposta}`);
                await propostasRepository.deleteByCodigo(codProposta);
            }

            if (usuario) {
                logInfo(`Removendo usuário ${usuario.getEmail()}`);
                await usuariosRepository.deleteByEmail(usuario.getEmail());
            }
        }
    });

    test.describe('Filtro', () => {
        test('Deve haver um filtro com Proposal, Qtdy, Shipment,S Packing, Operation, Product Type, Status e Validade.', async ({
            page,
        }) => {
            const dashboardPage = new DashboardPage(page);
            await dashboardPage.visit();
            await dashboardPage.preencherFormularioLogin(
                EMAIL_CLIENT,
                SENHA_CLIENT
            );

            const buttonNames = [
                'PROPOSAL N°',
                'QTDY',
                'SHIPMENT',
                'PACKING',
                'OPERATION',
                'PRODUCT TYPE',
                'STATUS',
                'CLEAR',
            ];

            for (const name of buttonNames) {
                await page.getByRole('button', { name }).isVisible();
                await page.getByRole('button', { name }).click();
            }
        });

        test('não Deve filtrar quando informar dados invalidos', async ({
            page,
        }) => {
            const dashboardPage = new DashboardPage(page);
            await dashboardPage.visit();
            await dashboardPage.preencherFormularioLogin(
                EMAIL_CLIENT,
                SENHA_CLIENT
            );

            //TODO:
            await page.getByRole('button', { name: 'QTDY' }).click();
            await page.locator('#maiorQ').click();
            // Preencher o campo de input
            await page.locator('#filtroNumero').fill('-9999');

            // Esperar por um evento ou uma ação assíncrona após o preenchimento
            // Aqui, estou usando um exemplo de esperar até que o botão de envio esteja habilitado (substitua conforme necessário)
            await page.getByRole('button', { name: 'SEARCH' }).click();

            // Verificar o status code após o preenchimento
            const response = await page.waitForResponse(
                response => response.status() === 400
            );

            // Aqui você pode realizar ações com a resposta, se necessário
            console.log('Status Code:', response.status());
        });
    });
});

test.describe('Propostas', () => {
    test('Deve criar uma proposta de Sell', async ({
        page,
        propostasRepository,
        propostaMock,
    }) => {
        const dadosCadastroProposta = propostaMock.getDadosCadastroProposta({
            tipo: TipoDeProposta.Venda,
        });

        const dashboardPage = new DashboardPage(page);
        //caminho de login
        await dashboardPage.visit();
        await dashboardPage.preencherFormularioLogin(
            EMAIL_CLIENT,
            SENHA_CLIENT
        );
        await dashboardPage.submitLogin();

        await dashboardPage.preencherFormularioProposta(dadosCadastroProposta);

        //codigo da proposta
        const codigoProposta = await page
            .locator('div.corpo p.subtitulo:not(.fonte-padrao-varela)')
            .textContent();

        if (!codigoProposta) {
            logErro('Falha ao obter código da proposta criada.');
            return;
        }

        // Deleta proposta inserida
        await propostasRepository.deleteByCodigo(codigoProposta);
    });

    test('Deve criar um proposta de Buy', async ({
        page,
        propostasRepository,
        propostaMock,
    }) => {
        const dadosCadastroProposta = propostaMock.getDadosCadastroProposta({
            tipo: TipoDeProposta.Compra,
        });

        const dashboardPage = new DashboardPage(page);

        //caminho de login
        await dashboardPage.visit();
        await dashboardPage.preencherFormularioLogin(
            EMAIL_CLIENT,
            SENHA_CLIENT
        );
        await dashboardPage.submitLogin();

        await dashboardPage.preencherFormularioProposta(dadosCadastroProposta);

        const codigoProposta = await page
            .locator('div.corpo p.subtitulo:not(.fonte-padrao-varela)')
            .textContent();

        if (!codigoProposta) {
            logErro('Falha ao obter código da proposta criada.');
            return;
        }

        // Deleta proposta inserida
        await propostasRepository.deleteByCodigo(codigoProposta);
    });

    test('Deve gerar um código de proposta após a confirmação de uma proposta.', async ({
        page,
        propostasRepository,
        propostaMock,
    }) => {
        const dadosCadastroProposta = propostaMock.getDadosCadastroProposta();

        const dashboardPage = new DashboardPage(page);

        //caminho de login
        await dashboardPage.visit();
        await dashboardPage.preencherFormularioLogin(
            EMAIL_CLIENT,
            SENHA_CLIENT
        );
        await dashboardPage.submitLogin();

        await dashboardPage.preencherFormularioProposta(dadosCadastroProposta);

        const codigoProposta = await page
            .locator('div.corpo p.subtitulo:not(.fonte-padrao-varela)')
            .textContent();

        if (!codigoProposta) {
            logErro('Falha ao obter código da proposta criada.');
            return;
        }

        // Deleta proposta inserida
        await propostasRepository.deleteByCodigo(codigoProposta);
    });

    test('Deve aplicar em uma proposta', async ({
        page,
        propostasRepository,
        propostaMock,
    }) => {
        const dadosCadastroProposta = propostaMock.getDadosCadastroProposta();

        const dashboardPage = new DashboardPage(page);

        //caminho de login
        await dashboardPage.visit();
        await dashboardPage.preencherFormularioLogin(
            EMAIL_CLIENT,
            SENHA_CLIENT
        );
        await dashboardPage.submitLogin();

        await dashboardPage.preencherFormularioProposta(dadosCadastroProposta);

        const codigoProposta = await page
            .locator('div.corpo p.subtitulo:not(.fonte-padrao-varela)')
            .textContent();

        if (!codigoProposta) {
            logErro('Falha ao obter código da proposta criada.');
            return;
        }

        // Deleta proposta inserida
        await propostasRepository.deleteByCodigo(codigoProposta);
    });

    test('não Deve aplicar mais de um vez para a mesma proposta', async ({
        page,
        usuarioMock,
        propostaMock,
        usuariosRepository,
        propostasRepository,
        negociacoesRepository,
    }) => {
        let codProposta: string = '';

        const usuario = await usuarioMock.novoUsuarioAprovado();

        if (usuario instanceof Erro) {
            throw new Error(usuario.message);
        }

        const proposta = await propostaMock.novaProposta(usuario.getEmail(), {
            status: StatusProposta.Aberto,
        });

        if (!(proposta instanceof Erro)) {
            codProposta = proposta.getCodigo();
        }

        try {
            const dashboardPage = new DashboardPage(page);
            await dashboardPage.visit();
            await dashboardPage.preencherFormularioLogin(
                EMAIL_CLIENT,
                SENHA_CLIENT
            );

            await page.getByTestId('btnOverview_' + codProposta).click();
            await page
                .locator('#NegociationTerm')
                .fill('Termos de negoçoes...');

            await page.getByTestId('btnEnviarOverview').click();

            await page.getByTestId('btnFecharOverview').click();
            //fazer a proposta novamente
            await page.getByTestId('btnOverview_' + codProposta).click();
            await page
                .locator('#NegociationTerm')
                .fill('Termos de negoçoes...');

            await page.getByTestId('btnEnviarOverview').click({ force: true });
        } finally {
            //deletar proposta e usuario da propsota
            if (codProposta) {
                logInfo(`Removendo proposta ${codProposta}`);
                await propostasRepository?.deleteByCodigo(codProposta);
            }

            if (usuario) {
                logInfo(`Removendo usuário ${usuario.getEmail()}`);
                await usuariosRepository.deleteByEmail(usuario.getEmail());
            }
        }
    });

    test('não Deve criar negociações além dos 255 caracteres', async ({
        page,
        usuarioMock,
        propostaMock,
        usuariosRepository,
        propostasRepository,
    }) => {
        let codProposta: string = '';

        // Cria usuário dono da proposta que será criada em seguida
        const usuario = await usuarioMock.novoUsuarioAprovado();

        if (usuario instanceof Erro) {
            throw new Error(usuario.message);
        }

        // Cria uma proposta com status 'Aberto à negociações' (disponível)
        const proposta = await propostaMock.novaProposta(usuario.getEmail(), {
            status: StatusProposta.Aberto,
        });

        if (!(proposta instanceof Erro)) {
            codProposta = proposta.getCodigo();
        }

        try {
            const dashboardPage = new DashboardPage(page);
            await dashboardPage.visit();
            await dashboardPage.preencherFormularioLogin(
                EMAIL_CLIENT,
                SENHA_CLIENT
            );

            await page.getByTestId('btnOverview_' + codProposta).click();

            await page
                .locator('#NegociationTerm')
                // Texto com 257 caracteres
                .fill(
                    'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam eleifend rhoncus odio sed malesuada. Maecenas neque dolor, lobortis eget lorem ut, suscipit vestibulum augue. Aliquam sit amet pellentesque arcu, ut auctor tortor. Suspendisse non sapien eu...'
                );

            await page.getByTestId('btnEnviarOverview').click();

            await page.getByLabel('Proposal Error').isVisible();
        } finally {
            if (codProposta) {
                logInfo(`Removendo proposta ${codProposta}`);
                await propostasRepository?.deleteByCodigo(codProposta);
            }

            if (usuario) {
                logInfo(`Removendo usuário ${usuario.getEmail()}`);
                await usuariosRepository.deleteByEmail(usuario.getEmail());
            }
        }
    });
});
