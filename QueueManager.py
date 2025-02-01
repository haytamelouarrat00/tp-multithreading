#!/usr/bin/env python3
"""
Queue Manager Module

This module provides both the server and client for managing task and result queues.
It uses multiprocessing.managers.BaseManager to allow remote access to shared Queue objects.
"""

import argparse
import logging
from multiprocessing import Queue
from multiprocessing.managers import BaseManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Default configuration
DEFAULT_PORT = 50000
DEFAULT_HOST = "localhost"
DEFAULT_AUTHKEY = b"pass"
DEFAULT_QUEUE_SIZE = 100


class TaskQueueManager(BaseManager):
    pass


class QueueClient:
    def __init__(
        self,
        host: str = DEFAULT_HOST,
        port: int = DEFAULT_PORT,
        authkey: bytes = DEFAULT_AUTHKEY,
    ) -> None:
        self.host = host
        self.port = port
        self.authkey = authkey

        # Register the queues (the server provides the callable)
        TaskQueueManager.register("get_task_queue")
        TaskQueueManager.register("get_result_queue")

        self.manager = TaskQueueManager(
            address=(self.host, self.port), authkey=self.authkey
        )
        self.manager.connect()

        self.task_queue = self.manager.get_task_queue()
        self.result_queue = self.manager.get_result_queue()
        logger.info("Connected to QueueManager at %s:%d", self.host, self.port)

    def get_task_queue(self) -> Queue:
        return self.task_queue

    def get_result_queue(self) -> Queue:
        return self.result_queue


def run_server(
    host: str = DEFAULT_HOST,
    port: int = DEFAULT_PORT,
    authkey: bytes = DEFAULT_AUTHKEY,
    queue_size: int = DEFAULT_QUEUE_SIZE,
) -> None:
    task_queue: Queue = Queue(queue_size)
    result_queue: Queue = Queue(queue_size)
    TaskQueueManager.register("get_task_queue", callable=lambda: task_queue)
    TaskQueueManager.register("get_result_queue", callable=lambda: result_queue)

    manager = TaskQueueManager(address=(host, port), authkey=authkey)
    server = manager.get_server()
    logger.info("Starting QueueManager server on %s:%d", host, port)
    server.serve_forever()


def main() -> None:
    parser = argparse.ArgumentParser(description="Queue Manager: Server or Client")
    parser.add_argument(
        "--mode",
        choices=["server", "client"],
        required=True,
        help="Run in server mode to start the queue server or in client mode to connect to it",
    )
    parser.add_argument(
        "--host",
        type=str,
        default=DEFAULT_HOST,
        help="Host address (default: localhost)",
    )
    parser.add_argument(
        "--port", type=int, default=DEFAULT_PORT, help="Port number (default: 50000)"
    )
    parser.add_argument(
        "--authkey",
        type=str,
        default=DEFAULT_AUTHKEY.decode("utf-8"),
        help="Authentication key (as string, will be encoded to bytes)",
    )

    args = parser.parse_args()
    authkey: bytes = args.authkey.encode("utf-8")

    if args.mode == "server":
        run_server(host=args.host, port=args.port, authkey=authkey)
    else:
        client = QueueClient(host=args.host, port=args.port, authkey=authkey)
        try:
            task_queue = client.get_task_queue()
            result_queue = client.get_result_queue()
            logger.info("Task queue size: %d", task_queue.qsize())
            logger.info("Result queue size: %d", result_queue.qsize())
        except Exception as e:
            logger.error("Failed to retrieve queues: %s", e)


if __name__ == "__main__":
    main()
