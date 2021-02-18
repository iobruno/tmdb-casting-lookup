import logging

logging.basicConfig(format="%(asctime)s %(levelname)s %(name)s - %(message)s",
                    level=logging.INFO,
                    datefmt="%Y-%m-%dT%H:%M:%S")


def get_logger(logger_name: str):
    return logging.getLogger(logger_name)
