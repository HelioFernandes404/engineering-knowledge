import { NACIONALIDADE_BR } from '@src/constants/constants';
import {
    StatusAprovacaoUsuario,
    TipoDocumentoEstrangeiro,
} from '@src/enums/enums';
import { IUsuarioDoc, IUsuarioEntity } from '@src/interfaces/usuarios';

export type TDocumentacaoUsuario = {
    cnae?: string;
    cnpj?: string;
    atividade?: string;
    documentoEst?: {
        tipo: TipoDocumentoEstrangeiro;
        dados: string;
    };
};

export default class Usuario implements IUsuarioEntity {
    private id: string;
    private razaoSocial: string;
    private email: string;
    private telefone: string;
    private nacionalidade: string;
    private documentacao: TDocumentacaoUsuario;
    private emailVerificado: boolean;
    private statusAprovacao: StatusAprovacaoUsuario;

    constructor(dados: any) {
        this.id = dados.id ?? dados._id;
        this.razaoSocial = dados.razaoSocial;
        this.email = dados.email;
        this.telefone = dados.telefone;
        this.nacionalidade = dados.nacionalidade;
        this.documentacao = this.formatarDocumentacao(dados);
        this.emailVerificado = dados.emailVerificado ?? false;
        this.statusAprovacao =
            dados.statusAprovacao ?? StatusAprovacaoUsuario.Pendente;
    }

    getID(): string {
        return this.id;
    }

    getEmail(): string {
        return this.email;
    }

    getRazaoSocial(): string {
        return this.razaoSocial;
    }

    /**
     * Retorna os campos esperados pelo banco de dados para criar um novo usuário
     */
    getFields(): IUsuarioDoc {
        return {
            razaoSocial: this.razaoSocial,
            nacionalidade: this.nacionalidade,
            documentacao: this.documentacao,
            email: this.email,
            telefone: this.telefone,
            emailVerificado: this.emailVerificado,
            statusAprovacao: this.statusAprovacao,
        };
    }

    private formatarDocumentacao(dados: any): TDocumentacaoUsuario {
        if (!dados.nacionalidade) {
            return undefined;
        }

        if (dados.nacionalidade === NACIONALIDADE_BR) {
            return {
                cnae: dados.documentacao.cnae,
                cnpj: dados.documentacao.cnpj,
                atividade: dados.documentacao.atividade,
            };
        }

        return {
            atividade: dados.documentacao.atividade,
            documentoEst: dados.documentacao.documentoEst,
        };
    }
}
