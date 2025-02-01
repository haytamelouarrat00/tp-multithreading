#!/usr/bin/env python3
import argparse
import logging
from QueueManager import QueueClient


def monitor_results(expected_count: int):
    client = QueueClient()
    logging.info("Monitoring result queue; expecting %d results...", expected_count)

    results = []
    while len(results) < expected_count:
        result = client.result_queue.get()  # This is a blocking call.
        # If the result isn’t already a dictionary, try to convert it.
        if not isinstance(result, dict):
            try:
                result = result.__dict__
            except Exception:
                pass
        results.append(result)
        logging.info("Received result %d/%d", len(results), expected_count)

    # Aggregate summary statistics
    summary_by_minion = {}
    overall_sum = 0.0
    overall_count = 0

    for res in results:
        # Expect each result to have a 'time' field (the execution time)
        # and optionally a 'minion' field indicating its source.
        minion_type = res.get("minion", "py")
        try:
            exec_time = float(res.get("time", 0))
        except (TypeError, ValueError):
            exec_time = 0.0

        overall_sum += exec_time
        overall_count += 1

        if minion_type not in summary_by_minion:
            summary_by_minion[minion_type] = {"count": 0, "sum": 0.0}
        summary_by_minion[minion_type]["count"] += 1
        summary_by_minion[minion_type]["sum"] += exec_time

    overall_avg = overall_sum / overall_count if overall_count > 0 else 0.0

    print("\n=== Execution Summary ===")
    print(f"Total tasks processed: {overall_count}")
    print(f"Overall average execution time: {overall_avg:.6f} seconds\n")

    for m_type, data in summary_by_minion.items():
        count = data["count"]
        sum_time = data["sum"]
        avg_time = sum_time / count if count > 0 else 0.0
        print(f"Minion type: {m_type}")
        print(f"    Count: {count}")
        print(f"    Sum of execution times: {sum_time:.6f} seconds")
        print(f"    Average execution time: {avg_time:.6f} seconds\n")


def main():
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(
        description="Monitor result queue and produce execution summary."
    )
    parser.add_argument(
        "--expected",
        type=int,
        required=True,
        help="Expected number of results (tasks) to wait for.",
    )
    args = parser.parse_args()
    monitor_results(args.expected)


if __name__ == "__main__":
    main()
