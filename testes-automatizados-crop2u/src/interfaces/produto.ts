import Erro from '@src/handlers/Erro';
import { IEntity, IRepository } from './common';

export type TProdutoDoc = {
    codigo: string;
    nome: string;
};

export interface IProdutoEntity extends IEntity {
    getCodigo(): string;
    getNome(): string;
}

export interface IProdutosRepository extends IRepository<IProdutoEntity> {
    find(codigo: string): Promise<IProdutoEntity | Erro>;
}
