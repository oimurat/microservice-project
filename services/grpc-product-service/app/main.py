import asyncio, service
import grpc, product_pb2_grpc

async def serve():
    server = grpc.aio.server()
    product_pb2_grpc.add_ProductServiceServicer_to_server(service.ProductService(), server)
    server.add_insecure_port('[::]:50052')
    await server.start()
    await server.wait_for_termination()

if __name__ == "__main__":
    asyncio.run(serve())