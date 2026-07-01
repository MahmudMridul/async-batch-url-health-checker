from app_logger import AppLogger
from collections.abc import Generator
from pydantic import ValidationError, HttpUrl
import httpx

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


async def fetch_url(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url=url)
        logger.info(f"Status code: {response.status_code}")


def main():
    FILE = "url_list.txt"
    generator = read_url_list(FILE)

    for item in generator:
        try:
            url = HttpUrl(url=item)
        except ValidationError as e:
            logger.error(f"Validation error: {e}")


if __name__ == "__main__":
    main()
