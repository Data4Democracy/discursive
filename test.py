import sys
import logging
import time

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s')
    logger = logging.getLogger()
    logger.warn("started " + " ".join(sys.argv))
    time.sleep(65)
    logger.warn("stopped " + " ".join(sys.argv))
