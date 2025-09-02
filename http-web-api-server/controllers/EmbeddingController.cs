using Microsoft.AspNetCore.Mvc;
using NplService;
using System.Runtime.InteropServices;

namespace grpc_client_web_api.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class EmbeddingController(EmbeddingService.EmbeddingServiceClient client) : ControllerBase
    {
        [HttpGet()]
        public async Task<IActionResult> EmbedText([FromQuery] string text)
        {
            var req = new EmbedRequest();
            req.Texts.Add(text);
            var res = await client.EmbedAsync(req);

            var bytes = res.Data.Span;
            var floats = MemoryMarshal.Cast<byte, double>(bytes);
            return Ok(floats.ToArray());
        }

    }
}