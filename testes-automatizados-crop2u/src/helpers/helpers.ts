import { Page, TestInfo } from '@playwright/test';
import Erro from '@src/handlers/Erro';
import { handleUndefined } from '@src/handlers/ExceptionHandler';
import { ILoginsRepository } from '@src/interfaces/logins';
import { IUsuariosRepository } from '@src/interfaces/usuarios';
import { randomBytes } from 'crypto';
import { IPropostasRepository } from '@src/interfaces/propostas';
import { INegociacoesRepository } from '@src/interfaces/negociacoes';
import { LoginPage } from '@pages/login/LoginPage';
import { toastrLogin } from '@pages/login/ui/en/LoginUI';
import { encrypt } from './encryption';
import UsuarioMock from '@src/mocks/usuario/UsuarioMock';
import { Incoterms, StatusProposta, TipoDeProposta } from '@src/enums/enums';

export function getEnv(key: string): string {
    return process.env[key] ?? handleUndefined(key);
}

export function logInfo(msg: string) {
    console.log(`>> [INFO]: ${msg}`);
}

export function logErro(msg: string) {
    console.error(`>> [ERR]: ${msg}`);
}

export function logTestInfo(info: TestInfo) {
    console.log(
        `\n[${info.project.name} #${info.parallelIndex}/${info.workerIndex}]:`,
        info.title
    );
}

/**
 * Remove registros do banco de dados de logins e de usuários
 * associados ao email informado.
 *
 * Retorna 1 caso registros tenham sido removidos com sucesso
 * Retorna 0 caso não sejam encontrados registros associados ao email informado
 * Retorna instância de 'Erro' em caso de falha
 */
export async function deleteUser(
    email: string,
    loginsRepo: ILoginsRepository,
    usuariosRepo: IUsuariosRepository
) {
    logInfo(`Removendo usuário da base dados: ${email}`);

    const res = await usuariosRepo.deleteByEmail(email);

    if (res instanceof Erro) {
        return res;
    }

    return await loginsRepo.deleteByEmail(email);
}

/**
 * Função utilizada para gerar o código identificador de propostas e negociações
 * Para propostas tamanho deve ser 6 e para negociações tamanho deve ser 8
 */
export const gerarStringAlfanumericaAleatoria = (tamanho: number) => {
    return randomBytes(1.5 * tamanho) // 1.5x maior para em seguida remover caracteres não alfanuméricos
        .toString('base64')
        .replace(/[+/=]/g, '')
        .slice(0, tamanho);
};

/**
 * Gerador de número aleatório entre 0 e maxNumber inclusive.
 * Exemplo: randomNumerUpTo(4) irá gerar um número aleatório que pode ser
 * 0, 1, 2, 3 ou 4
 */
export const randomNumberUpTo = (maxNumber: number) =>
    Math.floor(maxNumber * (1 - Math.random()));

/**
 * Deleta todas as propostas e todas as negociações do banco de dados
 */
export const deleteAllPropostas = async (
    propostasRepo: IPropostasRepository,
    negociacoesRepo: INegociacoesRepository
) => {
    await negociacoesRepo.deleteAll();
    await propostasRepo.deleteAll();
};

/**
 * Efetua fluxo de login como usuário Administrador
 */
export const loginAsAdmin = async (page: Page) => {
    const loginPage = new LoginPage(page);

    await loginPage.visit();
    await loginPage.preencherFormularioLogin(
        getEnv('USER_ADMIN'),
        getEnv('PWD_ADMIN')
    );
    await loginPage.submitLogin();

};

/**
 * Insere usuários aleatórios, únicos e distintos, diretamente no banco de dados
 * @param qtdDeUsuarios - Total de usuários a serem inseridos (Default: 1)
 * @param usuarioMock - Instância de UsuarioMock
 */
export const cadastrarUsuariosAleatorios = async (
    usuarioMock: UsuarioMock,
    qtdDeUsuarios: number = 1
) => {
    for (const i of Array.from({ length: qtdDeUsuarios }, (_, i) => i)) {
        if (i % 2 === 0) {
            await usuarioMock.novoUsuario();
        } else {
            await usuarioMock.novoUsuarioEstrangeiro();
        }
    }
};

export const encriptarSenha = async (senha: string) => {
    return await encrypt(senha);
};

export const tipoDePropostaToString = (tipo: TipoDeProposta) => {
    const tiposDeProposta = new Map([
        [TipoDeProposta.Venda, 'Venda'],
        [TipoDeProposta.Compra, 'Compra'],
    ]);

    return tiposDeProposta.get(tipo) ?? '';
};

export const statusDaPropostaToString = (tipo: StatusProposta) => {
    const statusDaProposta = new Map([
        [StatusProposta.Analise, 'UNDER-REVIEW'],
        [StatusProposta.Aberto, 'AVAILABLE'],
        [StatusProposta.Negociacao, 'DEALING'],
        [StatusProposta.Finalizada, 'FINISHED'],
        [StatusProposta.Suspensa, 'SUSPENDED'],
        [StatusProposta.Cancelada, 'CANCELED'],
        [StatusProposta.Expirada, 'EXPIRED'],
        [StatusProposta.Reprovada, 'CANCELED'],
    ]);
    return statusDaProposta.get(tipo);
};

export const incotermToString = (tipo: Incoterms) => {
    const incoterm = new Map([
        [Incoterms.EXW, 'EXW'],
        [Incoterms.FCA, 'FCA'],
        [Incoterms.FAS, 'FAS'],
        [Incoterms.FOB, 'FOB'],
        [Incoterms.CPT, 'CPT'],
        [Incoterms.CIP, 'CIP'],
        [Incoterms.CFR, 'CFR'],
        [Incoterms.CIF, 'CIF'],
        [Incoterms.DAP, 'DAP'],
        [Incoterms.DPU, 'DPU'],
        [Incoterms.DDP, 'DDP'],
    ]);

    return incoterm.get(tipo) ?? '';
};

/** Helper para exibir de forma mais legível a tipagem de objetos.
 *
 * Exemplo:
 * type Intersected = Prettify<
 *      { a: string; } & { b: number; } & { c: boolean; }
 * >;
 *
 * Resultado ao fazer hover em um objeto do tipo Intersected:
 * {
 *   a: string;
 *   b: number;
 *   c: boolean;
 * }
 * */
export type Prettify<T> = {
    [K in keyof T]: T[K];
} & {};
