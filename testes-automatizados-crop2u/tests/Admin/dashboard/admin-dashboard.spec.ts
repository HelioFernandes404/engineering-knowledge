import { expect, test } from '@playwright/test';
import { loginAsAdmin } from '@src/helpers/helpers';

test.beforeEach(async ({ page }) => {
    await loginAsAdmin(page);
});

test.describe('Admin Dashboard', () => {
    test('Deve exibir listagem de propostas', async ({ page }) => {
        const isVisiblePropostasTable = await page.isVisible(
            'app-propostas-table'
        );
        expect(isVisiblePropostasTable).toBeTruthy();
    });

    test('Deve exibir listagem de usuários pendentes de aprovação', async ({
        page,
    }) => {
        const isVisibleUsuariosTable = await page.isVisible(
            'app-novos-usuario'
        );
        expect(isVisibleUsuariosTable).toBeTruthy();
    });

    test('Deve exibir listagem de propostas pendentes de aprovação', async ({
        page,
    }) => {
        const isVisibleNovasPropostasTable = await page.isVisible(
            'app-novas-propostas'
        );
        expect(isVisibleNovasPropostasTable).toBeTruthy();
    });

    test('Deve exibir listagem de negociações', async ({ page }) => {
        const isVisibleNovasNegociacoesTable = await page.isVisible(
            'app-alterar-status'
        );
        expect(isVisibleNovasNegociacoesTable).toBeTruthy();
    });
});
