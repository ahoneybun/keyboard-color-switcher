import logging

logger = logging.getLogger(f'battery_backlight.{__name__}')


def read_file(path: str) -> str:
    with open(path, 'r') as f:
        data = f.read()
        logger.debug(f"Read {data} from {path}")
        return data if isinstance(data, str) else data.decode('utf-8')


def write_file(path: str, value: str):
    with open(path, 'wb') as f:
        logger.debug(f'Writing: {value} to {path}')
        f.write(value.encode())
