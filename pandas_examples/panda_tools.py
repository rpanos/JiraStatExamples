
import pandas as pd

""" These are some of the reusable "wrappers" I used to make certain statictical functions easier """

def give_obj_at_perc_steps(dframe, column, step=.05, end_val=1):
    """

    :param dframe: The data frame of a Django QuerySet
    :param column: column in question
    :param step:  quantile step
    :param end_val:  how far to capture (0.0-1.0)
    :return:  A list of values at each quantile
    """
    res_ls = []
    tot = end_val / step
    for i in range(int(tot) + 1):
        q_s = i * step
        quant = dframe[column].quantile(q=q_s)
        res_ls.append(quant)
        print column + " ___________ " + str(q_s) + " = " + str(quant)

    return res_ls


def build_activity_sample_df():

    # This was the Django code - we will demo with an input file for now ...
    # adobejira_usr = User.objects.get(username="adobejira")
    # usr_st_ls = User_stat.objects.filter(user__server_key=Jira_servers.APACHE_SERVER) #.exclude(user=adobejira_usr) # exclude(user=adobejira_usr)

    user_stat_df = pd.read_csv("User_stat_sample_1000.csv")

    user_sample_df = pd.DataFrame({  'tot_history_count': give_obj_at_perc_steps(user_stat_df, 'tot_history_count_Jan_2015', step=.005),
                    'tot_history_create': give_obj_at_perc_steps(user_stat_df, 'tot_history_create_Jan_2015', step=.005),
                    'tot_history_resolve': give_obj_at_perc_steps(user_stat_df, 'tot_history_resolve_Jan_2015', step=.005),
                    'tot_history_comment': give_obj_at_perc_steps(user_stat_df, 'tot_history_comment_Jan_2015', step=.005)})

    file_name = 'exported_data/Hist_u_activity-TEST.csv'
    user_sample_df.to_csv(file_name, encoding='utf-8')

    return user_sample_df



# To demo
build_activity_sample_df()