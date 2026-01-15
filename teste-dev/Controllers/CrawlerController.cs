using CrawlerAPI.Interfaces;
using CrawlerAPI.Model;
using Microsoft.AspNetCore.Mvc;

namespace CrawlerAPI.Controllers;

[ApiController]
[Route("api/[controller]")]
public class CrawlerController(ICrawlersServices services) : ControllerBase
{

    [HttpPost]
    public async Task<CrawlerResponse> Crawl(CrawlerRequest crawlerRequest)
    {
        var result = await services.GetCrawlWebSite(
            crawlerRequest.WebsiteUrl, 
            crawlerRequest.maxDepth, 
            crawlerRequest.maxPagesToSearch);
        return result;
    }
    
}