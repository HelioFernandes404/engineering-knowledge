import Erro from '@src/handlers/Erro';
import { IEntity, IRepository } from './common';

export interface ILoginEntity extends IEntity {
	getEmail(): string;
	getRole(): string;
}

export interface ILoginsRepository extends IRepository<ILoginEntity> {
	deleteByEmail(email: string): Promise<number | Erro>;
}
