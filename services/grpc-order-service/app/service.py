import order_pb2, order_pb2_grpc

class OrderService(order_pb2_grpc.OrderServiceServicer):
    def PlaceOrder(self, request, context):
        print(f"[OrderService] PlaceOrder requested: {request.id}", flush=True)

        return order_pb2.OrderResponse(
            success=True,
            message="注文が成功しました"
        )
    
    def RefundOrder(self, request, context):
        print(f"[OrderService] RefundOrder requested: {request.id}", flush=True)

        return order_pb2.OrderResponse(
            success=True,
            message=f"注文 {request.id} の取消が完了しました"
        )