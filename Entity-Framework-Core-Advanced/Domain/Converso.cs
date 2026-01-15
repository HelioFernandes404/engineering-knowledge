using System.Net;

namespace EFcore.Domain
{
    public class Conversor
    {
        public int Id { get; set; }
        public bool Ativo { get; set; }
        public bool Excluido { get; set; }
        public Versao? Versao { get; set; }
        public Status Status { get; set; } 
    }

    public enum Versao
    {
        Versao1,
        Versao2,
        Versao3
    }

    public enum Status
    {
        EmAnalise,
        Aprovado,
        Recusado
    }
}
