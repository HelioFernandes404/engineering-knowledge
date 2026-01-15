namespace DominandoEFCore;
using System;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Infrastructure;
using Microsoft.EntityFrameworkCore.Storage;

public class Carregamentos
{
        static void CarregamentoLento()
        {
            using var db = new ApplicationContext();
            SetupTiposCarregamentos(db);

            //db.ChangeTracker.LazyLoadingEnabled = false; // Desabilita o carregamento preguiçoso

            var departamentos = db.Departamentos.ToList(); // vai ate o banco e traz os departamentos

            foreach (var departamento in departamentos)
            {

                Console.WriteLine("-------------------");
                Console.WriteLine($"Departamento: {departamento.Descricao}");

                if (departamento.Funcionarios?.Any() ?? false)
                {
                    foreach (var funcionario in departamento.Funcionarios)
                    {
                        Console.WriteLine($"\tFuncionario: {funcionario.Nome}");
                    }
                }
                else
                {
                    Console.WriteLine("Nenhum funcionário encontrado");
                }
            }
        }
        static void CarregamentoExplicito()
        {
            using var db = new ApplicationContext();
            SetupTiposCarregamentos(db);

            var departamentos = db.Departamentos.ToList(); // vai ate o banco e traz os departamentos

            foreach (var departamento in departamentos)
            {
                if (departamento.Id == 2)
                {
                    // carrega os funcionarios de um  departamento especifico
                    //db.Entry(departamento).Collection(p => p.Funcionarios).Load(); 

                    db.Entry(departamento).Collection(p => p.Funcionarios).Query().Where(p => p.Id > 2).ToList();
                }

                Console.WriteLine("-------------------");
                Console.WriteLine($"Departamento: {departamento.Descricao}");

                if (departamento.Funcionarios?.Any() ?? false)
                {
                    foreach (var funcionario in departamento.Funcionarios)
                    {
                        Console.WriteLine($"\tFuncionario: {funcionario.Nome}");
                    }
                }
                else
                {
                    Console.WriteLine("Nenhum funcionário encontrado");
                }
            }
        }
        static void CarregamentoAdiantado()
        {
            using var db = new ApplicationContext();
            SetupTiposCarregamentos(db);

            var departamentos = db.Departamentos // vai ate o banco e traz os departamentos
                .Include(p => p.Funcionarios); // carrega os funcionarios de cada departamento

            foreach (var departamento in departamentos)
            {
                Console.WriteLine("-------------------");
                Console.WriteLine($"Departamento: {departamento.Descricao}");

                if (departamento.Funcionarios?.Any() ?? false)
                {
                    foreach (var funcionario in departamento.Funcionarios)
                    {
                        Console.WriteLine($"\tFuncionario: {funcionario.Nome}");
                    }
                }
                else
                {
                    Console.WriteLine("Nenhum funcionário encontrado");
                }
            }
        }
        static void SetupTiposCarregamentos(ApplicationContext db)
        {
            if (!db.Departamentos.Any()) // Se não existir departamentos
            {
                db.Departamentos.AddRange(
                    new Departamento
                    {
                        Descricao = "Departamento 01",
                        Funcionarios = new System.Collections.Generic.List<Funcionario>
                        {
                            new Funcionario
                            {
                                Nome = "Rafael Almeida",
                                CPF = "99999999911",
                                RG = "2100062"
                            }
                        }
                    },
                    new Departamento
                    {
                        Descricao = "Departamento 02",
                        Funcionarios = new System.Collections.Generic.List<Funcionario>
                        {
                            new Funcionario
                            {
                                Nome = "Bruno Brito",
                                CPF = "88888888811",
                                RG = "3100062"
                            },
                            new Funcionario
                            {
                                Nome = "Marrone",
                                CPF = "77777777711",
                                RG = "4100062"
                            }
                        }
                    });

                db.SaveChanges();
                db.ChangeTracker.Clear();
            }
        }
}
