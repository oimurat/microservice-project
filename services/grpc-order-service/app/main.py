import asyncio, service
import grpc, order_pb2_grpc

async def serve():
    server = grpc.aio.server()
    order_pb2_grpc.add_OrderServiceServicer_to_server(service.OrderService(), server)
    server.add_insecure_port("[::]:50053")
    await server.start()
    await server.wait_for_termination()

if __name__ == "__main__":
    asyncio.run(serve())