import Erro from '@src/handlers/Erro';
import { IEntity, IRepository } from './common';

export interface INegociacaoEntity extends IEntity {
    getCodigo(): string;
    getUsuarioId(): string;
    getCodProposta(): string;
}

export interface INegociacoesRepository extends IRepository<INegociacaoEntity> {
    deleteByCodigo(codigo: string): Promise<number | Erro>;
    deleteAll(): Promise<void>;
}
