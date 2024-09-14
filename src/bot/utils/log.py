from datetime import datetime


def debug(message: str) -> None:
    now = datetime.now()
    print(f'{now.strftime(r'%d.%m.%Y, %H:%M:%S.%f')}: {message}')