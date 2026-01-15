import {
    NACIONALIDADE_BR,
    NACIONALIDADE_RUSSA,
} from '@src/constants/constants';
import Usuario, { TDocumentacaoUsuario } from '@src/db/entities/Usuario';
import { Role, StatusAprovacaoUsuario } from '@src/enums/enums';
import Erro from '@src/handlers/Erro';
import {
    encriptarSenha,
    gerarStringAlfanumericaAleatoria,
    getEnv,
    logInfo,
    randomNumberUpTo,
} from '@src/helpers/helpers';
import { ILoginsRepository } from '@src/interfaces/logins';
import { IUsuariosRepository } from '@src/interfaces/usuarios';
import {
    TCadastroUsuarioBR,
    TCadastroUsuarioEstrangeiro,
    TNovoUsuarioOptions,
    TPartialCadastroUsuarioBR,
    TPartialCadastroUsuarioEstrangeiro,
    TUsuarioFields,
} from './types';

export default class UsuarioMock {
    private usuariosRepository: IUsuariosRepository;
    private loginsRepository: ILoginsRepository;

    private defaultUserData: TUsuarioFields = {
        razaoSocial: '',
        email: '',
        senha: getEnv('PWD_CLIENT'),
        telefone: '123456789',
        nacionalidade: NACIONALIDADE_BR,
        documentacao: {},
        emailVerificado: true,
        statusAprovacao: StatusAprovacaoUsuario.Pendente,
    };

    constructor(
        usuariosRepository: IUsuariosRepository,
        loginsRepository: ILoginsRepository
    ) {
        this.usuariosRepository = usuariosRepository;
        this.loginsRepository = loginsRepository;
    }

    /**
     *
     * Insere um usuário na base de dados.
     *
     * @param opts - {
     *  dados: Dados do usuário. Quaisquer campos informados irão sobrescrever
     *  os dados default e campos não informados irão utilizar o default.
     *  Não há necessidade de especificar todos os campos do usuário, apenas o(s)
     *  campo(s) desejado(s)
     *
     *  withLogin: Indica se este usuarío será utilizado pra fazer login no sistema
     * }
     *
     * - Caso opts.dados não seja especificado, valores default serão utilizados criando
     *   um usuário brasileiro com e-mail verificado e pendente de aprovação pelo admin
     *
     * - Caso opts.withLogin não seja especificado, não será criado um registro na tabela
     * de logins, impossibilitando utilizar este usuário para fazer login no sistema.
     */
    async novoUsuario(opts: TNovoUsuarioOptions = { withLogin: false }) {
        const dados = opts.dados
            ? { ...this.initRandomUser(), ...opts.dados }
            : this.initRandomUser();

        const { withLogin } = opts;

        const usuario = await this.usuariosRepository.create(
            new Usuario(dados).getFields()
        );

        if (usuario instanceof Erro) {
            return usuario;
        }

        logInfo(
            `Usuário inserido na base dados: ${usuario.getEmail()} (${usuario.getID()})`
        );

        if (withLogin) {
            const senhaEncriptada = await encriptarSenha(dados.senha);

            const login = await this.loginsRepository.create({
                email: usuario.getEmail(),
                senha: senhaEncriptada,
                refId: usuario.getID(),
                role: Role.usuario,
            });

            if (login instanceof Erro) {
                return login;
            }

            logInfo(`Login inserido na base dados: ${usuario.getEmail()}`);
        }

        return usuario;
    }

    /**
     *
     * Insere um usuário estrangeiro na base de dados.
     *
     * @param opts - {
     *  dados: (Opcional) Dados do usuário. Quaisquer campos informados irão sobrescrever
     *  os dados default e campos não informados irão utilizar o default.
     *  Não há necessidade de especificar todos os campos do usuário, apenas o(s)
     *  campo(s) desejado(s)
     *
     *  withLogin: (Opcional) Indica se este usuarío será utilizado pra fazer login no sistema
     * }
     *
     * - Caso opts.dados não seja especificado, valores default serão utilizados criando
     *   um usuário estrangeiro com e-mail verificado e pendente de aprovação pelo admin
     *
     * - Caso opts.withLogin não seja especificado, não será criado um registro na tabela
     * de logins, impossibilitando utilizar este usuário para fazer login no sistema.
     */
    async novoUsuarioEstrangeiro(
        opts: TNovoUsuarioOptions = { withLogin: false }
    ) {
        const dados = this.initRandomUser({ isUsuarioBr: false });

        return await this.novoUsuario({ dados, withLogin: opts.withLogin });
    }

