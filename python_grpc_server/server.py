from sentence_transformers import SentenceTransformer
import asyncio
import grpc
from grpc import aio
from generated import embedding_pb2 as api
from generated import embedding_pb2_grpc as grpc_server


class EmbeddingService(grpc_server.EmbeddingServiceServicer):
    def _init_(self) -> None:
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    def Embed(self, request, context):
        if request.texts is None:
            context.set_code(grpc.StatusCode.ABORTED)
            context.set_details("Missing texts to embed")
            context.abort()
        texts = list(request.texts)
        result = self._model.encode_query(texts) # type: ignore
        response = api.EmbedResponse()  # type: ignore
        for embedding in result:
            vec = api.Vector() # type: ignore
            vec.dimension.extend(embedding.toList())
            response.vectors.append(vec)
        response.shape = result.shape
        return(response)
    
async def serve_async(port: int = 500051):
    server = aio.server()
    grpc_server.add_EmbeddingServiceServicer_to_server(EmbeddingService(), server=server)
    server.add_insecure_port(f"[::]:{port}")
    await server.start()
    print("server has started ...")
    await server.wait_for_termination()

if __name__ == "__main__":
    print("Starting server")
    asyncio.run(serve_async())