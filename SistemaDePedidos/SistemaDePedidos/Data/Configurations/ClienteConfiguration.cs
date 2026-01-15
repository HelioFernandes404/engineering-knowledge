using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using SistemaDePedidos.Domain;
using System.Reflection.Metadata;


namespace SistemaDePedidos.Data.Configurations
{
    // Desacopla as regras de configuração de modelo de dados por tabela
    public class ClienteConfiguration : IEntityTypeConfiguration<Cliente>
    {
        public void Configure(EntityTypeBuilder<Cliente> builder)
        {
            builder.ToTable("Clientes"); //Nomeia Tabela no BD
            builder.HasKey(p => p.Id); //Define PK tabela
            builder.Property(p => p.Nome).HasColumnType("VARCHAR(80)").IsRequired(); //Configura o tipo de dado e obrigatório
            builder.Property(p => p.Telefone).HasColumnType("CHAR(11)");
            builder.Property(p => p.CEP).HasColumnType("CHAR(8)").IsRequired();
            builder.Property(p => p.Estado).HasColumnType("CHAR(2)").IsRequired();
            builder.Property(p => p.Cidade).HasMaxLength(70).IsRequired();//Define tamanho máximo campo

            builder.HasIndex(i => i.Telefone).HasDatabaseName("idx_cliente_telefone");//Cria indice no BD
        }
    }
}
