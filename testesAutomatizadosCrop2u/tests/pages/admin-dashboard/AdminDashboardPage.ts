import { Locator, Page, expect } from '@playwright/test';
import { TipoDeProposta } from '@src/enums/enums';
import {
    incotermToString,
    logErro,
    statusDaPropostaToString,
} from '@src/helpers/helpers';
import { IPropostaEntity } from '@src/interfaces/propostas';
import {
    GridPropostas,
    OverviewProposta,
    OverviewUsuario,
} from './ui/en/AdminDashboardUI';

export default class AdminDashboardPage {
    private readonly page: Page;

    constructor(page: Page) {
        this.page = page;
    }

    async openUserOverview() {
        await this.page
            .getByRole('button', { name: 'abrir overview' })
            .first()
            .click();

        return this.page.isVisible('app-overview-usuarios-admin');
    }

    /**
     * Localiza, na tabela da listagem de usuários pendentes, a linha correspondente
     * ao usuário com a razaoSocial passada como parâmetro
     *
     * Retorna o Locator da linha correspondente ao usuário
     * ou retorna null caso não encontre o usuário na listagem de usuários pendentes
     */
    async findPendingUserRow(razaoSocial: string) {
        const userRow = this.page.getByRole('row', {
            name: razaoSocial,
            exact: true,
        });

        const nextPageBtn = this.page
            .locator('app-novos-usuario')
            .getByLabel('Próxima página');

        let [userRowIsVisible, nextPageBtnIsEnabled] = await Promise.all([
            userRow.isVisible(),
            nextPageBtn.isEnabled(),
        ]);

        // Avança a paginação até encontrar o usuário com a razaoSocial informada
        // ou até chegar à ultima página da listagem de usuários pendentes
        while (!userRowIsVisible) {
            if (!nextPageBtnIsEnabled) {
                break;
            }

            await nextPageBtn.click();

            [userRowIsVisible, nextPageBtnIsEnabled] = await Promise.all([
                userRow.isVisible(),
                nextPageBtn.isEnabled(),
            ]);
        }

        if (!userRowIsVisible) {
            return null;
        }

        return this.page.getByRole('row', { name: razaoSocial });
    }

    async clickAprovarUsuarioTableBtn(userRow: Locator) {
        await userRow.getByRole('button').nth(1).click();
    }

    async clickReprovarUsuarioTableBtn(userRow: Locator) {
        await userRow.getByRole('button').nth(2).click();
    }

    async clickAprovarUsuarioOverviewBtn() {
        this.page
            .getByRole('button', {
                name: OverviewUsuario.aprovar,
                exact: true,
            })
            .click();
    }

    async clickReprovarUsuarioOverviewBtn() {
        this.page
            .getByRole('button', {
                name: OverviewUsuario.reprovar,
                exact: true,
            })
            .click();
    }

    async findPendingPropRow(codigo: string) {
        const propRow = this.page.locator(`#nova-proposta__${codigo}`);

        const nextPageBtn = this.page
            .locator('app-novas-propostas')
            .getByLabel('Próxima página');

        let [propRowIsVisible, nextPageBtnIsEnabled] = await Promise.all([
            propRow.isVisible(),
            nextPageBtn.isEnabled(),
        ]);

        // Avança a paginação até encontrar o usuário com a razaoSocial informada
        // ou até chegar à ultima página da listagem de usuários pendentes
        while (!propRowIsVisible) {
            if (!nextPageBtnIsEnabled) {
                break;
            }

            await nextPageBtn.click();

            [propRowIsVisible, nextPageBtnIsEnabled] = await Promise.all([
                propRow.isVisible(),
                nextPageBtn.isEnabled(),
            ]);
        }

        if (!propRowIsVisible) {
            return null;
        }

        return propRow;
    }

    async openPropOverview(propRow: Locator) {
        await propRow
            .getByRole('button', { name: 'abrir overview' })
            .first()
            .click();

        return this.page.isVisible('app-overview-propostas-admin');
    }

    async validatePropOverviewFields(
        proposta: IPropostaEntity,
        razaoSocial: string,
        nomeProduto: string
    ) {
        const propFields = proposta.getFields();

        const operation =
            propFields.tipo === TipoDeProposta.Venda
                ? OverviewProposta.tipoVenda
                : OverviewProposta.tipoCompra;

        const statusString = statusDaPropostaToString(proposta.getStatus());

        const fieldsMap = new Map<string, string>([
            ['#proposal-user', razaoSocial],
            ['#proposal-code', propFields.codigo],
            [
                '#qtdy',
                `${propFields.produto.quantidade.valor} ${propFields.produto.quantidade.unidadeMedida}`,
            ],
            ['#price', propFields.precificacao],
            ['#shipment', propFields.periodoEmbarque],
            ['#packing', propFields.produto.ensacamento],
            ['#operation', operation],
            ['#type-of-product', nomeProduto],
            ['#payment-terms', propFields.termosPagamento],
            ['#status', GridPropostas.status[statusString]],
            ['#incoterm', incotermToString(propFields.incoterm)],
        ]);

        let fieldText: string;

        fieldsMap.forEach(async (propFieldValue, fieldID) => {
            fieldText = await this.page.locator(fieldID).textContent();

            try {
                expect(fieldText.includes(propFieldValue)).toBeTruthy();
            } catch (e) {
                logErro(`Valor incorreto para o campo ${fieldID}.
Valor esperado: ${propFieldValue}.
Valor obtido: ${fieldText.replace(/^\w+:/, '')}`);

                throw e;
            }
        });
    }

    async clickAprovarProp(propRow: Locator) {
        await propRow.getByRole('button', { name: 'aprovar proposta' }).click();
    }

    async clickReprovarProp(propRow: Locator) {
        await propRow
            .getByRole('button', { name: 'reprovar proposta' })
            .click();
    }
}
