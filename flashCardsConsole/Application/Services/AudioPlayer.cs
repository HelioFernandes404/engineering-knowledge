using NAudio.Wave;

namespace Application.Services
{
    public class AudioPlayer : IDisposable
    {
        private WaveOutEvent _outputDevice;
        private AudioFileReader _audioFile;

        public AudioPlayer(WaveOutEvent outputDevice, AudioFileReader audioFile)
        {
            _outputDevice = outputDevice;
            _audioFile = audioFile;
        }

        public AudioPlayer()
        {
        }

        public async Task PlayAudioFileAsync(string filePath)
        {
            _audioFile = new AudioFileReader(filePath);
            _outputDevice = new WaveOutEvent();
            _outputDevice.Init(_audioFile);

            _outputDevice.PlaybackStopped += (sender, args) =>
            {
                _outputDevice.Stop();
            };

            _outputDevice.Play();

            while (_outputDevice.PlaybackState == PlaybackState.Playing)
            {
                await Task.Delay(1000);
            }
        }


        public async Task<bool> HealthCheckTts()
        {
            using (HttpClient client = new HttpClient())
            {
                try
                {
                    HttpResponseMessage response = await client.GetAsync("http://localhost:5002/api/tts");
                    if (response.IsSuccessStatusCode)
                    {
                        return true;
                    }
                }
                catch (HttpRequestException)
                {
                    return false;
                }
            }

            return false;
        }

        public void Dispose()
        {
            _audioFile?.Dispose();
            _outputDevice?.Dispose();
        }
    }
}
