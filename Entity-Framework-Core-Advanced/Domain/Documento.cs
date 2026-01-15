using Microsoft.EntityFrameworkCore;

namespace DominandoEFCore
{
  public class Documento
  {
    public string _cpf;
    public int Id { get; set; }

    public void SetCpf(string cpf)
    {
      // Validações
      if (string.IsNullOrEmpty(cpf))
        throw new Exception("CPF inválido");

      _cpf = cpf;
    }

    [BackingField(nameof(_cpf))]
    public string CPF => _cpf;

    public string GetCPF() => _cpf;

  }
}