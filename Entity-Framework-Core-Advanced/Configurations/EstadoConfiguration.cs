using DominandoEFCore.Domain;
using EFcore.Domain;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace DominandoEFCore;

public class EstadoConfiguration : IEntityTypeConfiguration<Estado> // boa praticar segregar 
{
  public void Configure(EntityTypeBuilder<Estado> builder)
  {

    //Configurar para um para o Flunt API

    // Relacionamento de one-to-one
    builder.HasOne(p => p.Governador)
      .WithOne(p => p.Estado)
      .HasForeignKey<Governador>(p => p.EstadoId);

    //AutoInclude
    builder.Navigation(p => p.Governador).AutoInclude();

    // Relacionamento de one-to-many
    builder
      .HasMany(p => p.Cidades)
      .WithOne(p => p.Estado)
      .IsRequired(false);
    //.OnDelete(DeleteBehavior.Cascade);

  }
}
