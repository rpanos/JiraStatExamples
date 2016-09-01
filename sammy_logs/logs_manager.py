
import logging
import pprint

__author__ = 'Rpanos'


class SammyLog():
    """
        This really just is a light weight wrapper around the logging package
    """

    def __init__(self, dir_name, log_name):
        self.dir_name = dir_name
        self.log_name = log_name
        self.this_logger = self.__set_logs__()

    def __set_logs__(self):

        this_logger = logging.getLogger(self.log_name)
        this_logger.setLevel(logging.DEBUG)  ## Basicallty all

        # create file handler which logs even debug messages
        fhc = logging.FileHandler(self.dir_name + '/' + self.log_name + '_CRITICAL.log')
        fhc.setLevel(logging.CRITICAL)

        fhe = logging.FileHandler(self.dir_name + '/' + self.log_name + '_ERR.log')
        fhe.setLevel(logging.ERROR)

        fhw = logging.FileHandler(self.dir_name + '/' + self.log_name + '_WARN.log')
        fhw.setLevel(logging.WARNING)

        fhi = logging.FileHandler(self.dir_name + '/' + self.log_name + '_INFO.log')
        fhi.setLevel(logging.INFO)

        fhd = logging.FileHandler(self.dir_name + '/' + self.log_name + '_DEBUG.log')
        fhd.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s : %(message)s')
        fhe.setFormatter(formatter)
        fhw.setFormatter(formatter)
        fhc.setFormatter(formatter)
        fhd.setFormatter(formatter)
        fhi.setFormatter(formatter)

        # add the handlers to the logger
        this_logger.addHandler(fhe)
        this_logger.addHandler(fhw)
        this_logger.addHandler(fhc)
        this_logger.addHandler(fhd)
        this_logger.addHandler(fhi)

        return this_logger


class LogsManager(object):
    """
        Allows for new function names in logger with default names
    """
    _log_library = {}
    mangerCount = 0

    def __init__(self, dir_name='logs', log_name='main_log'):

        if log_name not in LogsManager._log_library:
            sammy_log = SammyLog(dir_name, log_name)
            LogsManager._log_library[log_name] = sammy_log
            LogsManager.mangerCount += 1

    def get_sammy_log(self, log_name='main_log'):

        if log_name in LogsManager._log_library:
            return LogsManager._log_library[log_name]
        else:
            print "%% NO LOG BY THAT NAME : ", log_name

    def log_lvl_0(self, message, log_name='main_log'):
        lgr = self.get_sammy_log(log_name)
        lgr.this_logger.critical(message)

    def log_lvl_1(self, message, log_name='main_log'):
        lgr = self.get_sammy_log(log_name)
        lgr.this_logger.error(message)

    def log_lvl_2(self, message, log_name='main_log'):
        lgr = self.get_sammy_log(log_name)
        lgr.this_logger.warning(message)

    def log_lvl_3(self, message, log_name='main_log'):
        lgr = self.get_sammy_log(log_name)
        lgr.this_logger.info(message)

    def log_lvl_4(self, message, log_name='main_log'):
        p_print = pprint.PrettyPrinter(indent=4)
        lgr = self.get_sammy_log(log_name)
        p_print.pprint(lgr)
        lgr.this_logger.debug(message)

    def test_logs(self, log_name='main_log', test_flag=''):
        if log_name in self._log_library:
            self._log_library[log_name].test_this_logger(test_flag)
        else:
            print "NO LOG BY THAT NAME : ", log_name


class LogsCpt(object):
    log_name = ""
    sammy_log = {}

    def __init__(self, dir_name='logs', log_name='main_log'):

        # print "GET LOGS in init!!  for " + log_name
        self.sammy_log = SammyLog(dir_name, log_name)

    def log_lvl_0(self, message):
        try:
            self.sammy_log.this_logger.critical(message)
        except Exception as inst:
            self.sammy_log.this_logger.critical("String Issue") + " type:" + type(inst)

    def log_lvl_1(self, message):
        try:
            self.sammy_log.this_logger.error(message)
        except Exception as inst:
            self.sammy_log.this_logger.error("String Issue") + " type:" + type(inst)

    def log_lvl_2(self, message):
        try:
            self.sammy_log.this_logger.warning(message)
        except Exception as inst:
            self.sammy_log.this_logger.warning("String Issue") + " type:" + type(inst)

    def log_lvl_3(self, message):
        try:
            self.sammy_log.this_logger.info(message)
        except Exception as inst:
            self.sammy_log.this_logger.info("String Issue") + " type:" + type(inst)

    def log_lvl_4(self, message):
        try:
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(self.sammy_log)
            self.sammy_log.this_logger.debug(message)
        except Exception as inst:
            self.sammy_log.this_logger.debug("String Issue")  + " type:" + type(inst)

    def test_logger(self):
        self.sammy_log.this_logger.test_this_logger
