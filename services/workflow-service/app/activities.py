from temporalio import activity
import grpc
import order_pb2, order_pb2_grpc
import payment_pb2, payment_pb2_grpc

# gRPCクライアント初期化（docker-compose 上のサービス名を使う）
order_channel = grpc.insecure_channel("grpc-order-service:50053")
order_stub = order_pb2_grpc.OrderServiceStub(order_channel)

payment_channel = grpc.insecure_channel("grpc-payment-service:50054")
payment_stub = payment_pb2_grpc.PaymentServiceStub(payment_channel)

@activity.defn
async def process_order(id: str, item_id: str):
    quantity = 1
    request = order_pb2.OrderRequest(id=id, item_id=item_id, quantity=quantity)
    response = order_stub.PlaceOrder(request)

    print(f"[Activity] Order placed: {response.message}", flush=True)

    return response.message

@activity.defn
async def charge_payment(order_id: str):
    amount = 1000
    request = payment_pb2.PaymentRequest(order_id=order_id, amount=amount)
    response = payment_stub.PayOrder(request)

    print(f"[Activity] Payment charged: {response.message}", flush=True)

    return response.message

@activity.defn
async def refund_order(id: str):
    request = order_pb2.RefundRequest(id=id)
    response = order_stub.RefundOrder(request)

    print(f"[Activity] Order refunded: {response.message}", flush=True)

    return response.message
