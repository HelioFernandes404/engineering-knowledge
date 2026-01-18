namespace CrawlerAPI.Model;

public class CrawlerResponse
{
    public int MoreLinksFounds { get; set; }
    public IEnumerable<string> LinksFounds { get; set; }
    
}