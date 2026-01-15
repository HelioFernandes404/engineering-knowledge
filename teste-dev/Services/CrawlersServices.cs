using CrawlerAPI.Interfaces;
using CrawlerAPI.Model;
using CrawlerAPI.Model.enums;
using HtmlAgilityPack;

namespace CrawlerAPI.Services;

public class CrawlersServices : ICrawlersServices
{
    private readonly HttpClient _httpClient;
    private HashSet<string> _visitedUrls;
    private List<string> _crawledLinks;
    private readonly int _maxDepth;
    private int _maxPagesToSearch;

    public CrawlersServices(HttpClient httpClient)
    {
        _httpClient = httpClient;
        _visitedUrls = new HashSet<string>();
        _crawledLinks = new List<string>();
        _maxDepth = (int)SearchDepthEnums.MAX_DEPTH;
    }
    
    public async Task<CrawlerResponse> GetCrawlWebSite(string startUrl, int depth, int maxPagesToSearch)
    {
        _visitedUrls.Clear();
        _crawledLinks.Clear();
        _maxPagesToSearch = maxPagesToSearch;
        
        await CrawlAsync(startUrl, depth);

        return new CrawlerResponse
        {
            LinksFounds = _crawledLinks.Take(maxPagesToSearch).ToList(),
            MoreLinksFounds = _crawledLinks.Count
        };
    }

    // Recursividade
    async Task CrawlAsync(string url, int depth)
    {
        if (ShouldStopCrawling(depth, url)) return;
        
        _visitedUrls.Add(url);

        try
        {
            string pageContent = await GetPageContentAsync(url);

            if (string.IsNullOrEmpty(pageContent)) return;
    
            var links = ExtractLinksFromContent(pageContent, url);
            foreach (var href in links)
            {
                if (_visitedUrls.Count >= _maxPagesToSearch) break;
                _crawledLinks.Add(href);
                await CrawlAsync(href, depth + 1);
            }
        }
        catch (Exception e)
        {
            Console.WriteLine($"Erro ao acessar a página {url}: {e.Message}");
        }
    }

    private IEnumerable<string> ExtractLinksFromContent(string content, string baseUrl)
    {
        HtmlDocument doc = new HtmlDocument();
        doc.LoadHtml(content);
        
        var links = doc.DocumentNode.SelectNodes("//a[@href]");
        if (links == null) return Enumerable.Empty<string>();
        
        return links.Select(link => GetAbsoluteUrl(link.GetAttributeValue("href", string.Empty), baseUrl))
            .Where(href => !string.IsNullOrEmpty(href) && IsValidUrl(href));
    }
    
    private string GetAbsoluteUrl(string href, string baseUrl)
    {
        if (Uri.IsWellFormedUriString(href, UriKind.Relative))
        {
            var baseUri = new Uri(baseUrl);
            return new Uri(baseUri, href).ToString();
        }
        return href;
    }

    private async Task<string> GetPageContentAsync(string url)
    {
        try
        {
            return await _httpClient.GetStringAsync(url);
        }
        catch (Exception e)
        {
            Console.WriteLine($"Erro ao obter o conteúdo da página {url}: {e.Message}");
            return null;
        }
    }

    private bool ShouldStopCrawling(int depth, string url)
    {
        return _crawledLinks.Count >= _maxPagesToSearch || _visitedUrls.Contains(url) || depth > _maxDepth;
    }
    
    private bool IsValidUrl(string href)
    {
        if (!Uri.IsWellFormedUriString(href, UriKind.Absolute)) return false;

        Uri uri = new Uri(href);
        return uri.Scheme == Uri.UriSchemeHttp || uri.Scheme == Uri.UriSchemeHttps;
    }
}
