# Async Batch URL Health Checker

A small async Python tool that reads a list of URLs, validates them, and checks their health concurrently using `httpx` and `asyncio`. Results include HTTP status, response time, and any errors encountered.

## Features

- Concurrent URL checks using `asyncio.gather` with a semaphore to cap in-flight requests
- URL validation via Pydantic's `HttpUrl` before making any requests
- Per-URL results: status code, response time (ms), and error message (if any)
- Structured logging to both console and a daily-rotating log file (`logs/app.log`)

## Requirements

- Python >= 3.14
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

## Installation

```bash
uv sync
```

Or with pip:

```bash
pip install httpx pydantic
```

## Usage

1. Add the URLs you want to check to `url_list.txt`, one per line.
2. Run the checker:

```bash
uv run main.py
```

Each result is printed to the console in the form:

```python
{'url': 'https://example.com/', 'status': 200, 'response_time_ms': 123.45, 'error': None}
```

Invalid URLs are skipped and logged as validation errors; they are not included in the results.

## Configuration

- **Concurrency**: controlled by the `asyncio.Semaphore` value in `main()` (default: 5).
- **Input file**: set via the `FILE` constant in `main()` (default: `url_list.txt`).
- **Logging**: configured in `logging_config.json` — console output at `DEBUG` level, file output at `INFO` level with daily rotation and a 2-day backup.

## Project Structure

```
main.py               # Entry point: reads URLs, validates them, runs health checks
app_logger.py          # AppLogger: loads logging config and provisions the log directory
logging_config.json     # Logging configuration (formatters, handlers, levels)
url_list.txt            # Input list of URLs to check
logs/                    # Rotating log files (generated at runtime)
```
