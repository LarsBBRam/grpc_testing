using System.Runtime.InteropServices;
using Microsoft.AspNetCore.Mvc;
using NplService;

AppContext.SetSwitch("System.Net.Http.SocketsHttpHandler.Http2UnencryptedSupport", true);

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
// Learn more about configuring OpenAPI at https://aka.ms/aspnet/openapi
builder.Services.AddOpenApi();
builder.Services.AddControllers();
builder.Services.AddGrpcClient<EmbeddingService.EmbeddingServiceClient>(options =>
{
    options.Address = new Uri("http://localhost:50051");
});

var app = builder.Build();
app.MapControllers();
// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();
}

app.UseHttpsRedirection();

// app.MapGet("embed", async (EmbeddingService.EmbeddingServiceClient client, [FromQuery] string text) =>
// {
//     var request = new EmbedRequest();
//     request.Texts.Add(text);
//     var response = await client.EmbedAsync(request);
//     var bytes = response.Data.Span;
//     var doubles = MemoryMarshal.Cast<byte, double>(bytes);
//     return doubles;
// });

app.Run();
