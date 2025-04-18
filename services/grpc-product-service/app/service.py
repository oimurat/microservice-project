import product_pb2, product_pb2_grpc
from model import get_product_by_id

class ProductService(product_pb2_grpc.ProductServiceServicer):
    def GetProduct(self, request, context):
        data = get_product_by_id(request.id)
        print(f"📥 gRPC Request: id={request.id}, fields={request.fields}", flush=True)
        print(f"🧾 get_product_by_id result: {data}", flush=True)

        product = product_pb2.Product()

        for field in request.fields:
            if field in data:
                setattr(product, field, data[field])

        print(f"✅ Returning Product: {product}", flush=True)

        return product_pb2.ProductResponse(product=product)