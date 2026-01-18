using Microsoft.EntityFrameworkCore.Infrastructure;

namespace DominandoEFCore;

public class Departamento
{
    public int Id { get; set; }
    public string Descricao { get; set; }
    public bool Ativo { get; set; }
    public bool Excluido { get; set; }
    public List<Funcionario> Funcionarios { get; set; } //1N (proriedade de navegação)
    

}
