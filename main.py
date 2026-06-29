import logging
from collections.abc import Generator

def read_url_list(path : str) -> Generator[str, None, None]:
    try: 
        with open(file=path, mode='r', encoding='utf-8') as file:
            for line in file:
                yield line.rstrip("\n")
    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
        raise
    except OSError as e:
        logging.error(f"OS error: {e}")
        raise

def main():
    FILE = "url_list.txt"
    generator = read_url_list(FILE)

    for url in generator:
        print(url)


if __name__ == "__main__":
    main()
