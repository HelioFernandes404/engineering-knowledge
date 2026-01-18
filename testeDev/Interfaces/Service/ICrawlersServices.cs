using CrawlerAPI.Model;
using Microsoft.AspNetCore.Mvc;

namespace CrawlerAPI.Interfaces;

public interface ICrawlersServices
{
    Task<CrawlerResponse> GetCrawlWebSite(string url, int depth, int maxPagesToSearch);
}