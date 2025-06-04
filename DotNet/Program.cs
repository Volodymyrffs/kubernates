using System;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;

class Program
{
    static async Task Main(string[] args)
    {
        var botToken = Environment.GetEnvironmentVariable("TELEGRAM_BOT_TOKEN");
        var chatId = Environment.GetEnvironmentVariable("TELEGRAM_CHAT_ID");

        if (string.IsNullOrEmpty(botToken) || string.IsNullOrEmpty(chatId))
        {
            Console.WriteLine("Missing environment variables TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID");
            return;
        }

        var message = new { chat_id = chatId, text = "Hello from .NET Docker container!" };
        var json = JsonSerializer.Serialize(message);

        using var client = new HttpClient();
        var response = await client.PostAsync(
            $"https://api.telegram.org/bot{botToken}/sendMessage",
            new StringContent(json, Encoding.UTF8, "application/json"));

        Console.WriteLine($"Message sent, status code: {response.StatusCode}");
    }
}
