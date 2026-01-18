/*
using Microsoft.Extensions.Logging;

namespace DominandoEFCore;

public class ApplicationContext : DbContext // Class do EF core que gerencia o banco de dados
{
    public DbSet<Departamento> Departamentos { get; set; } 
    public DbSet<Funcionario> Funcionarios { get; set; }

    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
    {
        const string strConnection = "Server=DESKTOP-KH946K7\\SQLEXPRESS;Database=DevIO-02;Trusted_Connection=True;TrustServerCertificate=True;";
        optionsBuilder
            //.UseSqlServer(strConnection, p => p.UseQuerySplittingBehavior(QuerySplittingBehavior.SplitQuery)) // Define o comportamento de divisão de consulta
            .UseSqlServer(strConnection)
            .LogTo(Console.WriteLine, LogLevel.Information) // Loga as informações no console
            //.UseLazyLoadingProxies() // Habilita o carregamento preguiçoso
            .EnableSensitiveDataLogging(); // Habilita o log de informações sensíveis
    }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        //modelBuilder.Entity<Departamento>().HasQueryFilter(p => !p.Excluido); // Filtro global
    }
}
*/
