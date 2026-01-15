# Flashcards Learning System

## 📋 Sobre o Projeto
Sistema de flashcards para estudo com suporte a Text-to-Speech (TTS), desenvolvido em .NET 8. O projeto utiliza padrões de Clean Architecture e implementa diversos Design Patterns para manter o código organizado e escalável.

## 🚀 Tecnologias Utilizadas

- .NET 8.0
- Entity Framework Core
- Microsoft.Extensions.DependencyInjection
- Microsoft.Extensions.Configuration
- SQL Server (ou sua escolha de banco de dados)

## 🔧 Pré-requisitos

- [.NET SDK 8.0](https://dotnet.microsoft.com/download)
- IDE de sua preferência (Visual Studio 2022, VS Code, etc.)
- SQL Server (ou outro banco de dados compatível com EF Core)

## ⚙️ Configuração

1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

2. Restaure os pacotes NuGet
```bash
dotnet restore
```

3. Configure o arquivo `appsettings.json`
```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=(localdb)\\mssqllocaldb;Database=FlashcardsDB;Trusted_Connection=True;MultipleActiveResultSets=true"
  },
  "TTSConfiguration": {
    "SpeakerId": "p339",
    "StyleWav": "",
    "LanguageId": ""
  }
}
```

4. Execute as migrações do banco de dados
```bash
dotnet ef database update
```

## 📦 Estrutura do Projeto

```
src/
├── Application/
│   ├── Core/
│   │   ├── Interfaces/
│   │   └── Command/
│   ├── Features/
│   │   ├── Cards/
│   │   └── Decks/
│   └── Configuration/
├── Domain/
│   ├── Entities/
│   └── ValueObjects/
├── Infrastructure/
│   ├── Persistence/
│   └── Services/
└── Presentation/
    └── Console/
```

## 🎮 Como Usar

1. Execute o programa
```bash
dotnet run
```

2. Comandos disponíveis:
- `1` - Lista todos os baralhos disponíveis
- `start /{deckId}` - Inicia o estudo de um baralho específico
- `add /{deckId}` - Adiciona novas cartas ao baralho
- `:q` - Sai do programa

Exemplo de uso:
```bash
# Listar baralhos
1

# Iniciar estudo do baralho ID 1
start /1

# Adicionar cartas ao baralho ID 2
add /2
```

## 🏗️ Design Patterns Utilizados

- **Repository Pattern**: Para abstração do acesso a dados
- **Unit of Work**: Gerenciamento de transações
- **Command Pattern**: Para execução de comandos do console
- **Factory Pattern**: Criação de objetos
- **Dependency Injection**: Para inversão de controle

## 🧪 Testes

Execute os testes usando:
```bash
dotnet test
```

## 📝 Convenções de Código

- Seguimos o [C# Coding Conventions](https://docs.microsoft.com/en-us/dotnet/csharp/programming-guide/inside-a-program/coding-conventions)
- Utilizamos o estilo de nomenclatura PascalCase para classes e métodos
- Comentários em português para melhor compreensão do código

## 🤝 Contribuindo

1. Faça um Fork do projeto
2. Crie sua Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## ✨ Próximos Passos

- [ ] Implementação de interface web
- [ ] Suporte a múltiplos idiomas
- [ ] Sistema de revisão espaçada
- [ ] Exportação/Importação de decks
- [ ] Estatísticas de estudo

## 🐛 Problemas Conhecidos

- O sistema TTS requer configuração adicional para alguns idiomas
- Algumas operações podem ser lentas com grandes conjuntos de dados

## 📞 Suporte

Para suporte, por favor abra uma [issue](https://github.com/seu-usuario/seu-repositorio/issues) no GitHub.

## 🙋‍♂️ Autor

Seu Nome - [@seuTwitter](https://twitter.com/seuTwitter)

Project Link: [https://github.com/seu-usuario/seu-repositorio](https://github.com/seu-usuario/seu-repositorio)