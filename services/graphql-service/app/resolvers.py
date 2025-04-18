import strawberry, aio_pika, json
from strawberry.types import Info
from typing import Optional

from grpc_clients import (
    grpc_cart,
    grpc_product,
    grpc_order,
    grpc_payment
)

async def publish_order_event(id: str, item_id: str) -> str:
    connection = await aio_pika.connect_robust("amqp://user:pass@rabbitmq/")
    channel = await connection.channel()

    message = aio_pika.Message(
        body=json.dumps({
            "id": id,
            "item_id": item_id
        }).encode()
    )

    await channel.default_exchange.publish(message, routing_key="order.created")
    await connection.close()
    
    return f"Order event published for {id}"

# DTO定義：Product
@strawberry.type
class Product:
    id: Optional[str]
    name: Optional[str]
    price: Optional[float]
    description: Optional[str]

# DTO定義：Cart
@strawberry.type
class Cart:
    id: Optional[str]
    product_id: Optional[str]
    quantity: Optional[int]


@strawberry.type
class Query:
    @strawberry.field
    def product(self, info: Info, id: str) -> Product:
        top = info.selected_fields[0]
        requested_fields = [f.name for f in top.selections]

        print(f"[GraphQL] リクエストフィールド: {requested_fields}", flush=True)

        product = grpc_product.get_product_by_id(id, fields=requested_fields)

        return Product(
            id=product.id if "id" in requested_fields else None,
            name=product.name if "name" in requested_fields else None,
            price=product.price if "price" in requested_fields else None,
            description=product.description if "description" in requested_fields else None,
        )

    @strawberry.field
    def cart(self, info: Info, id: str) -> Cart:
        top = info.selected_fields[0]
        requested_fields = [f.name for f in top.selections]

        print(f"[GraphQL] リクエストフィールド: {requested_fields}", flush=True)

        cart = grpc_cart.get_cart_by_id(id, fields=requested_fields)

        return Cart(
            id=cart.id if "id" in requested_fields else None,
            product_id=cart.product_id if "product_id" in requested_fields else None,
            quantity=cart.quantity if "quantity" in requested_fields else None,
        )


@strawberry.type
class Mutation:
    @strawberry.field
    def create_cart(self, id: str, product_id: str, quantity: int) -> str:
        return grpc_cart.create_cart(id=id, product_id=product_id, quantity=quantity)

    @strawberry.field
    def place_order(self, id: str, item_id: str, quantity: int) -> str:
        return grpc_order.place_order(id, item_id, quantity)

    @strawberry.field
    def refund_order(self, order_id: str) -> str:
        return grpc_order.refund_order(order_id)

    @strawberry.field
    def pay_order(self, order_id: str, amount: int) -> str:
        return grpc_payment.pay_order(order_id, amount)

    @strawberry.field
    async def workflow_order(self, order_id: str, item_id: str) -> str:
        return await publish_order_event(order_id, item_id)
