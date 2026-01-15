using EFcore.Domain;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace DominandoEFCore;

public class ClienteConfiguration : IEntityTypeConfiguration<Cliente> // boa praticar segregar 
{
  public void Configure(EntityTypeBuilder<Cliente> builder)
  {
    builder.OwnsOne(c => c.Endereco, end =>
   {
     end.Property(p => p.Bairro).HasColumnName("Bairro"); // renomeia a coluna
     end.Property(p => p.Cidade).HasColumnName("Cidade");
     end.Property(p => p.Estado).HasColumnName("Estado");
     end.Property(p => p.Logradouro).HasColumnName("Logradouro");
     end.ToTable("Enderecos") // renomeia a tabela table spliting
     ;
   });


  }
}
