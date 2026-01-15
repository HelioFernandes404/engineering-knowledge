using RabbitMQ.Client;
using System.Text;
using RabbitMQ.Client.Events;

var factory = new ConnectionFactory {HostName = "localhost" };
using var connection = factory.CreateConnection();
using var channel = connection.CreateModel();

channel.QueueDeclare(queue: "hello",
    durable: false,
    exclusive: false,
    autoDelete: false, arguments: null);
    
    Console.WriteLine(" [*] Agurdado messagem.");
    
    var consumidor = new EventingBasicConsumer(channel);
    consumidor.Received += (model, ea) =>
    {
        var corpo = ea.Body.ToArray();
        var msg = Encoding.UTF8.GetString(corpo);
        
        Console.WriteLine($" [x] Recebido: {msg}");
    };
    
    channel.BasicConsume(queue: "hello", autoAck: true, consumer: consumidor);
    
    Console.WriteLine(" Apeter [enter] para sair.");
    Console.ReadLine();
    