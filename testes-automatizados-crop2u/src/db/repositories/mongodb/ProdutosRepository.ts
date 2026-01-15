import Produto from '@src/db/entities/Produto';
import Erro from '@src/handlers/Erro';
import { logInfo } from '@src/helpers/helpers';
import { IProdutoEntity, IProdutosRepository } from '@src/interfaces/produto';
import { Collection, Db } from 'mongodb';

export default class ProdutosRepository implements IProdutosRepository {
    private collection: Collection;

    constructor(db: Db) {
        logInfo('Instanciando ProdutosRepository');
        this.collection = db.collection('produtos');
    }

    async find(codigo: string): Promise<IProdutoEntity | Erro> {
        try {
            const res = await this.collection.findOne({ codigo });

            if (!res) {
                return new Erro(
                    `Nenhum produto encontrado com o código: ${codigo}`
                );
            }

            return new Produto(res);
        } catch (e: unknown) {
            return new Erro(`Falha ao buscar produto: ${codigo}`, e as Error);
        }
    }

    create(dados: any): Promise<IProdutoEntity | Erro> {
        throw new Error('Method not implemented.');
    }

    delete(filtro: { [key: string]: any }): Promise<number | Erro> {
        throw new Error('Method not implemented.');
    }
}
