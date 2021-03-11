import logging


class Logger:
    def __init__(self, clevel=logging.DEBUG):
        self.logger = logging.getLogger('Main')
        self.logger.setLevel(logging.INFO)
        fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
        if not self.logger.hasHandlers():
            sh = logging.StreamHandler()
            sh.setFormatter(fmt)
            sh.setLevel(clevel)
            self.logger.addHandler(sh)

    def d(self, tag: str, *kwargs):
        self.logger.debug(tag + ' ' + ' '.join([str(x) for x in kwargs]))

    def i(self, tag: str, *kwargs):
        self.logger.info(tag + ' ' + ' '.join([str(x) for x in kwargs]))

    def w(self, tag: str, *kwargs):
        self.logger.warning(tag + ' ' + ' '.join([str(x) for x in kwargs]))

    def e(self, tag: str, *kwargs):
        self.logger.error(tag + ' ' + ' '.join([str(x) for x in kwargs]))

    def c(self, tag: str, *kwargs):
        self.logger.critical(tag + ' ' + ' '.join([str(x) for x in kwargs]))


Log = Logger()
