from app_logger import AppLogger
from collections.abc import Generator
from pydantic import ValidationError, HttpUrl
import httpx
import asyncio
import time

logger = AppLogger(config_path="logging_config.json", logger_name=__name__).get_logger()


def read_url_list(path: str) -> Generator[str, None, None]:
    try:
        with open(file=path, mode="r", encoding="utf-8") as file:
            for line in file:
                yield line.rstrip("\n")
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        raise
    except OSError as e:
        logger.error(f"OS error: {e}")
        raise


async def fetch_url(url: str, client: httpx.AsyncClient):
    status = None
    error = None
    start = time.perf_counter()
    try:
        response = await client.get(url=url)
        # This raises HTTPStatusError for 4xx and 5xx responses
        response.raise_for_status()
        status = response.status_code
        logger.info(f"Success: Status code {response.status_code}")
    except httpx.HTTPStatusError as e:
        status = e.response.status_code
        error = str(e)
        logger.error(f"HTTP error {status} while fetching {url}")
    except httpx.RequestError as e:
        error = str(e)
        logger.error(f"Network error while fetching {url}: {e}")
    except Exception as e:
        error = str(e)
        logger.error(f"Something went wrong {e}")
    finally:
        elapsed_ms = (time.perf_counter() - start) * 1000
    return {
        'url': url,
        'status': status,
        'response_time_ms': elapsed_ms,
        'error': error
    }

async def main():
    FILE = "url_list.txt"
    valid_urls = []
    try:
        generator = read_url_list(FILE)
    except Exception as e:
        logger.error(f"Something went wrong: {e}")

    for item in generator:
        try:
            url = HttpUrl(url=item)
            valid_urls.append(str(url))
        except ValidationError as e:
            logger.error(f"Validation error for url {item}.\n{e}")

    async with httpx.AsyncClient() as client:
        tasks = [fetch_url(url, client=client) for url in valid_urls]
        results = await asyncio.gather(*tasks)
    
    for items in results:
        print(items)
        print("="*100)


if __name__ == "__main__":
    asyncio.run(main())
