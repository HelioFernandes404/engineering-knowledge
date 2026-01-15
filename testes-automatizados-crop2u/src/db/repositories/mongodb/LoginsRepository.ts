import { Collection, Db } from 'mongodb';
import Erro from '@src/handlers/Erro';
import { logInfo } from '@src/helpers/helpers';
import { ILoginEntity, ILoginsRepository } from '@src/interfaces/logins';
import Login from '@src/db/entities/Login';

export default class LoginsRepository implements ILoginsRepository {
    private collection: Collection;

    constructor(db: Db) {
        logInfo('Instanciando LoginsRepository');
        this.collection = db.collection('logins');
    }

    async create(dados: any): Promise<ILoginEntity | Erro> {
        try {
            const res = await this.collection.insertOne(dados);

            return new Login({ ...dados, id: res.insertedId });
        } catch (e: unknown) {
            return new Erro(
                `Falha ao criar login: ${JSON.stringify(dados)}`,
                e as Error
            );
        }
    }

    async deleteByEmail(email: string): Promise<number | Erro> {
        return await this.delete({ email });
    }

    async delete(filtro: { [key: string]: any }): Promise<number | Erro> {
        try {
            const res = await this.collection.deleteOne(filtro);

            if (!res.acknowledged) {
                logInfo(
                    `Falha ao deletar login. Filtro: ${JSON.stringify(filtro)}`
                );
            }

            return res.deletedCount;
        } catch (e: unknown) {
            return new Erro(
                `Falha ao deletar login. Filtro: ${JSON.stringify(filtro)}`,
                e as Error
            );
        }
    }
}
