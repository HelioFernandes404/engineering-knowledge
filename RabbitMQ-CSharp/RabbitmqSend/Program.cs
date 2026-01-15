using RabbitMQ.Client;
using System.Text;

var factory = new ConnectionFactory {HostName = "localhost" };
using var connection = factory.CreateConnection();
using var channel = connection.CreateModel();

channel.QueueDeclare(queue: "hello",
    durable: false,
    exclusive: false,
    autoDelete: false,
    arguments: null);
    
    Console.WriteLine("Digite sua messagem e parte <ENTER>");

    while (true)
    {
        string msg = Console.ReadLine();

        if (msg == "")
        {
            break;
        }
        
        //var aluno = new Aluno() { Id = 1, Nome = Milton" }
        //msg = JsonSerializer.Serialize(aluno);

        var body = Encoding.UTF8.GetBytes(msg);
        
        channel.BasicPublish(exchange: string.Empty, routingKey: "hello", basicProperties: null, body: body);
        
        Console.WriteLine($" [x] Enviado: {msg} ");
    }

    class Aluno
    {
        public int Id {get; set; }
        public string Nome {get; set; }
    }