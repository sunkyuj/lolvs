from main2 import (
    driver,
    master_list,
    match_listbox,
    master_btns,
    master_url_list,
    tabs,
    vs_tip_lb,
    my_ent,
    enemy_ent,
    champ_list,
)


def croll_all_champ():
    champ_list = []
    champs = driver.find_elements_by_class_name("champion-index__champion-item")
    for champ in champs:
        k_name = champ.get_attribute("data-champion-name")
        e_name = champ.get_attribute("data-champion-key")
        # print(k_name,e_name)
        champ_list.append(k_name)
        champ_list.append(e_name)
    return champ_list


def find_matchup(start):
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


def btn_clear():
    for i in range(0, 5):
        master_btns[i].configure(bg="SystemButtonFace", state="normal")


def change_btn_config():
    # global master_btns, master_list
    for i in range(0, 5):
        master_btns[i].configure(text=f"{i+1}.{master_list[i]}")
        master_btns[i].bind("<Button-1>", click_master)


def click_master(event):
    btn_clear()
    btn = event.widget
    btn.configure(state="disabled")
    global master_idx
    master_idx = int(btn["text"][0]) - 1
    driver.get(master_url_list[master_idx])
    global my_champ_name
    champ_match = driver.find_element_by_class_name("ChampionMatchSearchWrap")
    champ_match.find_element_by_class_name("Input").send_keys(my_champ_name)
    champ_match.find_element_by_class_name("Item.show").click()  # 클래스에 띄어쓰기 있으면 . 붙이자

    # 전적 한번에 20개씩 뜸
    global load_cnt
    load_cnt = 1
    find_matchup(load_cnt)

    return "break"


def get_vs_tip():
    # global my_champ_name, enemy_champ_name, vs_tip_lb
    psURL = f"https://lol.ps/versus/?champ1={my_champ_name}&champ2={enemy_champ_name}"
    driver.switch_to.window(tabs[1])  # lol.ps 탭으로 이동
    driver.get(psURL)
    tip_text = driver.find_element_by_class_name("guide-text").text  # 상대법 크롤링
    vs_tip_lb.configure(text=tip_text)


def get_masters():
    driver.switch_to.window(tabs[0])  # op.gg 탭으로 이동
    opggURL = f"https://www.op.gg/champion/{my_champ_name}/statistics"
    driver.get(opggURL)
    croll_masters = driver.find_elements_by_class_name(
        "champion-stats-summary-ranking__table__summoner"
    )

    master_list.clear()
    master_url_list.clear()
    for master in croll_masters:
        master_list.append(master.text)
        master_url = master.find_element_by_tag_name("a").get_attribute("href")
        master_url_list.append(master_url)


def search_vs():
    btn_clear()
    global my_champ_name, enemy_champ_name
    my_champ_name = my_ent.get("1.0", "end-1c")
    enemy_champ_name = enemy_ent.get("1.0", "end-1c")
    # print(my_champ_name,enemy_champ_name)
    if my_champ_name not in champ_list or enemy_champ_name not in champ_list:
        print("wrong input!!")
        return None

    get_vs_tip()
    get_masters()
    change_btn_config()

    return None


def focus_next_window(event):
    event.widget.tk_focusNext().focus()
    return "break"


def focus_prev_window(event):
    event.widget.tk_focusPrev().focus()
    return "break"


def press_enter():
    if my_ent.get("1.0", "end-1c") == "" or enemy_ent.get("1.0", "end-1c") == "":
        return "break"
    search_vs()
    return "break"
