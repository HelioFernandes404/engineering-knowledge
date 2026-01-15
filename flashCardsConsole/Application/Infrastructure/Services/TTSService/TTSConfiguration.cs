using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Application.Infrastructure.Services.TTSService
{
    public class TTSConfiguration
    {
        public string BaseUrl { get; set; } = "http://localhost:5002/api/tts";
        public string SpeakerId { get; set; }
        public string StyleWav { get; set; }
        public string LanguageId { get; set; }
    }
}
