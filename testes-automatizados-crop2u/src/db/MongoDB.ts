import { Db, MongoClient } from 'mongodb';
import { getEnv, logErro, logInfo } from '@src/helpers/helpers';
import Erro from '@src/handlers/Erro';

export default class MongoDB {
    private static dbURI = getEnv('DB_URI');
    private static dbName = getEnv('DB_NAME');
    private static client: MongoClient = new MongoClient(MongoDB.dbURI);
    private static instance: MongoDB | null = null;
    private db: Db;

    private constructor() {
        const db = MongoDB.connect();

        if (db instanceof Erro) {
            throw db;
        }

        logInfo('Conectado ao Banco de Dados.');
        this.db = db;
    }

    getDB() {
        return this.db;
    }

    static getCollection(collectionName: string) {
        return MongoDB.getInstance().getDB().collection(collectionName);
    }

    static getInstance() {
        if (!MongoDB.instance) {
            logInfo('Instanciando MongoDB.');
            MongoDB.instance = new MongoDB();
        }

        return MongoDB.instance;
    }

    static async close() {
        await MongoDB.disconnect();
    }

    private static connect() {
        try {
            return MongoDB.client.db(MongoDB.dbName);
        } catch (e: unknown) {
            MongoDB.disconnect();

            return new Erro(
                '[DB] Falha ao conectar com o banco de dados.',
                e as Error
            );
        }
    }

    private static async disconnect() {
        await MongoDB.client.close().catch(e => {
            logErro('[DB] Erro ao encerrar conexão.');
            logErro(e);
        });

        MongoDB.instance = null;
        logInfo('[DB] Conexão encerrada com sucesso.');
    }
}
