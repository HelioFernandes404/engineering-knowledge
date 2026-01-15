import { Collection, Db } from 'mongodb';
import Erro from '@src/handlers/Erro';
import {
    IPropostaEntity,
    IPropostasRepository,
} from '@src/interfaces/propostas';
import { logErro, logInfo } from '@src/helpers/helpers';
import MongoDB from '@src/db/MongoDB';
import Proposta from '@src/db/entities/Proposta';
import { StatusProposta } from '@src/enums/enums';

export default class PropostasRepository implements IPropostasRepository {
    private collection: Collection;
    private produtosCollection: Collection;

    constructor(db: Db) {
        logInfo('Instanciando PropostasRepository');
        this.collection = db.collection('propostas');
        this.produtosCollection = db.collection('produtos');
    }

    async create(dados: any): Promise<IPropostaEntity | Erro> {
        try {
            const produto = await this.produtosCollection.findOne({
                codigo: dados.produto.codigo,
            });

            if (!produto) {
                return new Erro(
                    `Produto inválido. Código informado: ${dados.produto.codigo}`
                );
            }

            const res = await this.collection.insertOne(dados);

            logInfo(`Proposta criada: ${dados.codigo}`);

            return new Proposta({
                ...dados,
                id: res.insertedId,
            });
        } catch (e: unknown) {
            return new Erro(
                `Falha ao criar proposta: ${JSON.stringify(dados)}`,
                e as Error
            );
        }
    }

    async updateStatus(codigo: string, novoStatus: StatusProposta) {
        let expiraEm = new Date(); // Agora

        if (
            [StatusProposta.Aberto, StatusProposta.Negociacao].includes(
                novoStatus
            )
        ) {
            // 24h depois de agora
            expiraEm = new Date(Date.now() + 24 * 60 * 60 * 1000);
        }

        try {
            const res = await this.collection.updateOne(
                { codigo },
                {
                    $set: {
                        status: novoStatus,
                        expiraEm,
                    },
                }
            );

            if (!res.acknowledged || res.modifiedCount === 0) {
                return new Erro(
                    `Falha ao alterar status da proposta ${codigo}. Resposta: ${JSON.stringify(
                        res
                    )}`
                );
            }

            return true;
        } catch (e: unknown) {
            return new Erro(
                `Falha ao alterar status da proposta ${codigo}`,
                e as Error
            );
        }
    }

    async deleteByCodigo(codigo: string): Promise<number | Erro> {
        return await this.delete({ codigo });
    }

    async delete(filtro: { [key: string]: any }): Promise<number | Erro> {
        try {
            const res = await this.collection.deleteOne(filtro);

            if (!res.acknowledged) {
                logInfo(
                    `Falha ao deletar proposta. Filtro: ${JSON.stringify(
                        filtro
                    )}`
                );
            }

            if (res.deletedCount > 0) {
                logInfo(
                    `Proposta removida da base de dados: ${JSON.stringify(
                        filtro
                    )}`
                );
            }

            return res.deletedCount;
        } catch (e: unknown) {
            return new Erro(
                `Falha ao deletar proposta. Filtro: ${JSON.stringify(filtro)}`,
                e as Error
            );
        }
    }

    async deleteAll(): Promise<void> {
        logInfo('Removendo todos os registros da coleção "propostas"');

        try {
            const res = await this.collection.deleteMany({});

            logInfo(`Total de propostas removidas: ${res.deletedCount}`);
        } catch (e: unknown) {
            logErro('Falha ao remover todos registros da coleção "propostas"');
            logErro((e as Error).message);
        }
    }
}
