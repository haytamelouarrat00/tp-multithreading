import logging
from QueueManager import QueueClient
from task import Task  # Assuming Task is defined in task.py

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Minion(QueueClient):
    def __init__(self) -> None:
        super().__init__()
        logger.info("Minion initialized and connected to the queue server.")

    def do_job(self) -> None:
        try:
            task: Task = (
                self.task_queue.get()
            )  # Blocking call until a task is available
            job_id = task.get_identifier()
            task.work()
            exec_time = task.get_time()
            logger.info(
                "Job %d executed by a minion. Execution time: %s", job_id, exec_time
            )
            self.result_queue.put(task)
        except Exception as e:
            logger.exception("An error occurred while processing a job: %s", e)


def main() -> None:
    minion = Minion()
    try:
        while True:
            minion.do_job()
    except KeyboardInterrupt:
        logger.info("Minion interrupted. Exiting gracefully.")


if __name__ == "__main__":
    main()
