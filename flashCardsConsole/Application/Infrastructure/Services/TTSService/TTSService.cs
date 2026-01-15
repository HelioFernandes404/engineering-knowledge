using Application.Infrastructure.Services.External;
using Application.Services;


namespace Application.Infrastructure.Services.TTSService
{
    public class TTSService
    {
        private readonly TTSConfiguration _config;

        public TTSService(TTSConfiguration config)
        {
            _config = config ?? throw new ArgumentNullException(nameof(config));
        }

        public async Task ConvertTextToSpeechAndPlay(string text, string outputPath = "output.wav")
        {
            try
            {
                using var ttsClient = new TTSClient(_config);

                var audioBytes = await ttsClient.GetAudioBytesAsync(text);

                await File.WriteAllBytesAsync(outputPath, audioBytes);

                using var player = new AudioPlayer();
                await player.PlayAudioFileAsync(outputPath);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"An error occurred: {ex.Message}");
            }
        }
    }

}
