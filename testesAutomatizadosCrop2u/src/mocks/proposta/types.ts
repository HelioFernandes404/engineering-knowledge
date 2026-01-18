import { Incoterms, StatusProposta, TipoDeProposta } from '@src/enums/enums';
import { Prettify } from '@src/helpers/helpers';

export type TPropostaFields = {
    codigo: string;
    usuarioId: string;
    produto: {
        codigo: string;
        quantidade: {
            unidadeMedida: 'MT';
            valor: number;
        };
        ensacamento: string;
    };
    produtor: string;
    incoterm: Incoterms;
    precificacao: string;
    termosPagamento: string;
    periodoEmbarque: string;
    expiraEm: Date;
    tipo: TipoDeProposta;
    status: StatusProposta;
};

export type TCadastroProposta = Prettify<
    Omit<TPropostaFields, 'codigo' | 'usuarioId' | 'expiraEm' | 'status'>
>;

export type TPropostaPartialFields = Prettify<Partial<TPropostaFields>>;

export type TPartialCadastroProposta = Prettify<Partial<TCadastroProposta>>;
