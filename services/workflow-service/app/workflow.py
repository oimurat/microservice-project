from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy
from activities import process_order, charge_payment, refund_order

@workflow.defn
class OrderWorkflow:
    @workflow.run
    async def run(self, id: str, item_id: str):
        try:
            # 1回だけリトライ
            await workflow.execute_activity(
                process_order,
                args=[id, item_id],
                start_to_close_timeout=timedelta(seconds=30),
                retry_policy=RetryPolicy(
                    initial_interval=timedelta(seconds=2),
                    maximum_attempts=1,
                    backoff_coefficient=2.0
                )
            )

            await workflow.execute_activity(
                charge_payment,
                args=[id],
                start_to_close_timeout=timedelta(seconds=30),
                retry_policy=RetryPolicy(
                    initial_interval=timedelta(seconds=2),
                    maximum_attempts=1,
                    backoff_coefficient=2.0
                )
            )

        except Exception as e:
            # エラーが発生した場合はrefund_orderを実行し、ワークフローを終了
            await workflow.execute_activity(
                refund_order,
                args=[id],
                start_to_close_timeout=timedelta(seconds=30),
                retry_policy=RetryPolicy(
                    initial_interval=timedelta(seconds=2),
                    maximum_attempts=1,
                    backoff_coefficient=2.0
                )
            )
            raise e  # エラーを再送出してワークフローを終了
