import { StatusNegociacao } from '@src/enums/enums';
import { gerarStringAlfanumericaAleatoria } from '@src/helpers/helpers';
import { INegociacaoEntity } from '@src/interfaces/negociacoes';
import Proposta from './Proposta';
import Usuario from './Usuario';

export default class Negociacao implements INegociacaoEntity {
    private id: string;
    private usuario: Usuario;
    private usuarioId: string;
    private proposta: Proposta;
    private propostaCod: string;
    private codigo: string;
    private termos: string;
    private status: StatusNegociacao;
    private novasMsgs: number;
    private novasMsgsIDs: { id: string; delivered: boolean }[];

    constructor(dados: any) {
        this.id = dados.id;
        this.usuario = dados.usuario;
        this.usuarioId = dados.usuarioId ?? '';
        this.proposta = dados.proposta;
        this.propostaCod = dados.propostaCod ?? '';
        this.termos = dados.termos;
        this.codigo = dados.codigo ?? gerarStringAlfanumericaAleatoria(8);
        this.status = dados.status ?? StatusNegociacao.Analise;
        this.novasMsgs = dados.novasMsgs?.length ?? 0;
        this.novasMsgsIDs = dados.novasMsgs ?? [];
    }

    getCodigo(): string {
        return this.codigo;
    }

    getUsuarioId(): string {
        return this.usuario?.getID() ?? this.usuarioId?.toString();
    }

    getCodProposta(): string {
        return this.proposta?.getCodigo() ?? this.propostaCod;
    }

    getID(): string {
        return this.id;
    }
}
