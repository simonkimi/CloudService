import logging
import time
import os


class Logger:
    def __init__(self, clevel=logging.DEBUG, flevel=logging.DEBUG):
        try:
            times = time.strftime("%m-%d-%H-%M-%S", time.localtime())
            # path = 'log/' + times + '.log'
            # if not os.path.exists('log'):
            #     os.mkdir('log')
            # with open(path, 'w') as f:
            #     f.write('')
            self.logger = logging.getLogger('Main')
            self.logger.setLevel(logging.INFO)
            fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
            # 设置CMD日志
            sh = logging.StreamHandler()
            sh.setFormatter(fmt)
            sh.setLevel(clevel)
            # # # 设置文件日志
            # fh = logging.FileHandler(path)
            # fh.setFormatter(fmt)
            # fh.setLevel(flevel)
            self.logger.addHandler(sh)
            self.logger.addHandler(fh)
        except:
            pass

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
