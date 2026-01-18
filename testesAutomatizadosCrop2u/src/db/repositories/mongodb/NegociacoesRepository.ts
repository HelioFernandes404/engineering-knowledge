import { Collection, Db } from 'mongodb';
import Erro from '@src/handlers/Erro';
import {
    INegociacaoEntity,
    INegociacoesRepository,
} from '@src/interfaces/negociacoes';
import { logErro, logInfo } from '@src/helpers/helpers';
import Negociacao from '@src/db/entities/Negociacao';

export default class NegociacoesRepository implements INegociacoesRepository {
    private collection: Collection;

    constructor(db: Db) {
        logInfo('Instanciando NegociacoesRepository');
        this.collection = db.collection('negociacoes');
    }

    async create(dados: any): Promise<INegociacaoEntity | Erro> {
        try {
            const res = await this.collection.insertOne(dados);

            logInfo(`Negociação criada: ${dados.codigo}`);

            return new Negociacao({
                ...dados,
                id: res.insertedId,
            });
        } catch (e: unknown) {
            return new Erro(
                `Falha ao criar negociação: ${JSON.stringify(dados)}`
            );
        }
    }

    async delete(filtro: { [key: string]: any }): Promise<number | Erro> {
        try {
            const res = await this.collection.deleteOne(filtro);

            if (!res.acknowledged) {
                logInfo(
                    `Falha ao deletar negociação. Filtro: ${JSON.stringify(
                        filtro
                    )}`
                );
            }

            return res.deletedCount;
        } catch (e: unknown) {
            return new Erro(
                `Falha ao deletar negociação. Filtro: ${JSON.stringify(
                    filtro
                )}`,
                e as Error
            );
        }
    }

    async deleteByCodigo(codigo: string): Promise<number | Erro> {
        return await this.delete({ codigo });
    }

    async deleteAll(): Promise<void> {
        logInfo('Removendo todos os registros da coleção "negociacoes"');

        try {
            const res = await this.collection.deleteMany({});

            logInfo(`Total de negociações removidas: ${res.deletedCount}`);
        } catch (e: unknown) {
            logErro(
                'Falha ao remover todos registros da coleção "negociacoes"'
            );
            logErro((e as Error).message);
        }
    }
}
