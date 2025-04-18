import asyncio, aio_pika, json
from temporalio.client import Client
from workflow import OrderWorkflow

async def main():
    print("[Consumer] consumer.py started", flush=True)

    connection = await aio_pika.connect_robust("amqp://user:pass@rabbitmq/")
    channel = await connection.channel()
    queue = await channel.declare_queue("order.created", durable=True)

    client = await Client.connect("temporal:7233")

    print("[Consumer] Waiting for 'order.created' events...", flush=True)

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                data = json.loads(message.body)
                print(f"[Consumer] Event received: {data}", flush=True)

                id = data["id"]
                item_id = data["item_id"]

                # ここで少し待機処理を挟む
                await asyncio.sleep(10)

                await client.start_workflow(
                    OrderWorkflow.run,
                    args=[id, item_id],
                    id=f"order-{id}",
                    task_queue="order-task-queue"
                )

                print(f"[✓] Started workflow for {id}", flush=True)

if __name__ == "__main__":
    asyncio.run(main())
