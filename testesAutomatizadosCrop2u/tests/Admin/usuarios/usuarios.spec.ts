import { expect } from '@playwright/test';
import { BACKEND_BASE_URL } from '@src/constants/constants';
import Erro from '@src/handlers/Erro';
import { loginAsAdmin } from '@src/helpers/helpers';
import { HttpStatus, StatusAprovacaoUsuario } from '@src/enums/enums';
import AdminDashboardPage from '@pages/admin-dashboard/AdminDashboardPage';
import test from '@src/fixtures/mongoDbWorkerFixture';

test.describe('Gerenciamento de usuários', () => {
    test('Deve conseguir visualizar informações de cadastro de novo usuário', async ({
        page,
        usuarioMock,
        usuariosRepository,
    }) => {
        // Insere um usuário no banco de dados
        const usuario = await usuarioMock.novoUsuario();

        if (usuario instanceof Erro) {
            throw new Error(usuario.message);
        }

        try {
            const adminDashboardPage = new AdminDashboardPage(page);

            await loginAsAdmin(page);

            const userRow = await adminDashboardPage.findPendingUserRow(
                usuario.getRazaoSocial()
            );

            if (!userRow) {
                throw new Error(
                    `usuário ${usuario.getRazaoSocial()} não encontrado na listagem de usuários pendentes.`
                );
            }

            const isVisibleOverviewUsuarios =
                await adminDashboardPage.openUserOverview();

            // TODO: Validar campos exibidos no overview

            expect(isVisibleOverviewUsuarios).toBeTruthy();
        } finally {
            await usuariosRepository.deleteByEmail(usuario.getEmail());
        }
    });

    test('Deve conseguir aprovar um novo usuário através do overview do cadastro', async ({
        page,
        usuarioMock,
        usuariosRepository,
    }) => {
        const usuario = await usuarioMock.novoUsuario();

        if (usuario instanceof Erro) {
            throw new Error(usuario.message);
        }

        try {
            const adminDashboardPage = new AdminDashboardPage(page);

            await loginAsAdmin(page);

            const userRow = await adminDashboardPage.findPendingUserRow(
                usuario.getRazaoSocial()
            );

            if (!userRow) {
                throw new Error(
                    `usuário ${usuario.getRazaoSocial()} não encontrado na listagem de usuários pendentes.`
                );
            }

            await userRow.getByRole('button').first().click();

            const [{ responseStatus, responseBody }] = await Promise.all([
                page
                    .waitForResponse(
                        `${BACKEND_BASE_URL}/api/v1/usuarios/${usuario.getID()}`
                    )
                    .then(async res => {
                        return {
                            responseStatus: res.status(),
                            responseBody: await res.json(),
                        };
                    }),

                await adminDashboardPage.clickAprovarUsuarioOverviewBtn(),
            ]);

            expect(responseStatus).toBe(HttpStatus.Success);
            expect(responseBody.statusAprovacao).toBe(
                StatusAprovacaoUsuario.Aprovado
            );
        } finally {
            await usuariosRepository.deleteByEmail(usuario.getEmail());
        }
    });

    test('Deve conseguir reprovar um novo usuário através do overview do cadastro', async ({
        page,
        usuarioMock,
        usuariosRepository,
    }) => {
        const usuario = await usuarioMock.novoUsuario();

        if (usuario instanceof Erro) {
            throw new Error(usuario.message);
        }

        try {
            const adminDashboardPage = new AdminDashboardPage(page);

            await loginAsAdmin(page);

            const userRow = await adminDashboardPage.findPendingUserRow(
                usuario.getRazaoSocial()
            );

            if (!userRow) {
                throw new Error(
                    `usuário ${usuario.getRazaoSocial()} não encontrado na listagem de usuários pendentes.`
                );
            }

            await userRow.getByRole('button').first().click();

            const [{ responseStatus, responseBody }] = await Promise.all([
                page
                    .waitForResponse(
                        `${BACKEND_BASE_URL}/api/v1/usuarios/${usuario.getID()}`
                    )
                    .then(async res => {
                        return {
                            responseStatus: res.status(),
                            responseBody: await res.json(),
                        };
                    }),

                await adminDashboardPage.clickReprovarUsuarioOverviewBtn(),
            ]);

            expect(responseStatus).toBe(HttpStatus.Success);
            expect(responseBody.statusAprovacao).toBe(
                StatusAprovacaoUsuario.Reprovado
            );
        } finally {
            await usuariosRepository.deleteByEmail(usuario.getEmail());
        }
    });

    test('Deve conseguir aprovar um novo usuário através da listagem de usuários pendentes', async ({
        page,
        usuarioMock,
        usuariosRepository,
    }) => {
        const usuario = await usuarioMock.novoUsuario();

        if (usuario instanceof Erro) {
            throw new Error(usuario.message);
        }

        try {
            const adminDashboardPage = new AdminDashboardPage(page);

            await loginAsAdmin(page);

            const userRow = await adminDashboardPage.findPendingUserRow(
                usuario.getRazaoSocial()
            );

            if (!userRow) {
                throw new Error(
                    `usuário ${usuario.getRazaoSocial()} não encontrado na listagem de usuários pendentes.`
                );
            }

            const [{ responseStatus, responseBody }] = await Promise.all([
                page
                    .waitForResponse(
                        `${BACKEND_BASE_URL}/api/v1/usuarios/${usuario.getID()}`
                    )
                    .then(async res => {
                        return {
                            responseStatus: res.status(),
                            responseBody: await res.json(),
                        };
                    }),

                await adminDashboardPage.clickAprovarUsuarioTableBtn(userRow),
            ]);

            expect(responseStatus).toBe(HttpStatus.Success);
            expect(responseBody.statusAprovacao).toBe(
                StatusAprovacaoUsuario.Aprovado
            );
        } finally {
            await usuariosRepository.deleteByEmail(usuario.getEmail());
        }
    });

    test('Deve conseguir reprovar um novo usuário através da listagem de usuários pendentes', async ({
        page,
        usuarioMock,
        usuariosRepository,
    }) => {
        const usuario = await usuarioMock.novoUsuario();

        if (usuario instanceof Erro) {
            throw new Error(usuario.message);
        }

        try {
            const adminDashboardPage = new AdminDashboardPage(page);

            await loginAsAdmin(page);

            const userRow = await adminDashboardPage.findPendingUserRow(
                usuario.getRazaoSocial()
            );

            if (!userRow) {
                throw new Error(
                    `usuário ${usuario.getRazaoSocial()} não encontrado na listagem de usuários pendentes.`
                );
            }

            const [{ responseStatus, responseBody }] = await Promise.all([
                page
                    .waitForResponse(
                        `${BACKEND_BASE_URL}/api/v1/usuarios/${usuario.getID()}`
                    )
                    .then(async res => {
                        return {
                            responseStatus: res.status(),
                            responseBody: await res.json(),
                        };
                    }),

                await adminDashboardPage.clickReprovarUsuarioTableBtn(userRow),
            ]);

            expect(responseStatus).toBe(HttpStatus.Success);
            expect(responseBody.statusAprovacao).toBe(
                StatusAprovacaoUsuario.Reprovado
            );
        } finally {
            await usuariosRepository.deleteByEmail(usuario.getEmail());
        }
    });
});
