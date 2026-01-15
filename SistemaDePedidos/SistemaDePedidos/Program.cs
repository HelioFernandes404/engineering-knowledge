using System;
using System.Collections.Generic;
using System.Linq;
using Microsoft.AspNetCore.Hosting;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Hosting;
using SistemaDePedidos.Domain;
using SistemaDePedidos.ValueObjects;
using static System.Runtime.InteropServices.JavaScript.JSType;

namespace SitemaDePedidos
{
    public class Program
    {
        public static void Main(string[] args)
        {
            /*
            //Chamada dos Métodos
            
            InserirDados();
            InserirDadosEmMassa();
            ConsultarDados();
            CadastrarPedido();
            DeletarDados(2);
            AtualizarNomeCliente(2, "Will");
            AtualizarObjDesconectado();
            DeletarDados(5);
            DeletarDadosDesconectado();*/

            // Levanta a api
            // CreateHostBuilder(args).Build().Run();

            /*
            Utilizada apenas em abimente de desenvolvimento
            NUNCA EM PRODUÇÃO

            using var db = new Data.ApllicationContext();
            db.Database.Migrate();

            Verifica migrações pendentes
            var existe = db.Database.GetPendingMigrations().Any();
            if (existe)
            {
                Se existirem migrações pendentes
            }*/
        }
        private static void ConsultarPedidoCarregamentoAdiantado() //Carregamento aditado 
        {
            using var db = new Data.ApllicationContext();
            var pedidos = db.Pedidos.Include(p => p.Itens) // inclui os itens do pedido na consulta
                                    .ThenInclude(p => p.Produto) // vai dentro do inclue e traz os produtos que contem em itens
                                    .ToList();

            Console.WriteLine(pedidos.Count);
        }
        private static void ConsultarDados() 
        {
            using var db = new Data.ApllicationContext();
            var consultaPorSintaxe = (from c in db.Clientes where c.Id > 0 select c).ToList();
            var consultaPorMetodo = db.Clientes.Where(p => p.Id > 0)
                                               .OrderBy(p => p.Id)
                                               .ToList();

            foreach (var cliente in consultaPorMetodo)
            {
                Console.WriteLine($"Consultando Cliente: {cliente.Id}");
                db.Clientes.Find(cliente.Id);
            }
        } 
        private static void CadastrarPedido() // Carregamento atrasado
        {
            using var db = new Data.ApllicationContext();

            var cliente = db.Clientes.FirstOrDefault();
            var produto = db.Produtos.FirstOrDefault();

            var pedido = new Pedido
            {
                ClienteId = cliente.Id,
                InicadoEm = DateTime.Now,
                FinalizadoEm = DateTime.Now,
                Observacao = "Pedido Teste",
                TipoFrete = TipoFrete.SemFrete,
                Itens = new List<PedidoItem>
                {
                    new PedidoItem
                    {
                        ProdutoId = produto.Id,
                        Desconto = 0,
                        Quantidade = 1,
                        Valor = 10
                    }
                }
            };

            db.Pedidos.Add(pedido);
            db.SaveChanges();
        }
        private static void InserirDados()
        {
            var produto = new Produto
            {
                Descricao = "Produto Teste",
                CodigoBarras = "1234567891231",
                Valor = 10m,
                TipoProduto = TipoProduto.MercadoriaParaRevenda,
                Ativo = true
            };

            using var db = new Data.ApllicationContext();
            db.Produtos.Add(produto);
            var registros = db.SaveChanges();
            Console.WriteLine($"Total Registros(s): {registros}");
            // Setando de forma genérica
            //db.Set<Produto>().Add(produto);
        }
        private static void InserirDadosEmMassa()
        {
            var produto = new Produto
            {
                Descricao = "Produto Teste",
                CodigoBarras = "1234567891231",
                Valor = 10m,
                TipoProduto = TipoProduto.MercadoriaParaRevenda,
                Ativo = true
            };

            var cliente = new Cliente
            {
                Nome = "Nicolas Theodoro",
                CEP = "25955540",
                Cidade = "Teresópolis",
                Estado = "RJ",
                Telefone = "990178609",
            };

            var listaClientes = new[]
            {
                    new Cliente
                {
                    Nome = "Teste 1",
                    CEP= "25955540",
                    Cidade = "Teresópolis",
                    Estado = "RJ",
                    Telefone = "21990178609",
                },
                new Cliente
                {
                    Nome = "Teste 2",
                    CEP= "25955540",
                    Cidade = "Teresópolis",
                    Estado = "RJ",
                    Telefone = "21990178609",
                },
            };

            using var db = new Data.ApllicationContext();

            //Adicionando objetos
            //db.AddRange(produto, cliente);

            //Adicionando lista de objetos
            db.Clientes.AddRange(listaClientes);

            var registros = db.SaveChanges();

            Console.WriteLine($"Total Registros(s): {registros}");
        }
        private static void AtualizarObjDesconectado()
        {
            var id = 3;
            using var db = new Data.ApllicationContext();

            var clienteDesconectado = new
            {
                Nome = "Cliente Desconectado",
                Telefone = "7966669999"
            };

            // Utilizado principalmente em APIS
            // Primeiro recebe o obj, procura na base e então atualiza
            var cliente = db.Clientes.Find(id);

            if (cliente != null)
            {
                //Atualiza só os campos que foram modificados
                db.Entry(cliente).CurrentValues.SetValues(clienteDesconectado);
                db.SaveChanges();
            }

        }
        private static void AtualizarNomeCliente(int id, string nomeCliente)
        {
            using var db = new Data.ApllicationContext();
            var cliente = db.Clientes.Find(id);

            if (cliente != null)
            {
                cliente.Nome = nomeCliente;
                // db.Clientes.Update(cliente); atualiza todas as colunas na base de dados

                //Salvando direto ele altera apenas as colunas que receberam novos dados
                db.SaveChanges();
            }
            else
            {
                Console.WriteLine("Não foi possível encontrar o cliente");
            }
        }
        private static void DeletarDados(int id)
        {
            using var db = new Data.ApllicationContext();
            var registro = db.Produtos.Find(id);

            if (registro != null)
            {
                db.Remove(registro);
                db.SaveChanges();
            }
        }
        private static void DeletarDadosDesconectado()
        {
            using var db = new Data.ApllicationContext();

            var cliente = new Cliente { Id = 3 };

            if (cliente != null)
            {
                // db.Remove(cliente);
                db.Entry(cliente).State = EntityState.Deleted;
                db.SaveChanges();
            }
        }

        /*
        public static IHostBuilder CreateHostBuilder(string[] args) =>
            Host.CreateDefaultBuilder(args)
                .ConfigureWebHostDefaults(webBuilder =>
                {
                    webBuilder.UseStartup<Startup>();
                });

        */
    }
        
}