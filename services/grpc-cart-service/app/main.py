import asyncio, service
import grpc, cart_pb2_grpc

async def serve():
    server = grpc.aio.server()
    cart_pb2_grpc.add_CartServiceServicer_to_server(service.CartService(), server)
    server.add_insecure_port('[::]:50051')
    await server.start()
    await server.wait_for_termination()

if __name__ == "__main__":
    asyncio.run(serve())