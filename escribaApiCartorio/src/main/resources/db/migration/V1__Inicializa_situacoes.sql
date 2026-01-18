-- Criação da tabela de situações do cartório
CREATE TABLE tb_situacaos (
                              id VARCHAR(20) PRIMARY KEY,
                              nome VARCHAR(50) NOT NULL UNIQUE
);

-- Criação da tabela de atribuições do cartório
CREATE TABLE tb_atribuicaos (
                                id VARCHAR(20) PRIMARY KEY,
                                nome VARCHAR(50) NOT NULL UNIQUE,
                                situacao BOOLEAN NOT NULL DEFAULT TRUE
);

-- Criação da tabela de cartórios
CREATE TABLE tb_cartorios (
                              id INT AUTO_INCREMENT PRIMARY KEY,
                              nome VARCHAR(150) NOT NULL UNIQUE,
                              observacao VARCHAR(250),
                              situacao_id VARCHAR(20),
                              FOREIGN KEY (situacao_id) REFERENCES tb_situacaos(id)
);

-- Criação da tabela de associação entre cartórios e atribuições
CREATE TABLE cartorio_atribuicao (
                                     cartorio_id INT,
                                     atribuicao_id VARCHAR(20),
                                     PRIMARY KEY (cartorio_id, atribuicao_id),
                                     FOREIGN KEY (cartorio_id) REFERENCES tb_cartorios(id),
                                     FOREIGN KEY (atribuicao_id) REFERENCES tb_atribuicaos(id)
);

-- Inserção das situações iniciais
INSERT INTO tb_situacaos (id, nome) VALUES ('SIT_ATIVO', 'Ativo');
INSERT INTO tb_situacaos (id, nome) VALUES ('SIT_BLOQUEADO', 'Bloqueado');

-- Inserção de atribuições genéricas
INSERT INTO tb_atribuicaos (id, nome) VALUES ('ATR_REGISTRO', 'Registro de Imóveis');
INSERT INTO tb_atribuicaos (id, nome) VALUES ('ATR_NOTARIA', 'Notarização de Documentos');
INSERT INTO tb_atribuicaos (id, nome) VALUES ('ATR_CERTIDOES', 'Emissão de Certidões');
INSERT INTO tb_atribuicaos (id, nome) VALUES ('ATR_PROCESSOS', 'Processos Judiciais');

-- Inserção de um cartório com uma atribuição
-- Como o H2 não suporta LAST_INSERT_ID(), vamos usar uma sequência para gerar o ID do cartório
CREATE SEQUENCE cartorio_id_seq;
INSERT INTO tb_cartorios (id, nome, observacao, situacao_id) VALUES (NEXT VALUE FOR cartorio_id_seq, 'Cartório Central', 'Oferece serviços de registro, notarização e emissão de certidões.', 'SIT_ATIVO');
INSERT INTO tb_cartorios (id, nome, observacao, situacao_id) VALUES (NEXT VALUE FOR cartorio_id_seq, 'Cartório Novo Sol', 'Oferece serviços de registro, notarização e emissão de certidões da salvação.', 'SIT_ATIVO');

-- Associando atribuições ao cartório
-- Como não podemos usar LAST_INSERT_ID(), vamos assumir que o ID do cartório é 1 (ou o próximo valor da sequência)
INSERT INTO cartorio_atribuicao (cartorio_id, atribuicao_id) VALUES (1, 'ATR_REGISTRO');
INSERT INTO cartorio_atribuicao (cartorio_id, atribuicao_id) VALUES (1, 'ATR_NOTARIA');
INSERT INTO cartorio_atribuicao (cartorio_id, atribuicao_id) VALUES (1, 'ATR_CERTIDOES');
INSERT INTO cartorio_atribuicao (cartorio_id, atribuicao_id) VALUES (1, 'ATR_PROCESSOS');
