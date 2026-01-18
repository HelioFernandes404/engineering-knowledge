import { Collection, Db, ObjectId } from 'mongodb';
import Erro from '@src/handlers/Erro';
import { logInfo } from '@src/helpers/helpers';
import { IUsuarioEntity, IUsuariosRepository } from '@src/interfaces/usuarios';
import MongoDB from '@src/db/MongoDB';
import Usuario from '@src/db/entities/Usuario';

export default class UsuariosRepository implements IUsuariosRepository {
    private collection: Collection;

    constructor(db: Db) {
        logInfo('Instanciando UsuariosRepository');
        this.collection = db.collection('usuarios');
    }

    async create(dados: any): Promise<IUsuarioEntity | Erro> {
        try {
            const res = await this.collection.insertOne(dados);

            if (!res.acknowledged) {
                return new Erro(
                    `Falha ao inserir usuário: ${JSON.stringify(dados)}`
                );
            }

            return new Usuario({ ...dados, id: res.insertedId });
        } catch (e: unknown) {
            return new Erro(
                `Falha ao inserir usuário: ${JSON.stringify(dados)}`,
                e as Error
            );
        }
    }

    async findByEmail(email: string): Promise<IUsuarioEntity | Erro> {
        try {
            const res = await this.collection.findOne({ email });

            if (!res) {
                return new Erro(
                    `Nenhum usuário encontrado com o e-mail: ${email}`
                );
            }

            return new Usuario(res);
        } catch (e: unknown) {
            return new Erro(
                `Falha ao buscar usuário. Email informado: ${email}`,
                e as Error
            );
        }
    }

    async delete(filtro: { [key: string]: any }): Promise<number | Erro> {
        try {
            const res = await this.collection.deleteOne(filtro);

            if (!res.acknowledged) {
                logInfo(
                    `Falha ao deletar usuário. Filtro: ${JSON.stringify(
                        filtro
                    )}`
                );
            }

            if (res.deletedCount > 0) {
                logInfo(
                    `Usuário removido da base de dados: ${JSON.stringify(
                        filtro
                    )}`
                );
            }

            return res.deletedCount;
        } catch (e: unknown) {
            return new Erro(
                `Falha ao deletar usuário. Filtro: ${JSON.stringify(filtro)}`,
                e as Error
            );
        }
    }

    async deleteByEmail(email: string) {
        return await this.delete({ email });
    }

    async deleteById(id: string) {
        return await this.delete({ _id: new ObjectId(id) });
    }
}
