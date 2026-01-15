# Crie uma lista de alunos e realize as operações de adicionar, remover, alterar e buscar alunos.

Alunos: list = ["Aluno2", "Aluno1", "Aluno3"]

Alunos.append("Aluno4")

if "Aluno4" in Alunos: print("Existe Aluno4: que foi adicionado")

Alunos.remove("Aluno4")

if "Aluno4" in Alunos: print("Aluno4: foi removendo com sucesso!")

nomeAntigoDoUsuario = Alunos[0];

novoNomeDoAluno = Alunos[0] = "Novo Aluno2";

if (nomeAntigoDoUsuario == novoNomeDoAluno):
    print("O nome não foi altrado: ERRROR")
else:
    print("O nome altrado: OK")

if "Novo Aluno2" in Alunos: print("O Valor Novo Aluno2 está na lista!")