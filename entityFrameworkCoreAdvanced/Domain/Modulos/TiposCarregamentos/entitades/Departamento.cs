 /*
using Microsoft.EntityFrameworkCore.Infrastructure;

namespace DominandoEFCore;

public class Departamento
{
    public int Id { get; set; }
    public string Descricao { get; set; }
    public bool Ativo { get; set; }
    public bool Excluido { get; set; }
    public List<Funcionario> Funcionarios { get; set; } //1N (proriedade de navegação)
    
    /*
    public Departamento()
    {

    }

    private Action<object, string> _lazyLoader;
    private Departamento(Action<object, string> lazyLoader)
    {
        _lazyLoader = lazyLoader;
    }
    private List<Funcionario> _funcionarios;
    public virtual List<Funcionario> Funcionarios   //1N Departamento 1 -> N Funcionario (proriedade de navegação)
    {
        get
        {
            _lazyLoader?.Invoke(this, nameof(Funcionarios));
            return _funcionarios;
        }
        set => _funcionarios = value;
    }
    
    private ILazyLoader _lazyLoader { get; set; }
    private Departamento(ILazyLoader lazyLoader)
    {
        _lazyLoader = lazyLoader;
    }
    private List<Funcionario> _funcionarios;
    public virtual List<Funcionario> Funcionarios   //1N Departamento 1 -> N Funcionario (proriedade de navegação)
    {
        get => _lazyLoader.Load(this, ref _funcionarios);
        set => _funcionarios = value;
    }
    
}
*/
