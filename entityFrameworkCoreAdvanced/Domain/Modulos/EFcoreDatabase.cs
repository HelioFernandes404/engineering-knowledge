namespace DominandoEFCore;
using System;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Infrastructure;
using Microsoft.EntityFrameworkCore.Storage;

public class EFcoreDatabase
{
  static void ScriptGeralDoBancoDeDados()
  {
    using var db = new ApplicationContext();
    var script = db.Database.GenerateCreateScript(); // Gera o script de criação do banco de dados
    Console.WriteLine(script);
  }
  static void TodasJaMigracoes() // Todas as migrações
  {
    using var db = new ApplicationContext();
    var migracoes = db.Database.GetAppliedMigrations(); // recupera todas as migrações aplicadas

    Console.WriteLine($"Total: {migracoes.Count()}");

    foreach (var migracao in migracoes)
    {
      Console.WriteLine($"Migração: {migracao}");
    }
  }

  static void TodasMigracoes() // Todas as migrações
  {
    using var db = new ApplicationContext();
    var migracoes = db.Database.GetMigrations();

    Console.WriteLine($"Total: {migracoes.Count()}");

    foreach (var migracao in migracoes)
    {
      Console.WriteLine($"Migração: {migracao}");
    }
  }
  static void AplicarMigracaoEmTempoDeExecucao() // Aplicar migracao em tempo de execução
  {
    using var db = new ApplicationContext();
    db.Database.Migrate(); // Aplica todas as migrações pendentes
  }
  static void MigracoesPendentes()
  {
    using var db = new ApplicationContext();
    var MigracoesPendentes = db.Database.GetPendingMigrations();

    Console.WriteLine($"Total: {MigracoesPendentes.Count()}");

    foreach (var migracao in MigracoesPendentes)
    {
      Console.WriteLine($"Migração: {migracao}");
    }

  }
  static void SqlInjection() // Evitar SQL Injection
  {
    using var db = new ApplicationContext();
    db.Database.EnsureDeleted();
    db.Database.EnsureCreated();

    db.Departamentos.AddRange(
        new Departamento { Descricao = "Departamento 01" },
        new Departamento { Descricao = "Departamento 02" }
    );

    db.SaveChanges();

    var descricao = "Teste ' or 1='1";
    db.Database.ExecuteSqlRaw("update departamentos set descricao={0} where id=1", descricao); //tranforma em db parameter

    foreach (var departamento in db.Departamentos.AsNoTracking())
    {
      Console.WriteLine($"Id: {departamento.Id}, Descricao: {departamento.Descricao}");
    }
  }
  static void ExecuteSQL()
  {
    using var db = new ApplicationContext();

    //Primeira opção
    using (var cmd = db.Database.GetDbConnection().CreateCommand())
    {
      cmd.CommandText = "SELECT 1";
      cmd.ExecuteNonQuery();
    }

    //Segunda opção
    var descricao = "TESTE";
    db.Database.ExecuteSqlRaw("update departamentos set descricao={0} where id=1", descricao); //tranforma em db parameter

    //Terceira opção
    db.Database.ExecuteSqlInterpolated($"update departamentos set descricao={descricao} where id=1");
  }
  static int _count;
  static void GerenciarEstadoDaConexao(bool GerenciarEstadoDaConexao)
  // Usado quando precisar fazer muitas consultas ao banco de dados
  {
    using var db = new ApplicationContext();
    var time = System.Diagnostics.Stopwatch.StartNew();

    var conexao = db.Database.GetDbConnection();
    conexao.StateChange += (_, __) => ++_count;

    if (GerenciarEstadoDaConexao)
    {
      conexao.Open();
    }

    for (var i = 0; i < 200; i++)
    {
      db.Departamentos.AsNoTracking().Any();
    }

    time.Stop();
    var mensagem = $"Tempo: {time.Elapsed.ToString()}, {GerenciarEstadoDaConexao}, Contador: {_count}";

    Console.WriteLine(mensagem);
  }
  static void HealthcheckDatabase()
  {
    using var db = new ApplicationContext();
    var canConnect = db.Database.CanConnect(); // Verifica se é possível se conectar ao banco de dados
    if (canConnect)
    {
      Console.WriteLine("Posso me conectar");
    }
    else
    {
      Console.WriteLine("Não posso me conectar");
    }
  }
  static void EnsureCreated() // Cria o banco de dados
  {
    using var db = new ApplicationContext();
    db.Database.EnsureCreated();
  }
  static void EnsureDeleted() // Deleta o banco de dados
  {
    using var db = new ApplicationContext();
    db.Database.EnsureDeleted();
  }
  static void GapDoEnsureCreated()
  {
    using var db1 = new ApplicationContext();
    using var db2 = new ApplicationContext();

    db1.Database.EnsureCreated();
    db2.Database.EnsureCreated(); // Erro devido a concorrência de acesso ao banco de dados 

    // Para resolver o problema de concorrência de acesso ao banco de dados.
    var databaseCreator = db2.GetService<IRelationalDatabaseCreator>();
    databaseCreator.CreateTables(); // Cria as tabelas
  }
}
