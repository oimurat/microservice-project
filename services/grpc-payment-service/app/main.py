import asyncio, service
import grpc, payment_pb2_grpc

async def serve():
    server = grpc.aio.server()
    payment_pb2_grpc.add_PaymentServiceServicer_to_server(service.PaymentService(), server)
    server.add_insecure_port("[::]:50054")
    await server.start()
    await server.wait_for_termination()

if __name__ == "__main__":
    asyncio.run(serve())