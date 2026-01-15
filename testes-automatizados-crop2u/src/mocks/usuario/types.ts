import { TDocumentacaoUsuario } from '@src/db/entities/Usuario';
import {
    StatusAprovacaoUsuario,
    TipoDocumentoEstrangeiro,
} from '@src/enums/enums';
import { Prettify } from '@src/helpers/helpers';

export type TUsuarioFields = {
    razaoSocial: string;
    email: string;
    senha: string;
    telefone: string;
    nacionalidade: string;
    documentacao: TDocumentacaoUsuario;
    emailVerificado: boolean;
    statusAprovacao: StatusAprovacaoUsuario;
};

export type TCadastroUsuarioBR = {
    razaoSocial: string;
    cnpj: string;
    cnae: string;
    email: string;
    confirmarEmail: string;
    telefone: string;
    senha: string;
    confirmarSenha: string;
};

export type TCadastroUsuarioEstrangeiro = Prettify<
    Omit<TCadastroUsuarioBR, 'cnpj' | 'cnae'> & {
        atividade: string;
        documentoEst: { tipo: TipoDocumentoEstrangeiro; dados: string };
    }
>;

export type TUsuarioPartialFields = Prettify<Partial<TUsuarioFields>>;

export type TPartialCadastroUsuarioBR = Prettify<Partial<TCadastroUsuarioBR>>;

export type TPartialCadastroUsuarioEstrangeiro = Prettify<
    Partial<TCadastroUsuarioEstrangeiro>
>;

export type TNovoUsuarioOptions = {
    dados?: TUsuarioPartialFields;
    withLogin?: boolean;
};
