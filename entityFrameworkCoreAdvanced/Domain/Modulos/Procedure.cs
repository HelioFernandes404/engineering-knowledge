using System;
using DominandoEFCore;
using Microsoft.Data.SqlClient;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Infrastructure;
using Microsoft.EntityFrameworkCore.Storage;



public class Procedure
{

    static void ConsultaViaProcedure()
    {
        using var db = new ApplicationContext();

        var dep = new SqlParameter("@dep", "Departamento");

        //FromSqlInterpolated(db, $"EXEC GetDepartamentos {dep}");

        var departamentos = db.Departamentos
        .FromSqlRaw("EXEC GetDepartamentos @p0", "Departamento").ToList();

        foreach (var departamento in departamentos)
        {
            Console.WriteLine($"Descrição: {departamento.Descricao}");
        }
    }
    static void CriarStoredProcedureDeConsulta()
    {
        var criarDepartamento = @"
            CREATE OR PROCEDURE GetDepartamentos
                @Descricao VARCHAR(50)
            AS
            BEGIN
                SELECT * FROM Departamentos WHERE Descricao LIKE @Descricao + '%'
            END
            ";
        using var db = new ApplicationContext();
        db.Database.ExecuteSqlRaw(criarDepartamento);
    }

    static void InserirDadosViaProcedure()
    {
        using var db = new ApplicationContext();
        db.Database.ExecuteSqlRaw("EXEC CriarDepartamento @p0, @p", "Departamento Via Procedure", true);
    }
    static void CriarStoredProcedure()
    {
        var criarDepartamento = @"
         CREATE OR ALTER PROCEDURE CriarDepartamento
            @Descricao VARCHAR(50),
            @Ativo BIT
            AS 
            BEGIN
                INSERT INTO Departamentos (Descricao, Ativo, Excluido)
                VALUES (@Descricao, @Ativo, 0)
            END  ";
        using var db = new ApplicationContext();
        db.Database.ExecuteSqlRaw(criarDepartamento);
    }
}
