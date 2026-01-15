using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Application.Infrastructure.Services.TTSService;

namespace Application.Domain.Dto
{
    // TTSRequest.cs
    public class TTSRequest
    {
        private readonly TTSConfiguration _config;

        public TTSRequest(TTSConfiguration config)
        {
            _config = config;
        }

        public string BuildRequestUrl(string text)
        {
            return $"{_config.BaseUrl}?text={Uri.EscapeDataString(text)}" +
                   $"&speaker_id={_config.SpeakerId}" +
                   $"&style_wav={Uri.EscapeDataString(_config.StyleWav)}" +
                   $"&language_id={Uri.EscapeDataString(_config.LanguageId)}";
        }
    }
}
