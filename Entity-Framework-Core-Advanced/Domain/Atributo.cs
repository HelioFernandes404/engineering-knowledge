using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using Microsoft.EntityFrameworkCore;

namespace DominandoEFCore
{
  [Index(nameof(Descricao), nameof(Observacao), IsUnique = true)]
  [Comment("Comentário do atributo da minha tebela")]
  public class Atributo
  {
    [Key]
    //[DatabaseGenerated(DatabaseGeneratedOption.Identity)] // Identity = AutoIncrement ja vem padrão no EFcore
    //[DatabaseGenerated(DatabaseGeneratedOption.Computed)] // Computed = Calculado
    [DatabaseGenerated(DatabaseGeneratedOption.None)] // Computed = Calculado
    public int Id { get; set; }

    [Column("MinhaDescricao", TypeName = "VARCHAR(255)")]
    public string Descricao { get; set; }

    [Required]
    [MaxLength(255)]
    public string Observacao { get; set; }
  }

  public class Aeroporto
  {
    public int Id { get; set; }
    public string Nome { get; set; }

    [NotMapped] // Não mapeia a propriedade no banco de dados
    public string PropriedadeTeste { get; set; }

    [InverseProperty("AeroportoPartida")]
    public ICollection<Voo> VoosDePartida { get; set; }
    [InverseProperty("AeroportoChegada")]
    public ICollection<Voo> VoosDeChegada { get; set; }
  }

  [NotMapped] // Não mapeia a classe no banco de dados
  public class Voo
  {
    public int Id { get; set; }
    public string Descricao { get; set; }

    public Aeroporto AeroportoPartida { get; set; }
    public Aeroporto AeroportoChegada { get; set; }
  }

  [Keyless]
  public class RelatorioFinanceiro
  {
    public string Descricao { get; set; }
    public decimal Total { get; set; }
    public DateTime Data { get; set; }
  }
}