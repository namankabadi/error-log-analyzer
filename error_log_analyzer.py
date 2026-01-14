"""
========================================================
ERROR LOG ANALYZER 
========================================================

✔ Behavior-driven log generation
✔ Streaming file processing (10GB safe)
✔ Generator-based I/O
✔ defaultdict-based counting
✔ Top-K extraction
✔ Production-grade logging
✔ Ready for distributed extension

Author: Naman Kabadi
========================================================
"""

import logging
import random
from datetime import datetime, timedelta
from collections import defaultdict
from heapq import nlargest
from typing import Generator, Dict

# ------------------------------------------------------
# LOGGING CONFIGURATION
# ------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# ------------------------------------------------------
# REALISTIC SYSTEM EVENTS
# ------------------------------------------------------

REQUEST_EVENTS = [
    "Incoming API request",
    "Request validation successful",
    "User authenticated",
    "Response sent successfully"
]

DEBUG_EVENTS = [
    "Executing database query",
    "Cache lookup initiated",
    "Calling downstream service"
]

WARN_EVENTS = [
    "Retrying database connection",
    "Downstream service latency high",
    "Cache miss detected"
]

ERROR_EVENTS = [
    "Database connection timeout",
    "Authentication service unavailable",
    "Disk space exhausted",
    "Unhandled null pointer exception"
]

# ------------------------------------------------------
# REALISTIC LOG GENERATION (BEHAVIOR DRIVEN)
# ------------------------------------------------------

def generate_sample_logs(file_path: str, total_requests: int = 60) -> None:
    """
    Generates realistic logs based on request lifecycle behavior.
    """
    logging.info("Starting realistic log generation...")
    current_time = datetime.now()

    with open(file_path, "w") as file:
        for request_id in range(total_requests):
            # INFO: request start
            file.write(f"[{current_time}] [INFO] Incoming API request\n")
            current_time += timedelta(seconds=1)

            # DEBUG: internal steps
            for _ in range(random.randint(1, 2)):
                file.write(f"[{current_time}] [DEBUG] {random.choice(DEBUG_EVENTS)}\n")
                current_time += timedelta(seconds=1)

            # WARN + ERROR probability
            if random.random() < 0.35:
                file.write(f"[{current_time}] [WARN] {random.choice(WARN_EVENTS)}\n")
                current_time += timedelta(seconds=1)

                if random.random() < 0.6:
                    file.write(f"[{current_time}] [ERROR] {random.choice(ERROR_EVENTS)}\n")
                    current_time += timedelta(seconds=1)
                    continue  # request failed

            # INFO: success
            file.write(f"[{current_time}] [INFO] Response sent successfully\n")
            current_time += timedelta(seconds=1)

    logging.info(f"Log file generated at: {file_path}")
    logging.info(f"Total requests simulated: {total_requests}")

# ------------------------------------------------------
# STREAMING LOG READER
# ------------------------------------------------------

def read_log_file(file_path: str) -> Generator[str, None, None]:
    """
    Generator for streaming large log files.
    """
    logging.info("Reading log file in streaming mode...")
    with open(file_path, "r") as file:
        for line in file:
            yield line.strip()

# ------------------------------------------------------
# ERROR MESSAGE COUNTING
# ------------------------------------------------------

def count_error_messages(file_path: str) -> Dict[str, int]:
    """
    Counts ERROR messages using constant memory.
    """
    logging.info("Analyzing ERROR messages...")
    error_counter = defaultdict(int)
    total_lines = 0
    error_lines = 0

    for line in read_log_file(file_path):
        total_lines += 1
        try:
            parts = line.split("] ", 2)
            level = parts[1][1:]

            if level == "ERROR":
                error_lines += 1
                message = parts[2]
                error_counter[message] += 1

        except IndexError:
            logging.warning("Malformed log line skipped")

    logging.info(f"Lines processed: {total_lines}")
    logging.info(f"ERROR lines found: {error_lines}")

    return error_counter

# ------------------------------------------------------
# TOP-K EXTRACTION
# ------------------------------------------------------

def find_top_k_errors(error_counter: Dict[str, int], k: int = 5):
    logging.info(f"Extracting top {k} ERROR messages...")
    return nlargest(k, error_counter.items(), key=lambda x: x[1])

# ------------------------------------------------------
# MAIN
# ------------------------------------------------------

def main():
    log_file = "application.log"

    logging.info("=" * 70)
    logging.info("ERROR LOG ANALYZER STARTED")
    logging.info("=" * 70)

    generate_sample_logs(log_file, total_requests=80)
    error_counts = count_error_messages(log_file)
    top_errors = find_top_k_errors(error_counts, 5)

    logging.info("=" * 70)
    logging.info("TOP 5 ERROR MESSAGES")
    logging.info("=" * 70)

    for idx, (msg, count) in enumerate(top_errors, start=1):
        logging.info(f"{idx}. {msg} → {count} occurrences")

    logging.info("=" * 70)
    logging.info("ANALYSIS COMPLETED")
    logging.info("=" * 70)

if __name__ == "__main__":
    main()
