from logging import PlaceHolder
from bs4 import BeautifulSoup
from selenium import webdriver
from tkinter import *
from selenium.webdriver.common.keys import Keys
from urllib3.packages.six import b
from multiprocessing import Pool
import chrome_auto_upgrade
import funcs

#############  func   #############
'''
셀레니움 비동기 크롤링
result = dirver.execute_async_script(""" 
var done = arguments[0]; 
require(["foo"], function (foo) {
     done(foo.computeSomething());
    });
 """)

'''


def croll_all_champ():
    champs = driver.find_elements_by_class_name("champion-index__champion-item")
    for champ in champs:
        k_name = champ.get_attribute("data-champion-name")
        e_name = champ.get_attribute("data-champion-key")
        # print(k_name,e_name)
        champ_list.append(k_name)
        champ_list.append(e_name)


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
            global match_listbox
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
    global master_btns, master_list
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
    global my_champ_name, enemy_champ_name, vs_tip_lb
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


def press_enter(event):
    if my_ent.get("1.0", "end-1c") == "" or enemy_ent.get("1.0", "end-1c") == "":
        return "break"
    search_vs()
    return "break"


#############  func   #############

###############################################################################################################################

# pool = Pool(processes=4) # 4개의 프로세스를 사용합니다.
# pool.map(,) # 함수를 넣어줍시다.

champ_list = []
master_list = []
master_url_list = []
load_cnt = 1

driver = chrome_auto_upgrade.get_driver()
# driver = webdriver.Chrome("chromedriver.exe", options=options)
driver.implicitly_wait(1)  # 로딩 완료되면 1초 기다리기

driver.get("https://www.op.gg/champion/statistics")  # op.gg
driver.execute_script('window.open("about:blank", "_blank");')  # new tab for lol.ps
tabs = driver.window_handles  # <-- 탭 관리
driver.switch_to.window(tabs[0])
croll_all_champ()

#############   GUI   #############

# ,relief='solid',bd=2
root = Tk()
root.title("vsLOL")
root.geometry("1000x700+50+50")
root.resizable(False, False)

vs_frm = Frame(root)  # frame
vs_frm.pack(side="top", pady=20)
Label(vs_frm, text="내 챔피언                                상대 챔피언").pack(anchor="w")
my_ent = Text(vs_frm, width=20, height=1, font=3)
my_ent.bind("<Tab>", focus_next_window)
my_ent.bind("<Return>", press_enter)
my_ent.focus()
my_ent.pack(side="left", fill="both", expand=True)
Label(vs_frm, text="vs").pack(side="left", fill="both", expand=True)
enemy_ent = Text(vs_frm, width=20, height=1, font=3)
enemy_ent.bind("<Tab>", focus_next_window)
enemy_ent.bind("<Shift-Tab>", focus_prev_window)
enemy_ent.bind("<Return>", press_enter)
enemy_ent.pack(side="left", fill="both", expand=True)
Button(vs_frm, text="search", command=search_vs, overrelief="solid").pack(side="bottom")

tip_frm = Frame(root)
tip_frm.pack(side="left", anchor="nw")
Label(tip_frm, text="<상대법>").pack(anchor="w")
tip_scroll = Scrollbar()
vs_tip_lb = Label(
    tip_frm, relief="solid", bd=2, justify="left", width=80, height=15, wraplength=550
)
vs_tip_lb.pack(anchor="w")

mastars_frm = Frame(root, padx=15)
mastars_frm.pack(side="left", anchor="nw")
Label(mastars_frm, text="<장인 리스트>").pack(anchor="w")
master_btns = []
for i in range(0, 5):
    master_btns.append(
        Button(
            mastars_frm,
            text=f"{i+1}. 챔피언을 입력하세요",
            pady=11,
            anchor="w",
            overrelief="solid",
            width=20,
            highlightcolor="grey",
            activebackground="grey",
            disabledforeground="green",
        )
    )
    master_btns[i].pack(anchor="w")

match_frm = Frame(root)
match_frm.pack(side="left", anchor="nw", fill="x")
Button(match_frm, text="전적 더 불러오기", relief="solid", bd=2, command=more_match).pack(
    anchor="e", padx=20
)
match_listbox = Listbox(match_frm, height=14, width=30)
match_listbox.pack(side="left")
scroll = Scrollbar(match_frm, orient="vertical")
# scroll.config(command=listNodes.yview)
scroll.pack(side="left", fill="y")

#############   GUI   #############
root.mainloop()
