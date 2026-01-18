using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace SistemaDePedidos.Domain
{
    //Trabalhando com DataAnnotations e Schema
    [Table("Clientes")] //muda o nome da tabela
    public class Cliente
    {
        [Key]
        public int Id { get; set; }
        [Required]
        public string Nome { get; set; }
        [Column("Phone")] // muda o nome do campo na base de dados
        public string Telefone { get; set; }
        public string CEP { get; set; }
        public string Estado { get; set; }
        public string Cidade { get; set; }

        //Add-Migration AddEmail
        //Update-Database
        //Remove-Migration
        public string Email { get; set; }

    }
}
