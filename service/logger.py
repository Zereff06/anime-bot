from loguru import logger

def start():
    logger.add("logs/log.json",
           format="{time} {level} {message}",
           level="DEBUG",
           rotation="512 KB",
           compression="zip",
           serialize=True
           )