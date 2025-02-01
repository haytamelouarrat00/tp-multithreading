#!/usr/bin/env python3
# new_boss.py

import time
import logging
from QueueManager import QueueClient
from task import (
    Task,
)  # Ensure your Task class has appropriate methods (see Option 1 below)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Boss(QueueClient):
    def create_job(self, job_id: int, size: int) -> None:
        """
        Create a Task with a unique identifier and a given problem size, then
        enqueue it to the task queue.
        """
        task = Task(identifier=job_id, size=size)
        self.task_queue.put(task)
        logger.info("Job %d created.", job_id)

    def get_result(self) -> tuple:
        """
        Retrieve a completed task from the result queue and extract its identifier
        and execution time.
        """
        task = self.result_queue.get()
        # Use methods if available or access attributes directly
        job_id = (
            task.get_identifier()
            if hasattr(task, "get_identifier")
            else task.identifier
        )
        exec_time = task.get_time() if hasattr(task, "get_time") else task.time
        return job_id, exec_time


def main() -> None:
    boss = Boss()
    nb_jobs = 99
    problem_size = 1500

    logger.info("Boss is creating %d tasks (problem size: %d).", nb_jobs, problem_size)
    for job_id in range(nb_jobs):
        boss.create_job(job_id, problem_size)

    # Start measuring when the first result is received.
    first_result_time = None
    total_task_time = 0.0

    for _ in range(nb_jobs):
        job_id, exec_time = boss.get_result()
        if first_result_time is None:
            first_result_time = time.perf_counter()
        total_task_time += exec_time
        logger.info("Task %d executed in %.6f seconds.", job_id, exec_time)

    last_result_time = time.perf_counter()
    overall_elapsed = (
        last_result_time - first_result_time if first_result_time is not None else 0.0
    )

    logger.info("Sum of individual task times: %.6f seconds.", total_task_time)
    logger.info(
        "Total elapsed time (first to last result): %.6f seconds.", overall_elapsed
    )


if __name__ == "__main__":
    main()
