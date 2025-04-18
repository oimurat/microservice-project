import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from workflow import OrderWorkflow
from activities import process_order, charge_payment, refund_order

async def main():
    client = await Client.connect("temporal:7233")
    worker = Worker(
        client,
        task_queue="order-task-queue",
        workflows=[OrderWorkflow],
        activities=[process_order, charge_payment, refund_order],
    )

    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
