import { logErro } from '@src/helpers/helpers';

export type CustomError = {
	name: string;
	message: string;
};

export default class Erro extends Error {
	status: number;
	erro: CustomError | undefined;

	constructor(msg: string, err?: Error) {
		super(msg);
		this.name = 'Erro';
		this.erro = err;

		logErro(msg);
		if (err?.message) {
			logErro(err.message);
		}
	}
}
