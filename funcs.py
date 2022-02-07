def croll_all_champ(driver):
    champ_list = []
    champs = driver.find_elements_by_class_name("champion-index__champion-item")
    for champ in champs:
        k_name = champ.get_attribute("data-champion-name")
        e_name = champ.get_attribute("data-champion-key")
        # print(k_name,e_name)
        champ_list.append(k_name)
        champ_list.append(e_name)
    return champ_list


def focus_next_window(event):
    event.widget.tk_focusNext().focus()
    return "break"


def focus_prev_window(event):
    event.widget.tk_focusPrev().focus()
    return "break"
