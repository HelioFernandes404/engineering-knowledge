using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DominandoEFCore.Domain.Modulos.Suporte
{
    public class Infra
    {

        static void ExecutarEstrategiaResiliencia()
        {
            using var db = new ApplicationContext();

            var strategy = db.Database.CreateExecutionStrategy();

            strategy.Execute(() =>
            {
                using var transaction = db.Database.BeginTransaction();

                db.Departamentos.Add(new Departamento { Descricao = "Departamento Transacao" });
                db.SaveChanges();

                transaction.Commit();
            });
        }

        static void TempoComandosGeral()
        {
            using var db = new ApplicationContext();

            db.Database.SetCommandTimeout(10); // timeout de 10 segundos dentro de um fluxo

            db.Database.ExecuteSqlRaw("SELECT 1 ");
        }

        static void HabilitandoBatchSize() // padrão de insert é 42
        {
            using var db = new ApplicationContext();

            db.Database.EnsureDeleted();
            db.Database.EnsureCreated();

            var conexao = db.Database.GetDbConnection();
            conexao.Open();

            for (int i = 0; i < 50; i++)
            {
                db.Departamentos.Add(
                    new Departamento
                    {
                        Descricao = "Departamento " + i
                    });
                db.SaveChanges();
            }
        }

        static void DadosSensiveis()
        {
            using var db = new ApplicationContext();

            var descricao = "Departamentos";

            var departamentos = db.Departamentos
                .FromSqlRaw($"SELECT * FROM Departamentos WHERE Descricao = '{descricao}'")
                .ToList();

        }

        static void ConsultarDepartamentos()
        {
            using var db = new ApplicationContext();

            var departamentos = db.Departamentos.FromSqlRaw("SELECT * FROM Departamentos").ToList();

            foreach (var departamento in departamentos)
            {
                Console.WriteLine($"Descrição: {departamento.Descricao}");
            }
        }
    }
}
