import { UNIDADE_MEDIDA_QTD_PRODUTO } from '@src/constants/constants';
import { Incoterms, StatusProposta, TipoDeProposta } from '@src/enums/enums';
import Erro from '@src/handlers/Erro';
import { IEntity, IRepository } from './common';

export type TPropostaDoc = {
    codigo: string;
    usuarioId: string;
    produto: {
        codigo: string;
        quantidade: {
            unidadeMedida: typeof UNIDADE_MEDIDA_QTD_PRODUTO;
            valor: number;
        };
        qualidade: string;
        ensacamento: string;
    };
    produtor: string;
    incoterm: Incoterms;
    precificacao: string;
    termosPagamento: string;
    periodoEmbarque: string;
    tipo: TipoDeProposta;
    expiraEm: Date;
};

export interface IPropostaEntity extends IEntity {
    getCodigo(): string;
    getUsuarioId(): string;
    getCodProduto(): string;
    getFields(): TPropostaDoc;
    getStatus(): StatusProposta;
}

export interface IPropostasRepository extends IRepository<IPropostaEntity> {
    deleteByCodigo(codigo: string): Promise<number | Erro>;
    updateStatus(
        codigo: string,
        novoStatus: StatusProposta
    ): Promise<true | Erro>;
    deleteAll(): Promise<void>;
}
