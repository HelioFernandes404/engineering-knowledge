using CrawlerAPI.Interfaces;
using CrawlerAPI.Services;

namespace CrawlerAPI.Configuration
{
    public static class DependencyInjectionConfig
    {
        public static IServiceCollection ResolveDependencies(this IServiceCollection services)
        {
            services.AddHttpClient();
            services.AddSingleton<ICrawlersServices, CrawlersServices>();

            return services;    
        }
    }
}