    async novoUsuarioAprovado(
        opts: TNovoUsuarioOptions = { withLogin: false }
    ) {
        const dados = this.initRandomUser();
        dados.statusAprovacao = StatusAprovacaoUsuario.Aprovado;

        return await this.novoUsuario({ dados, withLogin: opts.withLogin });
    }

    /**
     *
     * Retorna um objeto com os dados correspondentes aos campos
     * do cadastro de um novo usuário brasileiro
     *
     * @param dados - (Opcional) Quaisquer campos informados neste parâmetro irão
     * sobrescrever os valores default
     *
     * Exemplo:
     * Substitui o email default gerado aleatoriamente por 'xpto@mail.com'
     * > getDadosCadastroNovoUsuarioBR({email: 'xpto@mail.com'})
     */
    getDadosCadastroUsuarioBR(
        dados?: TPartialCadastroUsuarioBR
    ): TCadastroUsuarioBR {
        const dadosUsuario = dados
            ? { ...this.initRandomUser(), ...dados }
            : this.initRandomUser();

        return {
            razaoSocial: dadosUsuario.razaoSocial,
            cnpj: dadosUsuario.documentacao.cnpj,
            cnae: dadosUsuario.documentacao.cnae,
            email: dados?.confirmarEmail ?? dadosUsuario.email,
            confirmarEmail: dadosUsuario.email,
            telefone: dadosUsuario.telefone,
            senha: dadosUsuario.senha,
            confirmarSenha: dados?.confirmarSenha ?? dadosUsuario.senha,
        };
    }

    /**
     *
     * Retorna um objeto com os dados correspondentes aos campos
     * do cadastro de um novo usuário estrangeiro
     *
     * @param dados - (Opcional) Quaisquer campos informados neste parâmetro irão
     * sobrescrever os valores default
     */
    getDadosUsuarioEstrangeiro(
        dados?: TPartialCadastroUsuarioEstrangeiro
    ): TCadastroUsuarioEstrangeiro {
        const dadosUsuario = dados
            ? { ...this.initRandomUser({ isUsuarioBr: false }), ...dados }
            : this.initRandomUser({ isUsuarioBr: false });

        return {
            razaoSocial: dadosUsuario.razaoSocial,
            atividade: dadosUsuario.documentacao.atividade,
            documentoEst: dadosUsuario.documentacao.documentoEst,
            email: dadosUsuario.email,
            confirmarEmail: dados?.confirmarEmail ?? dadosUsuario.email,
            telefone: dadosUsuario.telefone,
            senha: dadosUsuario.senha,
            confirmarSenha: dados?.confirmarSenha ?? dadosUsuario.senha,
        };
    }

    private gerarRazaoSocialAletario(uniqueID: string) {
        return `QA Testes Automatizados - ${uniqueID}`;
    }

    private gerarEmailAleatorio(uniqueID: string) {
        return `crop2u-qa-${uniqueID}@devnullmail.com`;
    }

    private gerarCnpjAleatorio() {
        return `${randomNumberUpTo(1000)}${randomNumberUpTo(
            1000
        )}${randomNumberUpTo(1000)}`.padEnd(14, '0');
    }

    private gerarDocumentoEstrangeiroAleatorio() {
        return `${randomNumberUpTo(100)}${randomNumberUpTo(1000)}`.padEnd(
            7,
            '0'
        );
    }

    private initDocumentacao(nacionalidade: string): TDocumentacaoUsuario {
        const atividade = 'Testes automatizados';

        if (nacionalidade === NACIONALIDADE_BR) {
            return {
                atividade,
                cnae: '1234567',
                cnpj: this.gerarCnpjAleatorio(),
            };
        }

        return {
            atividade,
            documentoEst: {
                tipo: randomNumberUpTo(4) || 1, // Número de 1 a 4 inclusive
                dados: this.gerarDocumentoEstrangeiroAleatorio(),
            },
        };
    }

    private initRandomUser(
        opts: { isUsuarioBr: boolean } = { isUsuarioBr: true }
    ): TUsuarioFields {
        const uniqueID = gerarStringAlfanumericaAleatoria(8);
        const dados = { ...this.defaultUserData };

        dados.razaoSocial = this.gerarRazaoSocialAletario(uniqueID);
        dados.email = this.gerarEmailAleatorio(uniqueID);
        dados.nacionalidade = opts.isUsuarioBr
            ? NACIONALIDADE_BR
            : NACIONALIDADE_RUSSA;
        dados.documentacao = this.initDocumentacao(dados.nacionalidade);

        return dados;
    }
}
