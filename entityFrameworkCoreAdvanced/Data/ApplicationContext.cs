using System.Reflection;
using DominandoEFCore.Domain;
using EFcore.Domain;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Diagnostics;
using Microsoft.EntityFrameworkCore.Storage.ValueConversion;
using Microsoft.Extensions.Logging;

namespace DominandoEFCore;

public class ApplicationContext : DbContext
{
    public DbSet<Departamento> Departamentos { get; set; }
    public DbSet<Funcionario> Funcionarios { get; set; }
    public DbSet<Estado> Estados { get; set; }
    public DbSet<Cliente> Clientes { get; set; }
    public DbSet<Conversor> Conversors { get; set; }

    public DbSet<Pessoa> Pessoas { get; set; }
    public DbSet<Instrutor> Instrutuors { get; set; }
    public DbSet<Aluno> Alunos { get; set; }

    public DbSet<Dictionary<string, object>> Configuracoes => Set<Dictionary<string, object>>("Configuracoes");

    public DbSet<Aeroporto> Aeroportos { get; set; }
    public DbSet<Atributo> Atributos { get; set; }

    public DbSet<Funcao> Funcao { get; set; }

    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
    {
        const string strConnection = "Server=localhost;Database=efcore-curso;User Id=sa;Password=Adminxyz22#;MultipleActiveResultSets=true;Encrypt=false;TrustServerCertificate=true;";
        optionsBuilder
            .UseSqlServer(strConnection)
            .LogTo(Console.WriteLine, LogLevel.Information)
            ;
    }

    override protected void OnModelCreating(ModelBuilder modelBuilder)
    {
        // 1. forma de aplicar as configura de entidades 
        modelBuilder.ApplyConfiguration(new ClienteConfiguration());

        // 2. forma de aplicar para todas as configura de todas entidades 
        modelBuilder.ApplyConfigurationsFromAssembly(Assembly.GetExecutingAssembly());

        // 3. forma de aplicar para todas as configura de todas entidades
        modelBuilder.ApplyConfigurationsFromAssembly(typeof(ApplicationContext).Assembly);


        modelBuilder.SharedTypeEntity<Dictionary<string, object>>("Configuracoes", b =>
        {
            b.Property<int>("Id"); // obrigatório para efcore

            b.Property<string>("Chave")
            .HasColumnName("VARCHAR(40)")
            .IsRequired();

            b.Property<string>("Valor")
            .HasColumnName("VARCHAR(255)")
            .IsRequired();

        });

        modelBuilder.Entity<Funcao>(conf =>
        {
            conf.Property<string>("PropriedadeSombra")
            .HasColumnType("VARCHAR(255)")
            .HasDefaultValue("'test'");
        });
    }

}

