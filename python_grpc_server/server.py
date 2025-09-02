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
    
