from sentence_transformers import SentenceTransformer
import asyncio
import grpc
from grpc import aio
from generated import embedding_pb2 as api
from generated import embedding_pb2_grpc as grpc_server


class EmbeddingService(grpc_server.EmbeddingServiceServicer):
    def _init_(self) -> None:
        self._model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    def Embed(self, request, context):
        if request.texts is None:
            context.set_code(grpc.StatusCode.ABORTED)
            context.set_details("Missing texts to embed")
            context.abort()
        texts = list(request.texts)
        result = self._model.encode_query(texts) # type: ignore
        return api.EmbedResponse( # type: ignore
            data = result.tobytes(), # type: ignore
            shape = result.shape, # type: ignore
            dtype = str(result.dtype), # type: ignore
            fortran_order = result.flags["F_CONTIGUOUS"] # type: ignore
        )
        
        # response = api.EmbedResponse()  # type: ignore
        # # print(response)
        # # print(result.shape)
        # for embedding in result:
        #     vec = api.Vector() # type: ignore
        #     vec.dimension.extend(embedding.tolist()) # type: ignore
        #     response.vectors.append(vec)
        # for s in list(result.shape): # type: ignore
        #     response.shape.append(s)
        # return(response)
    
async def serve_async(port: int = 50051):
    server = aio.server()
    grpc_server.add_EmbeddingServiceServicer_to_server(EmbeddingService(), server=server)
    server.add_insecure_port(f"[::]:{port}")
    await server.start()
    print("server has started ...")
    await server.wait_for_termination()

if __name__ == "__main__":
    print("Starting server")
    asyncio.run(serve_async())