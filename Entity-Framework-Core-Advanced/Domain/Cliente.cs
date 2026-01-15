using System.Net;

namespace EFcore.Domain
{

  public class Cliente
  {
    public int Id { get; set; }
    public string Nome { get; set; }
    public string Telefone { get; set; }

    public Endereco Endereco { get; set; }
  }

  public class Endereco // obj de valor 
  {
    public string Logradouro { get; set; }
    public string Bairro { get; set; }
    public string Cidade { get; set; }
    public string Estado { get; set; }
  }


}