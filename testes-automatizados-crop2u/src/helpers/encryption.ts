import { CustomError } from '@src/handlers/Erro';
import { hash } from 'bcrypt';

export class EncryptionError extends Error {
    erro: CustomError;

    constructor(msg: string, err: Error) {
        super(msg);
        this.name = 'EncryptionError';
        this.erro = err;
    }
}

export const encrypt = async (dado: string) => {
    let encriptado: string = '';

    try {
        encriptado = await hash(dado, 10);

        return encriptado;
    } catch (e: unknown) {
        const msg = 'Erro ao gerar hash da senha.';
        console.error(msg, e);

        throw new EncryptionError(msg, e as Error);
    }
};
