
from sammy_logs.logs_general import Logs_list, sammy_str


def check_change_lbl(all_hist_qs, hist_obj, verbose_level=2):
    """
     Takes ANY action and summarizes the change with a addendum of _changed, _init, or _removed
       NOTE: this is only returning the addendum!!

    Clever and HIGHLY reusable!!  But let's not ALWAYs use it - use sparingly - probably best used in discovery

    This is Jira specific but should probably be an "option" every time - just only use on certain actions

    :param all_hist_qs: All events on this Ticket
    :param hist_obj: This event
    :return:
    """

    # Default - indicates unexpected scenario
    changed_lbl = '_UNK_1122'

    this_time_hist_ls_new = all_hist_qs.filter(action=hist_obj.action, date_time=hist_obj.date_time).exclude(new_key_val="")  #.order_by("date_time") # order_by unnneded?
    this_time_hist_ls_old = all_hist_qs.filter(action=hist_obj.action, date_time=hist_obj.date_time).exclude(old_key_val="")

    if len(this_time_hist_ls_old) > 0 and len(this_time_hist_ls_new) > 0:

        # print " ### check w both \n  " + smart_str(this_time_hist_ls_new[0]) + "|" + smart_str(this_time_hist_ls_old[0])

        # TODO : WAIT!! sometimes key is missing in assignee??????
        # http://127.0.0.1:8000/admin/tickets/history/?q=XERCESJ-800
        if hasattr(this_time_hist_ls_old[0], "old_key_val") and hasattr(this_time_hist_ls_new[0], "new_key_val") \
                and this_time_hist_ls_old[0].old_key_val != this_time_hist_ls_new[0].new_key_val:
            changed_lbl = '_changed'
        else:
            Logs_list.MINING_LOGS.log_lvl_1(" %%%% DID NOT FIND CHANGE TYPE **but** had new AND old??? " + sammy_str(hist_obj))

    elif len(this_time_hist_ls_old) == 0 and len(this_time_hist_ls_new) > 0:
        changed_lbl = '_init'
        if verbose_level > 4:
            Logs_list.MINING_LOGS.log_lvl_3(" #### FOUND AN INIT!! " + sammy_str(hist_obj))
    elif len(this_time_hist_ls_old) > 0 and len(this_time_hist_ls_new) == 0:
        changed_lbl = '_removed'
        if verbose_level > 4:
            Logs_list.MINING_LOGS.log_lvl_3(" #### FOUND AN REMOVED!! " + sammy_str(hist_obj))
    else:
        Logs_list.MINING_LOGS.log_lvl_2(" %%%% DID NOT FIND CHANGE TYPE?? " + sammy_str(hist_obj))

    return changed_lbl


def check_for_change_transaltions_no_repeat(all_hist_qs, hist_obj, change_actions_done,
                                            check_change_actions, use_sequences=False, verbose_level=2):
    """
    This evaluates all the same Hist records of the same action at the same time stamp

     Do not want to repeat either!

    """
    this_action = None

    if hist_obj.action in check_change_actions and hist_obj.action not in change_actions_done:

        chng_lbl = check_change_lbl(all_hist_qs, hist_obj)
        if len(chng_lbl) > 0:
            if verbose_level > 4:
                print " ^^NEW^^ a check_change_actions " + sammy_str(hist_obj.action) + " => " + check_change_actions[
                    hist_obj.action] + chng_lbl

            if use_sequences:
                if hist_obj.sequence_num is not None and hist_obj.sequence_num > 0:
                    # TODO: consider returning BOTH the seq and with label = so two labels for same event
                    this_action = check_change_actions[hist_obj.action] + "_" + str(hist_obj.sequence_num ) + "c_" + chng_lbl
                else:
                    this_action = check_change_actions[hist_obj.action] + "_?c_" + chng_lbl
            else:
                this_action = check_change_actions[hist_obj.action] + "_" + chng_lbl

            change_actions_done.append(hist_obj.action)

    elif hist_obj.action in change_actions_done:
        if verbose_level > 4:
            print " ___> already did " + str(hist_obj.action)

    return this_action, change_actions_done


def check_for_compound_transaltions_no_repeat_w_qs(all_hist_qs, hist_obj, compound_actions_done,
                                                   compound_convert_actions, verbose_level=2):
    """
    If in the proper config list and it hasnt been asserted yet, will combine action and event value
    :param all_hist_qs: All event records, this ticket
    :param hist_obj: this event row
    :param compound_actions_done: already used combo events
    :param compound_convert_actions: permitted events
    :return:
    """
    this_action_ls = []

    if hist_obj.action in compound_convert_actions and hist_obj.action not in compound_actions_done:
        if verbose_level > 4:
            print " ^^NEW^^ a COMPUND_convert_actions : " + smart_str(compound_convert_actions[hist_obj.action])

        compound_actions_done.append(hist_obj.action)

        this_action_ls = get_label_w_new_value_from_qs(all_hist_qs, hist_obj, compound_convert_actions)

        if verbose_level > 4:
            print " ##NEW## created COMPOUND ls :" + str(this_action_ls)

    return this_action_ls, compound_actions_done


#
def get_label_w_new_value_from_qs(all_hist_qs, hist_obj, simple_convert_actions):
    """
        Combines action and event value to create meaningful event label
    :param all_hist_qs: All event records, this ticket
    :param hist_obj:  this event row
    :param simple_convert_actions: permitted events
    :return:
    """

    res_ls = []
    converting_action = hist_obj.action

    if all_hist_qs is not None and len(all_hist_qs) > 0:  ## MOOT?
        #
        this_action_qs = all_hist_qs.filter(action=converting_action, new_val__isnull=False)

        for a_hist in this_action_qs:

            seq_lbl = simple_convert_actions[a_hist.action] + "_" + a_hist.new_val
            res_ls.append(seq_lbl)

    else:
        print " %%%%% ERROR - all_hist is None or empty |" + str(all_hist_qs) + "| while counting :" + str(hist_obj)

    return res_ls
