from loguru import logger


def start():
    logger.add("src/logs/log.log",
               format="{time: HH:mm} {level} {message}",
               level="INFO",
               rotation="1024 KB",
               compression="zip",
               serialize=True
               )
