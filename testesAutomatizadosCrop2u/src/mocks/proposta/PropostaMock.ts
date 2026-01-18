import { StatusProposta } from '@src/enums/enums';
import Erro from '@src/handlers/Erro';
import {
    gerarStringAlfanumericaAleatoria,
    randomNumberUpTo,
} from '@src/helpers/helpers';
import { IPropostasRepository } from '@src/interfaces/propostas';
import { IUsuariosRepository } from '@src/interfaces/usuarios';
import {
    TCadastroProposta,
    TPartialCadastroProposta,
    TPropostaFields,
    TPropostaPartialFields,
} from './types';

export default class PropostaMock {
    private propostasRepository: IPropostasRepository;
    private usuariosRepository: IUsuariosRepository;

    private defaultPropData: TPropostaFields = {
        codigo: '',
        usuarioId: '',
        produto: {
            codigo: '',
            quantidade: {
                unidadeMedida: 'MT',
                valor: 0,
            },
            ensacamento: '25 Kg pp bags',
        },
        produtor: 'Nome do Produtor',
        incoterm: 1,
        precificacao: '',
        termosPagamento: 'Texto com termos de pagamento',
        periodoEmbarque: 'Texto com período de embarque',
        expiraEm: new Date(),
        tipo: 1,
        status: StatusProposta.Analise,
    };

    constructor(
        propostasRepo: IPropostasRepository,
        usuariosRepo: IUsuariosRepository
    ) {
        this.propostasRepository = propostasRepo;
        this.usuariosRepository = usuariosRepo;
    }

    /**
     * Cria uma proposta direto no banco de dados.
     *
     * @param emailUsuario E-mail do usuário dono da proposta
     * @param dados - (Opcional) Dados da proposta a ser criada.
     * Cada campo especificado irá substituir os valores default.
     * Caso `dados` seja omitido, será criada uma proposta com dados aleatórios
     * e status 'Em Análise'
     * O campo 'expiraEm' da proposta será atribuído de acordo com o status informado.
     */
    async novaProposta(emailUsuario: string, dados?: TPropostaPartialFields) {
        const randomProp = await this.initRandomProp(
            emailUsuario,
            dados?.status
        );

        if (randomProp instanceof Erro) {
            return randomProp;
        }

        const dadosProposta = dados ? { ...randomProp, ...dados } : randomProp;

        return await this.propostasRepository.create(dadosProposta);
    }

    getDadosCadastroProposta(
        dados?: TPartialCadastroProposta
    ): TCadastroProposta {
        const dadosProposta = dados
            ? { ...this.gerarDadosPropostaAleatoria(), ...dados }
            : this.gerarDadosPropostaAleatoria();

        return dadosProposta;
    }

    private async initRandomProp(
        emailUsuario: string,
        status: StatusProposta = StatusProposta.Analise
    ) {
        const dados = { ...this.defaultPropData };

        const user = await this.usuariosRepository.findByEmail(emailUsuario);

        if (user instanceof Erro) {
            return user;
        }

        dados.codigo = gerarStringAlfanumericaAleatoria(6);
        dados.usuarioId = user.getID();
        dados.produto = this.gerarProdutoAleatorio();
        dados.incoterm = randomNumberUpTo(11) || 1;
        dados.precificacao = `USD ${randomNumberUpTo(5000)}/MT`;
        dados.tipo = randomNumberUpTo(100) % 3 || 1;
        dados.status = status;

        if (
            status === StatusProposta.Aberto ||
            status === StatusProposta.Negociacao
        ) {
            // 24h depois de agora
            dados.expiraEm = new Date(Date.now() + 24 * 60 * 60 * 1000);
        }

        return dados;
    }

    private gerarDadosPropostaAleatoria(): TCadastroProposta {
        return {
            produto: this.gerarProdutoAleatorio(),
            incoterm: randomNumberUpTo(11) || 1,
            precificacao: `USD ${randomNumberUpTo(5000)}/MT`,
            tipo: randomNumberUpTo(100) % 3 || 1,
            produtor: this.defaultPropData.produtor,
            termosPagamento: this.defaultPropData.termosPagamento,
            periodoEmbarque: this.defaultPropData.periodoEmbarque,
        };
    }

    private gerarProdutoAleatorio() {
        const produto = this.defaultPropData.produto;
        produto.codigo = randomNumberUpTo(11).toString().padStart(4, '0');
        produto.quantidade.valor = randomNumberUpTo(150);

        return produto;
    }
}
