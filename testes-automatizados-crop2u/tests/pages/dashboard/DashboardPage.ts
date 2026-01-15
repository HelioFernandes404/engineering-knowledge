import { expect, type Page } from '@playwright/test';
import { BACKEND_BASE_URL } from '@src/constants/constants';
import { HttpStatus } from '@src/enums/enums';
import { TCadastroProposta } from '@src/mocks/proposta/types';

export class DashboardPage {
    readonly page: Page;

    constructor(page: Page) {
        this.page = page;
    }

    async visit() {
        await this.page.goto('/');
    }

    async preencherFormularioLogin(email, senha) {
        await this.page.locator('#email').fill(email);
        await this.page.locator('#password').fill(senha);
    }

    async submitLogin() {
        await this.page.getByTestId('btnEntrarLogin').click();
    }

    async toastHaveText(message) {
        const toast = this.page.locator('.ngx-toastr');

        await expect(toast).toHaveText(message);
        await expect(toast).toBeHidden({ timeout: 15000 });
    }

    async obterRespostaDoBackend(btnByTestId, routerApi) {
        this.page.getByTestId(btnByTestId).click();
        const [response] = await Promise.all([
            this.page.waitForResponse(`${BACKEND_BASE_URL}${routerApi}`),
        ]);
        const responseStatus = await response.status();
        const jsonRes = await response.json();
        return { responseStatus, jsonRes };
    }

    async verificarTabelaPropostas(response) {
        expect(response.jsonRes).toBeDefined();
        expect(response.responseStatus).toBe(HttpStatus.Success);
        await this.page.locator('app-propostas-table').isVisible();
    }

    async verificarOverviewProposta(codigoPrimeiraProposta) {
        await this.page
            .getByText(`PROPOSAL N°: ${codigoPrimeiraProposta}`)
            .isVisible();
        await this.page
            .getByText(`PROPOSAL N°: ${codigoPrimeiraProposta}`)
            .click();
    }

    async preencherFormularioProposta(proposta: TCadastroProposta) {
        await this.page.locator(`#operacao-${proposta.tipo}`).click();

        await this.page.locator(`#produto-${proposta.produto.codigo}`).click();

        await this.page.locator(`#incoterm-${proposta.incoterm}`).click();

        await this.page.locator('#precificacao').fill(proposta.precificacao);
        await this.page
            .locator('#volume')
            .fill(`${proposta.produto.quantidade.valor}`);
        await this.page
            .locator('#periodoEmbarque')
            .fill(proposta.periodoEmbarque);
        await this.page
            .locator('#ensacamento')
            .fill(proposta.produto.ensacamento);
        await this.page
            .locator('#termosPagamento')
            .fill(proposta.termosPagamento);
        await this.page.locator('#produtor').fill(proposta.produtor);

        await this.page.getByRole('button', { name: 'SEND PROPOSAL' }).click();
        await this.page.waitForTimeout(15000);
        await this.page.getByText('PROPOSTA ENVIADA').isVisible();
    }

    async isVisibleElement(nameElement: string) {
        await this.page.getByTestId(nameElement).click();
        await this.page.getByTestId(nameElement).isVisible();
    }

    async waitForTimeoutAnyTime(time) {
        await this.page.waitForTimeout(time);
    }

    async clickBtnOverviewById(codProposta) {
        await this.page.getByTestId('btnOverview_' + codProposta).click();
    }

    async preencherNegociationTerm(locator, text) {
        await this.page.locator(locator).fill(text);
    }
}
