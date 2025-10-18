import logging
def get_logger(name: str = "agentic") -> logging.Logger:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    return logging.getLogger(name)
