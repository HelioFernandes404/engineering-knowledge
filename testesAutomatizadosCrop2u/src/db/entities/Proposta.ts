import { UNIDADE_MEDIDA_QTD_PRODUTO } from '@src/constants/constants';
import { Incoterms, StatusProposta, TipoDeProposta } from '@src/enums/enums';
import { gerarStringAlfanumericaAleatoria } from '@src/helpers/helpers';
import { IPropostaEntity, TPropostaDoc } from '@src/interfaces/propostas';

export type TQtdProduto = {
    unidadeMedida: typeof UNIDADE_MEDIDA_QTD_PRODUTO;
    valor: number;
};

export type TProdutoProposta = {
    codigo: string; // Type of Product
    quantidade: TQtdProduto; // Quantity
    qualidade: string;
    ensacamento: string; // Packing
};

export default class Proposta implements IPropostaEntity {
    private id: string;
    private codigo: string;
    private usuarioId: string;
    private produto: TProdutoProposta;
    private precificacao: string;
    private termosPagamento: string;
    private periodoEmbarque: string;
    private tipo: TipoDeProposta;
    private status: StatusProposta;
    private produtor: string;
    private expiraEm: Date;
    private incoterm: Incoterms;

    constructor(dados: any) {
        this.id = dados.id;
        this.codigo = dados.codigo ?? gerarStringAlfanumericaAleatoria(6);
        this.usuarioId = dados.usuarioId;
        this.produto = dados.produto;
        this.precificacao = dados.precificacao;
        this.termosPagamento = dados.termosPagamento;
        this.periodoEmbarque = dados.periodoEmbarque;
        this.tipo = dados.tipo;
        this.status = dados.status;
        this.produtor = dados.produtor;
        this.expiraEm = dados.expiraEm ?? new Date(); // Agora
        this.incoterm = dados.incoterm;
    }

    getFields(): TPropostaDoc {
        return {
            codigo: this.codigo,
            usuarioId: this.usuarioId,
            produto: this.produto,
            produtor: this.produtor,
            incoterm: this.incoterm,
            precificacao: this.precificacao,
            termosPagamento: this.termosPagamento,
            periodoEmbarque: this.periodoEmbarque,
            tipo: this.tipo,
            expiraEm: this.expiraEm,
        };
    }

    getCodProduto(): string {
        return this.produto.codigo;
    }

    getUsuarioId(): string {
        return this.usuarioId;
    }

    getCodigo(): string {
        return this.codigo;
    }

    getID(): string {
        return this.id;
    }

    getStatus(): StatusProposta {
        return this.status;
    }
}
