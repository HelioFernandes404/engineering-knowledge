import Erro from '@src/handlers/Erro';
import { IEntity, IRepository } from './common';
import { TDocumentacaoUsuario } from '@src/db/entities/Usuario';
import { StatusAprovacaoUsuario } from '@src/enums/enums';

export interface IUsuarioDoc {
    razaoSocial: string;
    nacionalidade: string;
    documentacao: TDocumentacaoUsuario;
    email: string;
    telefone: string;
    emailVerificado: boolean;
    statusAprovacao: StatusAprovacaoUsuario;
}

export interface IUsuarioEntity extends IEntity {
    getEmail(): string;
    getRazaoSocial(): string;
    getFields(): IUsuarioDoc;
}

export interface IUsuariosRepository extends IRepository<IUsuarioEntity> {
    findByEmail(email: string): Promise<IUsuarioEntity | Erro>;
    deleteByEmail(email: string): Promise<number | Erro>;
    deleteById(id: string): Promise<number | Erro>;
}
