import Erro from '@src/handlers/Erro';

export interface IEntity {
	getID(): string;
}

export interface IRepository<T extends IEntity> {
	create(dados: any): Promise<T | Erro>;
	delete(filtro: { [key: string]: any }): Promise<number | Erro>;
}
