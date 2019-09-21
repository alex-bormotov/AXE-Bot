from config import get_config


def dynamic_trail(last_change_percent):
    sell_trail_step = float(get_config()["sell_trail_step"])
    dyn_change_percent_for_trail_1 = float(get_config()["dyn_change_percent_for_trail_1"])
    dyn_change_percent_for_trail_2 = float(get_config()["dyn_change_percent_for_trail_2"])
    dyn_change_percent_for_trail_3 = float(get_config()["dyn_change_percent_for_trail_3"])
    dyn_change_percent_for_trail_4 = float(get_config()["dyn_change_percent_for_trail_4"])
    dyn_change_percent_for_trail_5 = float(get_config()["dyn_change_percent_for_trail_5"])
    dyn_trail_step_1 = float(get_config()["dyn_trail_step_1"])
    dyn_trail_step_2 = float(get_config()["dyn_trail_step_2"])
    dyn_trail_step_3 = float(get_config()["dyn_trail_step_3"])
    dyn_trail_step_4 = float(get_config()["dyn_trail_step_4"])
    dyn_trail_step_5 = float(get_config()["dyn_trail_step_5"])

    if last_change_percent > dyn_change_percent_for_trail_1:
        sell_trail_step = dyn_trail_step_1
    if last_change_percent > dyn_change_percent_for_trail_2:
        sell_trail_step = dyn_trail_step_2
    if last_change_percent > dyn_change_percent_for_trail_3:
        sell_trail_step = dyn_trail_step_3
    if last_change_percent > dyn_change_percent_for_trail_4:
        sell_trail_step = dyn_trail_step_4
    if last_change_percent > dyn_change_percent_for_trail_5:
        sell_trail_step = dyn_trail_step_5
    return sell_trail_step
