import requests
import payment_pb2, payment_pb2_grpc

class PaymentService(payment_pb2_grpc.PaymentServiceServicer):
    def PayOrder(self, request, context):

        print(f"🧾 決済処理: Order ID={request.order_id}, Amount={request.amount}")

        return payment_pb2.PaymentResponse(
            success=True,
            message="決済が成功しました"
        )
