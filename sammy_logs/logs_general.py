import pprint
from django.utils.encoding import smart_text

from sammy_logs.logs_manager import LogsCpt

__author__ = 'rpanos'


class Logs_list(object):
    """
        So that all modules can grab from the same static list
         . . takes advantage of code complete!
    """

    CAPTURE_LOGS = LogsCpt('logs', 'capture_e2_logs')
    SCRAPE_LOGS = LogsCpt('logs', 'scrape_e4_logs')
    VERIFICATION_LOGS = LogsCpt('logs', 'verification_g2_logs')
    METRICS_LOGS = LogsCpt('logs', 'metrics_e1_logs')
    CUSTOM_LOGS = LogsCpt('logs', 'custom_e2_logs')
    RESULTS_LOGS = LogsCpt('logs', 'results_e3_logs')
    MINING_LOGS = LogsCpt('logs', 'mining_b4_logs')
    GENERAL_LOGS = LogsCpt('logs', 'general_e1_logs')


def sammy_str(unk_obj):
    unk_str = " -Log Issue- "
    pp = pprint.PrettyPrinter(indent=4)

    try:
        unk_str = smart_text(unk_obj)
    except Exception as inst:

        Logs_list.GENERAL_LOGS.log_lvl_1(
            "%%%%%%% sammy_str ERR:" + str(type(inst)) + " ARG: " + pp.pformat(inst.args) + " INST: " + str(inst))

        print "%%% --- %% ERROR in  sammy_str "
        print str(type(inst))  # the exception instance
        print str(inst.args)  # arguments stored in .args
        print str(inst)  # __str__ allows args to printed directly

    return unk_str
