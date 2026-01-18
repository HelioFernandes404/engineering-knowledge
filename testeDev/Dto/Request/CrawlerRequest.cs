using System.ComponentModel.DataAnnotations;

namespace CrawlerAPI.Model;

public class CrawlerRequest
{


    [Required(ErrorMessage = "A URL é obrigatória.")]
    [Url(ErrorMessage = "URL inválida.")]
    public string WebsiteUrl { get; set; }
    
    [Range(0, 3, ErrorMessage = "O valor deve estar entre 0 e 3.")]
    public int maxDepth { get; set; }
    
    [Range(1, 1000, ErrorMessage = "O valor deve estar entre 1 e 1000.")]
    public int maxPagesToSearch { get; set; }
}