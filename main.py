from app_logger import AppLogger
from collections.abc import Generator
from pydantic import ValidationError, HttpUrl

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
