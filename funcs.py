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


"""
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
    
def search_vs(my_ent, enemy_ent):
    btn_clear(master_btns)
    # global my_champ_name, enemy_champ_name
    my_champ_name = my_ent.get("1.0", "end-1c")
    enemy_champ_name = enemy_ent.get("1.0", "end-1c")
    # print(my_champ_name,enemy_champ_name)
    if my_champ_name not in champ_list or enemy_champ_name not in champ_list:
        print("wrong input!!")
        return None

    get_vs_tip()
    get_masters()
    change_btn_config(master_btns, master_list)

    return None


def find_matchup(start):
    from main import driver, master_list, match_listbox

    GameItemList = driver.find_element_by_class_name("GameItemList")

    # GameItemWrap = GameItemList.find_elements_by_class_name('GameItemWrap')

    for k in range(start, start + 20):
        # Teams = match.find_elements_by_class_name('Team')
        master_name = master_list[master_idx]
        idx = ()

        teams = []
        for i in range(1, 3):
            team = []
            for j in range(1, 6):
                champ = GameItemList.find_element_by_xpath(
                    f'//*[@id="SummonerLayoutContent"]/div[2]/div[2]/div/div[2]/div[3]/div[{k}]/div/div[1]/div[6]/div[{i}]/div[{j}]/div[1]/div[1]'
                ).text
                name = GameItemList.find_element_by_xpath(
                    f'//*[@id="SummonerLayoutContent"]/div[2]/div[2]/div/div[2]/div[3]/div[{k}]/div/div[1]/div[6]/div[{i}]/div[{j}]/div[2]/a'
                ).text
                if name == master_name:
                    idx = (i, j)
                team.append([champ, name])
                # /div[1]/div[1]
            teams.append(team)
        vs_idx = (2, idx[1] - 1) if idx[0] == 1 else (1, idx[1] - 1)
        vs_champ = teams[vs_idx[0]][vs_idx[1]][0]
        print(vs_champ)
        global enemy_champ_name
        if vs_champ == enemy_champ_name:
            # global match_listbox
            match_listbox.insert()

        else:
            continue

        # for team in Teams:

        # //*[@id="SummonerLayoutContent"]/div[2]/div[2]/div/div[2]/div[3]/div[1]/div/div[1]/div[6]/div[1]/div[1]/div[1]/div[1]
        # //*[@id="SummonerLayoutContent"]/div[2]/div[2]/div/div[2]/div[3]/div[1]/div/div[1]/div[6]/div[1]/div[2]/div[1]/div[1]
        # //*[@id="SummonerLayoutContent"]/div[2]/div[2]/div/div[2]/div[3]/div[1]/div/div[1]/div[6]/div[2]/div[1]/div[1]/div[1]

        # //*[@id="SummonerLayoutContent"]/div[2]/div[2]/div/div[2]/div[3]/div[4]/div/div[1]/div[6]/div[1]/div[3]
        # //*[@id="SummonerLayoutContent"]/div[2]/div[2]/div/div[2]/div[3]/div[4]/div/div[1]/div[6]/div[1]/div[3]/div[1]/div[1]
        # //*[@id="SummonerLayoutContent"]/div[2]/div[2]/div/div[2]/div[3]/div[4]/div/div[1]/div[6]/div[1]/div[3]/div[2]/div[1]

        #
        # f"//*[@id=\"SummonerLayoutContent\"]/div[2]/div[2]/div/div[2]/div[3]/div[{몇번째 매치인가}]/div/div[1]/div[6]/div[{i}]/div[{j}]/div[{1.챔,2.닉}]/div[1]"

    # class GameItemList <--전체
    # class GameItemWrap <--하나
    # class GameMoreButton.Box <--더보기버튼


def more_match():
    global load_cnt
    load_cnt += 20
    find_matchup(load_cnt)
    pass


"""
