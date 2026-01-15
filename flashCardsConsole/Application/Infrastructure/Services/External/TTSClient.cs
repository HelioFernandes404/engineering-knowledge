using Application.Domain.Dto;
using Application.Infrastructure.Services.TTSService;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Application.Infrastructure.Services.External
{
    // TTSClient.cs
    public class TTSClient : IDisposable
    {
        private readonly HttpClient _httpClient;
        private readonly TTSRequest _ttsRequest;

        public TTSClient(TTSConfiguration config)
        {
            _httpClient = new HttpClient();
            _ttsRequest = new TTSRequest(config);
        }

        public async Task<byte[]> GetAudioBytesAsync(string text)
        {
            var requestUrl = _ttsRequest.BuildRequestUrl(text);
            var response = await _httpClient.GetAsync(requestUrl);
            response.EnsureSuccessStatusCode();
            return await response.Content.ReadAsByteArrayAsync();
        }

        public void Dispose()
        {
            _httpClient.Dispose();
        }
    }
}
