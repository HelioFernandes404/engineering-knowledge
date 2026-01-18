using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace DominandoEFCore
{
  public class PessoaConfiguration : IEntityTypeConfiguration<Pessoa>
  {
    public void Configure(EntityTypeBuilder<Pessoa> builder)
    {
      builder
        .ToTable("Pessoas");
    }
  }

  public class InstrutorConfiguration : IEntityTypeConfiguration<Instrutor>
  {
    public void Configure(EntityTypeBuilder<Instrutor> builder)
    {
      builder
        .ToTable("Instrutores");
    }
  }

  public class AlunoConfiguration : IEntityTypeConfiguration<Aluno>
  {
    public void Configure(EntityTypeBuilder<Aluno> builder)
    {
      builder
        .ToTable("Alunos");
    }
  }

}
