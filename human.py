def number_for_human(number):
    x_str = str(number)
    if "e-0" in x_str:
        return "%.08f" % number  # str
    else:
        return str(number)[:9]  # str
