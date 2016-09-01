
import pandas as pd

def give_obj_at_perc_steps_alt(dframe, column, step=.05, end_val=1):
    res_ls = []
    tot = end_val / step
    for i in range(int(tot) + 1):
        q_s = i * step
        quant = dframe[column].quantile(q=q_s)
        res_ls.append(quant)
        print column + " ___________ " + str(q_s) + " = " + str(quant)

    return res_ls