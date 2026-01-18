using System;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Infrastructure;
using Microsoft.EntityFrameworkCore.Storage;

namespace DominandoEFCore;

public class Consultas
{
  static void SplitQuery()
  {
    using var db = new ApplicationContext();
    db.Database.EnsureDeleted();
    Setup(db);

    //Resolver o problema da exploção do plano cartesiano
    var departamentos = db.Departamentos
                          .Include(p => p.Funcionarios)
                          .Where(p => p.Id < 3)
                          .AsSplitQuery() // divide a consulta em duas
                                          //.AsSingleQuery() // junta a consulta em uma
                          .ToList();

    foreach (var departamento in departamentos)
    {
      Console.WriteLine($"Descrição: {departamento.Descricao}");

      foreach (var funcionario in departamento.Funcionarios)
      {
        Console.WriteLine($"\t Nome: {funcionario.Nome}");
      }
    }
  }

  static void EntendendoConsulta1NN1()
  {
    using var db = new ApplicationContext();

    var fucinarios = db.Funcionarios
    .Include(p => p.Departamento)
    .ToList(); // so vai trazer os furcionarios que tem departamento


    foreach (var funcionario in fucinarios)
    {
      Console.WriteLine($"Nome: {funcionario.Nome} / Descrição Dep: {funcionario.Departamento.Descricao}");
    }


    /*
    // Exebir os fucinarios relacionando aos **departamentos
    var departamentos = db.Departamentos
        .Include(p => p.Funcionarios)
        .ToList();

    foreach (var departamento in departamentos)
    {
        Console.WriteLine($"Descrição: {departamento.Descricao}");

        foreach (var funcionario in departamento.Funcionarios)
        {
            Console.WriteLine($"\t Nome: {funcionario.Nome}");
        }
    }
    */
  }

  static void ConsultaComTag()
  {
    using var db = new ApplicationContext();
    db.Database.EnsureDeleted();
    Setup(db);

    var departamentos = db.Departamentos
        .TagWith("Estou enviando um comentário para o servidor")
        .ToList();

    foreach (var departamento in departamentos)
    {
      Console.WriteLine($"Descrição: {departamento.Descricao}");
    }
  }

  static void ConsultaInterpolada()
  {
    using var db = new ApplicationContext();
    db.Database.EnsureDeleted();
    Setup(db);

    var id = 0;
    var departamentos = db.Departamentos
        .FromSqlInterpolated($"SELECT * FROM Departamentos WHERE Id > {id}")
        .ToList();

    foreach (var departamento in departamentos)
    {
      Console.WriteLine($"Descrição: {departamento.Descricao}");
    }
  }

  static void ConsultaParametrizada()
  {
    using var db = new ApplicationContext();
    db.Database.EnsureDeleted();
    Setup(db);

    var id = 0;
    var departamentos = db.Departamentos
    .FromSqlRaw("SELECT * FROM Departamentos WHERE Id > {0}", id)
    .ToList();

    foreach (var departamento in departamentos)
    {
      Console.WriteLine($"Descrição: {departamento.Descricao}");
    }
  }

  static void ConsultaProjetada()
  {
    using var db = new ApplicationContext();
    db.Database.EnsureDeleted();
    Setup(db);

    var departamentos = db.Departamentos
        .Where(p => p.Id > 0)
        .Select(p => new
        {
          p.Descricao,
          Funcionarios = p.Funcionarios.Select(f => f.Nome)
        })
        .ToList();

    foreach (var departamento in departamentos)
    {
      Console.WriteLine($"Descrição: {departamento.Descricao}");

      foreach (var funcionario in departamento.Funcionarios)
      {
        Console.WriteLine($"\t Nome: {funcionario}");
      }
    }
  }

  static void IgnoreFiltroGlobal()
  {
    using var db = new ApplicationContext();
    db.Database.EnsureDeleted();
    Setup(db);

    var departamentos = db.Departamentos.IgnoreQueryFilters().Where(p => p.Id > 0).ToList();

    foreach (var departamento in departamentos)
    {
      Console.WriteLine($"Descrição: {departamento.Descricao} \t Excluido: {departamento.Excluido}");
    }
  }

  static void FiltroGlobal()
  {
    using var db = new ApplicationContext();
    db.Database.EnsureDeleted();
    Setup(db);

    var departamentos = db.Departamentos.Where(p => p.Id > 0).ToList();

    foreach (var departamento in departamentos)
    {
      Console.WriteLine($"Descrição: {departamento.Descricao} \t Excluido: {departamento.Excluido}");
    }
  }

  static void Setup(ApplicationContext db)
  {
    if (db.Database.EnsureCreated())
    {
      db.Departamentos.AddRange(
          new Departamento
          {
            Ativo = true,
            Descricao = "Departamento 01",
            Funcionarios = new List<Funcionario>
              {
                            new Funcionario
                            {
                                CPF = "12345678901",
                                RG = "11145678",
                                Nome = "Rafael Almeida",
                            }
              },
            Excluido = true
          },
          new Departamento
          {
            Ativo = true,
            Descricao = "Departamento 02",
            Funcionarios = new List<Funcionario>
              {
                            new Funcionario
                            {
                                CPF = "12345678901",
                                RG = "22345678",
                                Nome = "Bruno Brito",
                            },
                            new Funcionario
                            {
                                CPF = "12345678901",
                                RG = "33345678",
                                Nome = "Eduardo Pires",
                            }
              },
          });

      db.SaveChanges();
      db.ChangeTracker.Clear();
    }
  }
}
