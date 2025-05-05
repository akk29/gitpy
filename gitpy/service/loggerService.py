import logging
import threading

LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s --- %(message)s'

class Logger:

    _instance = None
    _lock = threading.Lock()

    @staticmethod
    def get_logger():
        if Logger._instance is None:
            Logger._lock.acquire()
            try:
                if Logger._instance is None:
                    logger = logging.getLogger(__name__)
                    logger.setLevel(logging.INFO)
                    handler = logging.StreamHandler()
                    formatter = logging.Formatter(LOGGING_FORMAT)
                    handler.setFormatter(formatter)
                    logger.addHandler(handler)
                    logger.propagate = False
                    Logger._instance = logger
            finally:
                Logger._lock.release()
        return Logger._instance