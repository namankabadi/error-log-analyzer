import tempfile
from error_log_analyzer import (
    generate_sample_logs,
    count_error_messages,
    find_top_k_errors
)

def test_error_counting():
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp:
        tmp.write(
            "[2024-01-01] [ERROR] Database connection timeout\n"
            "[2024-01-01] [ERROR] Database connection timeout\n"
            "[2024-01-01] [INFO] Request processed\n"
        )
        tmp.flush()

        counts = count_error_messages(tmp.name)

    assert counts["Database connection timeout"] == 2


def test_top_k_errors():
    data = {
        "E1": 10,
        "E2": 5,
        "E3": 1
    }
    top = find_top_k_errors(data, k=2)
    assert top[0][0] == "E1"
    assert len(top) == 2


def test_log_generation():
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        generate_sample_logs(tmp.name, total_requests=5)

    with open(tmp.name) as f:
        lines = f.readlines()

    assert len(lines) > 0
