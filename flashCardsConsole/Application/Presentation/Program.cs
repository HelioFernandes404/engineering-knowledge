using Application.Core.Command;
using Application.Core.Interfaces;
using Application.Domain.Model;
using Application.Features.Decks.Commands;
using Application.Infrastructure.Persistence.Repositories;
using Application.Infrastructure.Persistence;
using Application.Services;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Application.Infrastructure.Persistence.Context;
using Application.Infrastructure.Services.TTSService;
using System.Diagnostics;
using Serilog;


class Program
{

    private static IServiceProvider _serviceProvider;

    static async Task Main()
    {
        var config = InitializeConfiguration();

        var services = new ServiceCollection()
            .AddScoped<IUnitOfWork, UnitOfWork>()
            .AddSingleton<IConfiguration>(config)
            .AddDbContext<AppDbContext>()
            .AddScoped<DeckServices>()
            .AddScoped<CardServices>()
            .AddScoped<AudioPlayer>()
            .AddSingleton(new TTSConfiguration
            {
                SpeakerId = "p339",
                StyleWav = "",
                LanguageId = ""
            })
            .AddScoped<TTSService>();
        Log.Logger = new LoggerConfiguration()
            .WriteTo.Console()
            .CreateLogger();

        Log.Fatal($"Healthy TTS");
        await StartDockerIfTtsIsHealthy();
 

        _serviceProvider = services.BuildServiceProvider();

        var commandInvoker = new CommandInvoker(_serviceProvider);

        commandInvoker.RegisterCommand("1", scope =>
            new ListDecksCommand(scope.ServiceProvider.GetRequiredService<DeckServices>()));

        commandInvoker.RegisterCommand("start", scope =>
        {
            var deckServices = scope.ServiceProvider.GetRequiredService<DeckServices>();
            return new StartDeckCommand(deckServices, 1);
        });

        commandInvoker.RegisterCommand("add", scope =>
        {
            var deckServices = scope.ServiceProvider.GetRequiredService<DeckServices>();
            var cardServices = scope.ServiceProvider.GetRequiredService<CardServices>();

            return new AddCardInDeckCommand(deckServices, cardServices, 1);
        });

        await InitializeDatabaseAsync();

        Console.WriteLine("\n1: Listar Baralhos");
        Console.WriteLine("2: Add /deckId");
        Console.WriteLine("3: Start /deckId");
        Console.WriteLine("Digite :q para sair");

        while (true)
        {
            var input = Console.ReadLine()?.ToLower();
            if (input == ":q")
            {
                using var scope = _serviceProvider.CreateScope();
                var context = scope.ServiceProvider.GetRequiredService<AppDbContext>();

                Log.Information("SaveChangesAsync...");
                await context.SaveChangesAsync();

                break;
            }

            if (!string.IsNullOrEmpty(input))
            {
                try
                {
                    await commandInvoker.ExecuteCommandAsync(input);
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Erro ao executar comando: {ex.Message}");
                }
            }
        }
    }

    private static async Task InitializeDatabaseAsync()
    {
        using var scope = _serviceProvider.CreateScope();
        var context = scope.ServiceProvider.GetRequiredService<AppDbContext>();

        Log.Information("Ensuring database is created...");
        await context.Database.EnsureCreatedAsync();

        if (!await context.Decks.AnyAsync())
        {
            var card1 = new Card { Question = "this is one card !", Answer = "nova carta?" };

            var cardsList = new List<Card> { card1 };

            await context.Decks.AddAsync(new Deck { Name = "Frases: Iniciais ", Cards = cardsList });
            await context.Decks.AddAsync(new Deck { Name = "Frases: Intermediárias  " });
            await context.Decks.AddAsync(new Deck { Name = "Frases: Avançadas  " });

            await context.SaveChangesAsync();
        }
    }

    private static IConfiguration InitializeConfiguration()
    {
        return new ConfigurationBuilder()
            .SetBasePath(AppContext.BaseDirectory)
            .AddJsonFile("appsettings.json", optional: false, reloadOnChange: true)
            .Build();
    }

    public static async Task StartDockerIfTtsIsHealthy()
    {
        AudioPlayer player = new AudioPlayer();

        bool healthCheckTts = await player.HealthCheckTts();

        if (healthCheckTts)
        {
            // Se o health check retornar true, iniciamos o Docker
            Console.WriteLine("TTS service is healthy.");
        }
        else
        {
            StartDocker();
        }
    }

    public static void StartDocker()
    {
        try
        {
            ProcessStartInfo startInfo = new ProcessStartInfo
            {
                FileName = "docker",
                Arguments = "run --rm -it -p 5002:5002 --entrypoint /bin/bash ghcr.io/coqui-ai/tts-cpu -c \"python3 TTS/server/server.py --model_name tts_models/en/vctk/vits\"",
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false,
                CreateNoWindow = true
            };

            using (Process process = new Process())
            {
                process.StartInfo = startInfo;
                process.Start();

                string output = process.StandardOutput.ReadToEnd();
                string error = process.StandardError.ReadToEnd();

                process.WaitForExit();

                Console.WriteLine(output);

                if (!string.IsNullOrEmpty(error))
                {
                    Console.WriteLine($"Error: {error}");
                }
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error starting Docker: {ex.Message}");
        }
    }
}