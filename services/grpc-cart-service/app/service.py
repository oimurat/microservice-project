import cart_pb2, cart_pb2_grpc
from model import create_cart, get_cart_by_id

class CartService(cart_pb2_grpc.CartServiceServicer):
    def GetCart(self, request, context):
        cart_data = get_cart_by_id(request.id)
        print(f"📥 gRPC Request: id={request.id}, fields={request.fields}", flush=True)

        cart = cart_pb2.Cart()

        for field in request.fields:
            if field in cart_data:
                setattr(cart, field, cart_data[field])

        print(f"✅ Returning Product: {cart}", flush=True)

        return cart_pb2.CartResponse(cart=cart)

    def CreateCart(self, request, context):
        print(f"[CartService] create_cart: {request}")

        create_cart(
            id=request.id,
            product_id=request.product_id,
            quantity=request.quantity
        )

        return cart_pb2.CreateCartResponse(
            message=f"Cart {request.id} created successfully."
        )