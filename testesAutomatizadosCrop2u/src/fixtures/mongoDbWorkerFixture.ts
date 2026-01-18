import { test as base } from '@playwright/test';
import MongoDB from '@src/db/MongoDB';
import LoginsRepository from '@src/db/repositories/mongodb/LoginsRepository';
import NegociacoesRepository from '@src/db/repositories/mongodb/NegociacoesRepository';
import ProdutosRepository from '@src/db/repositories/mongodb/ProdutosRepository';
import PropostasRepository from '@src/db/repositories/mongodb/PropostasRepository';
import UsuariosRepository from '@src/db/repositories/mongodb/UsuariosRepository';
import { ILoginsRepository } from '@src/interfaces/logins';
import { INegociacoesRepository } from '@src/interfaces/negociacoes';
import { IProdutosRepository } from '@src/interfaces/produto';
import { IPropostasRepository } from '@src/interfaces/propostas';
import { IUsuariosRepository } from '@src/interfaces/usuarios';
import PropostaMock from '@src/mocks/proposta/PropostaMock';
import UsuarioMock from '@src/mocks/usuario/UsuarioMock';
import { Db } from 'mongodb';

type MongoDbWorkerFixtures = {
    db: Db;

    // Repositories
    loginsRepository: ILoginsRepository;
    usuariosRepository: IUsuariosRepository;
    produtosRepository: IProdutosRepository;
    propostasRepository: IPropostasRepository;
    negociacoesRepository: INegociacoesRepository;

    // Mocks
    usuarioMock: UsuarioMock;
    propostaMock: PropostaMock;
};

const test = base.extend<{}, MongoDbWorkerFixtures>({
    db: [
        async ({}, use) => {
            // Conecta ao banco de dados
            const db = MongoDB.getInstance().getDB();
            //
            //  Usa o banco de dados nos testes
            await use(db);

            // Encerra conexão com o banco de dados
            await MongoDB.close();
        },
        { scope: 'worker', auto: true },
    ],
    loginsRepository: [
        async ({ db }, use) => {
            await use(new LoginsRepository(db));
        },
        { scope: 'worker' },
    ],
    usuariosRepository: [
        async ({ db }, use) => {
            await use(new UsuariosRepository(db));
        },
        { scope: 'worker' },
    ],
    produtosRepository: [
        async ({ db }, use) => {
            await use(new ProdutosRepository(db));
        },
        { scope: 'worker' },
    ],
    propostasRepository: [
        async ({ db }, use) => {
            await use(new PropostasRepository(db));
        },
        { scope: 'worker' },
    ],
    negociacoesRepository: [
        async ({ db }, use) => {
            await use(new NegociacoesRepository(db));
        },
        { scope: 'worker' },
    ],
    usuarioMock: [
        async ({ usuariosRepository, loginsRepository }, use) => {
            await use(new UsuarioMock(usuariosRepository, loginsRepository));
        },
        { scope: 'worker' },
    ],
    propostaMock: [
        async ({ propostasRepository, usuariosRepository }, use) => {
            await use(
                new PropostaMock(propostasRepository, usuariosRepository)
            );
        },
        { scope: 'worker' },
    ],
});

export default test;
