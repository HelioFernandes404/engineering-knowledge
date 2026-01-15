# Crie um dicionário com nome, telefone e e-mail e realize as operações de manipulação de dados.
agenda_contato: dict[str, str] = {
    "nome": "joao silva",
    "telefone": "(11) 98544-9393",
    "email": "joao.silva@email.com",
    "key" : "ap-103"
}

# Adicionar pares chave-valor em um dicionário
agenda_contato["endereço"] = "Rua fic, 123"
agenda_contato["cep"] = "48009-800"

# Metodo Update
agenda_contato.update({
    "nome": "João Silva Neto",  # Alterando o nome
    "idade": 30  # Adicionando uma nova chave 'idade'
})

# Buscar
contato = agenda_contato.get("key")

# Alteração
agenda_contato["telefone"] = "(99) 9999-1111"


# Excluir
del agenda_contato["telefone"]

# Removendo a chave 'telefone' e obtendo seu valor
nome_removido = agenda_contato.pop("nome")
print(agenda_contato)