import AdminDashboardPage from '@pages/admin-dashboard/AdminDashboardPage';
import { expect } from '@playwright/test';
import { BACKEND_BASE_URL } from '@src/constants/constants';
import { HttpStatus, StatusProposta } from '@src/enums/enums';
import test from '@src/fixtures/mongoDbWorkerFixture';
import Erro from '@src/handlers/Erro';
import { loginAsAdmin } from '@src/helpers/helpers';

test.describe('Propostas em análise', () => {
    test('Deve conseguir visualizar informações da proposta', async ({
        page,
        usuarioMock,
        propostaMock,
        produtosRepository,
        propostasRepository,
        usuariosRepository,
    }) => {
        const usuario = await usuarioMock.novoUsuarioAprovado();

        if (usuario instanceof Erro) {
            throw usuario;
        }

        const proposta = await propostaMock.novaProposta(usuario.getEmail());

        if (proposta instanceof Erro) {
            throw proposta;
        }

        // Busca produto na base de dados para conferir o nome do produto
        const produto = await produtosRepository.find(proposta.getCodProduto());

        if (produto instanceof Erro) {
            throw produto;
        }

        const adminDashboardPage = new AdminDashboardPage(page);

        try {
            await loginAsAdmin(page);

            const propRow = await adminDashboardPage.findPendingPropRow(
                proposta.getCodigo()
            );

            if (!propRow) {
                throw new Error(
                    `proposta ${proposta.getCodigo()} não encontrada na listagem de propostas em análise.`
                );
            }

            const isVisibleOverviewProp =
                await adminDashboardPage.openPropOverview(propRow);

            expect(isVisibleOverviewProp).toBeTruthy();

            adminDashboardPage.validatePropOverviewFields(
                proposta,
                usuario.getRazaoSocial(),
                produto.getNome()
            );
        } finally {
            await propostasRepository.deleteByCodigo(proposta.getCodigo());
            await usuariosRepository.deleteByEmail(usuario.getEmail());
        }
    });

    test('Deve conseguir aprovar proposta', async ({
        page,
        usuarioMock,
        propostaMock,
        propostasRepository,
        usuariosRepository,
    }) => {
        const usuario = await usuarioMock.novoUsuarioAprovado();

        if (usuario instanceof Erro) {
            throw usuario;
        }

        const proposta = await propostaMock.novaProposta(usuario.getEmail());

        if (proposta instanceof Erro) {
            throw proposta;
        }

        const adminDashboardPage = new AdminDashboardPage(page);

        try {
            await loginAsAdmin(page);

            const propRow = await adminDashboardPage.findPendingPropRow(
                proposta.getCodigo()
            );

            if (!propRow) {
                throw new Error(
                    `proposta ${proposta.getCodigo()} não encontrada na listagem de propostas em análise.`
                );
            }

            const [{ responseStatus, responseBody }] = await Promise.all([
                page
                    .waitForResponse(
                        `${BACKEND_BASE_URL}/api/v1/propostas/${proposta.getCodigo()}?aprovar`
                    )
                    .then(async res => {
                        return {
                            responseStatus: res.status(),
                            responseBody: await res.json(),
                        };
                    }),

                await adminDashboardPage.clickAprovarProp(propRow),
            ]);

            expect(responseStatus).toBe(HttpStatus.Success);
            expect(responseBody.proposta.status).toBe(StatusProposta.Aberto);
            expect(responseBody.proposta.expiraEm).toBeGreaterThan(0);
        } finally {
            await propostasRepository.deleteByCodigo(proposta.getCodigo());
            await usuariosRepository.deleteByEmail(usuario.getEmail());
        }
    });

    test('Deve conseguir reprovar proposta', async ({
        page,
        usuarioMock,
        propostaMock,
        usuariosRepository,
        propostasRepository,
    }) => {
        const usuario = await usuarioMock.novoUsuarioAprovado();

        if (usuario instanceof Erro) {
            throw usuario;
        }

        const proposta = await propostaMock.novaProposta(usuario.getEmail());

        if (proposta instanceof Erro) {
            throw proposta;
        }

        const adminDashboardPage = new AdminDashboardPage(page);

        try {
            await loginAsAdmin(page);

            const propRow = await adminDashboardPage.findPendingPropRow(
                proposta.getCodigo()
            );

            if (!propRow) {
                throw new Error(
                    `proposta ${proposta.getCodigo()} não encontrada na listagem de propostas em análise.`
                );
            }

            const [{ responseStatus, responseBody }] = await Promise.all([
                page
                    .waitForResponse(
                        `${BACKEND_BASE_URL}/api/v1/propostas/${proposta.getCodigo()}`
                    )
                    .then(async res => {
                        return {
                            responseStatus: res.status(),
                            responseBody: await res.json(),
                        };
                    }),

                await adminDashboardPage.clickReprovarProp(propRow),
            ]);

            expect(responseStatus).toBe(HttpStatus.Success);
            expect(responseBody.proposta.status).toBe(StatusProposta.Reprovada);
            expect(responseBody.proposta.expiraEm).toBe(0);
        } finally {
            await propostasRepository.deleteByCodigo(proposta.getCodigo());
            await usuariosRepository.deleteByEmail(usuario.getEmail());
        }
    });
});
