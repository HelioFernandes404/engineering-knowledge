import { IProdutoEntity } from '@src/interfaces/produto';

export default class Produto implements IProdutoEntity {
    private id: string;
    private codigo: string;
    private nome: string;

    constructor(dados: any) {
        this.id = dados.id ?? dados._id;
        this.codigo = dados.codigo;
        this.nome = dados.nome;
    }

    getCodigo(): string {
        return this.codigo;
    }

    getNome(): string {
        return this.nome;
    }

    getID(): string {
        return this.id;
    }
}
