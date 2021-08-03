import tkinter as tk

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
import chrome_auto_upgrade
import funcs


'''
셀레니움 비동기 크롤링
result = dirver.execute_async_script(""" 
var done = arguments[0]; 
require(["foo"], function (foo) {
     done(foo.computeSomething());
    });
 """)
'''

###############################################################################################################################


driver = chrome_auto_upgrade.get_driver(
    show=False,  # show: 웹 브라우저를 띄우지 않는 headless chrome 옵션 적용
)
# driver = webdriver.Chrome("chromedriver.exe", options=options)
driver.implicitly_wait(1)  # 로딩 완료되면 1초 기다리기

driver.get("https://www.op.gg/champion/statistics")  # op.gg
driver.execute_script('window.open("about:blank", "_blank");')  # new tab for lol.ps
tabs = driver.window_handles  # <-- 탭 관리
driver.switch_to.window(tabs[0])

champ_list = funcs.croll_all_champ(driver)


# ,relief='solid',bd=2


class VsFrame(tk.Frame):

    my_champ_name, enemy_champ_name = "", ""

    def __init__(self, Parent, *args, **kwargs):
        tk.Frame.__init__(self, Parent, *args, **kwargs)
        self.Parent = Parent

        # self.vs_frm = tk.Frame(Parent)  # frame

        VsFrame.my_ent = tk.Entry(self, width=20, font=3)
        VsFrame.enemy_ent = tk.Entry(self, width=20, font=3)
        # self.vs_frm.pack(side="top", pady=20)
        tk.Label(self, text="내 챔피언                                상대 챔피언").pack(anchor="w")
        VsFrame.my_ent.bind("<Tab>", self.focus_next_window)
        VsFrame.my_ent.bind("<Return>", self.press_enter)
        VsFrame.my_ent.focus()
        # pyautogui.press(["alt", "shift"])  # 한 영
        # VsFrame.my_ent.
        VsFrame.my_ent.pack(side="left", fill="both", expand=True)
        tk.Label(self, text="vs").pack(side="left", fill="both", expand=True)

        VsFrame.enemy_ent.bind("<Tab>", self.focus_next_window)
        VsFrame.enemy_ent.bind("<Shift-Tab>", self.focus_prev_window)
        VsFrame.enemy_ent.bind("<Return>", self.press_enter)
        VsFrame.enemy_ent.pack(side="left", fill="both", expand=True)
        tk.Button(
            self,
            text="search",
            command=lambda: self.search_vs(),
            overrelief="solid",
        ).pack(side="bottom")

    def focus_next_window(self, event):
        event.widget.tk_focusNext().focus()
        return "break"

    def focus_prev_window(self, event):
        event.widget.tk_focusPrev().focus()
        return "break"

    def press_enter(self, event):
        if self.my_ent.get() == "" or self.enemy_ent.get() == "":
            return "break"
        self.search_vs()
        return "break"

    def search_vs(self):
        VsFrame.my_champ_name = self.my_ent.get()
        VsFrame.enemy_champ_name = self.enemy_ent.get()

        if VsFrame.my_champ_name not in champ_list or VsFrame.enemy_champ_name not in champ_list:
            print(f"wrong input!! {VsFrame.my_champ_name},{VsFrame.enemy_champ_name}")
            return None

        TipFrame.get_vs_tip(VsFrame.my_champ_name, VsFrame.enemy_champ_name)
        MasterFrame.get_masters()
        # MasterFrame.change_btn_config()

        return None


class TipFrame(tk.Frame):
    def __init__(self, Parent, *args, **kwargs):
        tk.Frame.__init__(self, Parent, *args, **kwargs)
        self.Parent = Parent

        # self.tip_frm = tk.Frame(Parent)
        TipFrame.tip_txt = tk.StringVar()

        TipFrame.vs_tip_lb = tk.Label(
            self,
            relief="solid",
            bd=2,
            justify="left",
            width=80,
            height=15,
            wraplength=550,
            textvariable=TipFrame.tip_txt,
        )

        tk.Label(self, text="<상대법>").pack(anchor="w")
        TipFrame.vs_tip_lb.pack(side="left", anchor="nw")

        TipFrame.scroll = tk.Scrollbar(self, orient="vertical")
        TipFrame.scroll.pack(side="left", fill="y")

    def get_vs_tip(my_champ_name, enemy_champ_name):  # called by vs
        psURL = f"https://lol.ps/versus/?champ1={my_champ_name}&champ2={enemy_champ_name}"  # need vs!!!!!!!!!!
        driver.switch_to.window(tabs[1])  # lol.ps 탭으로 이동
        driver.get(psURL)

        txt = driver.find_element_by_class_name("guide-text").text  # 상대법 크롤링
        TipFrame.tip_txt.set(txt)

        # self.vs_tip_lb.configure(textvariable=TipFrame.tip_txt)


class MasterFrame(tk.Frame):
    master_idx = -1

    def __init__(self, Parent, *args, **kwargs):
        tk.Frame.__init__(self, Parent, *args, **kwargs)
        self.Parent = Parent

        MasterFrame.master = [  # 버튼 5개에 이름과 주소 정보 들어감
            {"idx": i, "btn": None, "name": tk.StringVar(), "url": tk.StringVar()} for i in range(5)
        ]

        tk.Label(self, text="<장인 리스트>").pack(anchor="w")
        # MasterFrame.set_btn(["챔피언을 입력하세요"*5],[""*5])
        for i in range(0, 5):  # 버튼 5개 초기화
            MasterFrame.master[i]["btn"] = tk.Button(
                self,
                textvariable=MasterFrame.master[i]["name"],
                pady=11,
                anchor="w",
                overrelief="solid",
                width=20,
                highlightcolor="grey",
                activebackground="grey",
                disabledforeground="green",
            )
            MasterFrame.master[i]["btn"].bind("<Button-1>", self.click_master)
            MasterFrame.master[i]["btn"].pack(anchor="w")

    def set_btn(name_list, url_list):
        for i in range(0, 5):
            MasterFrame.master[i]["btn"].configure(bg="SystemButtonFace", state="normal")
            MasterFrame.master[i]["name"].set(
                str(MasterFrame.master[i]["idx"] + 1) + "." + name_list[i]
            )
            MasterFrame.master[i]["url"].set(url_list[i])

    def get_masters():  # called by vs
        driver.switch_to.window(tabs[0])  # op.gg 탭으로 이동
        opggURL = f"https://www.op.gg/champion/{VsFrame.my_champ_name}/statistics"  # need vs!!!
        driver.get(opggURL)
        croll_masters = driver.find_elements_by_class_name(
            "champion-stats-summary-ranking__table__summoner"
        )

        name_list = []
        url_list = []
        for master in croll_masters:
            name_list.append(master.text)
            master_url = master.find_element_by_tag_name("a").get_attribute("href")
            url_list.append(master_url)

        MasterFrame.set_btn(name_list, url_list)

    def click_master(self, event):
        btn = event.widget
        if btn["state"] == "disabled":
            return None

        for i in range(0, 5):  # 기존에 눌렸던 버튼 풀어줌
            MasterFrame.master[i]["btn"].configure(bg="SystemButtonFace", state="normal")

        btn.configure(state="disabled")

        MasterFrame.master_idx = int(btn["text"][0]) - 1
        driver.get(MasterFrame.master[MasterFrame.master_idx]["url"].get())
        champ_match = driver.find_element_by_class_name("ChampionMatchSearchWrap")
        champ_match.find_element_by_class_name("Input").send_keys(VsFrame.my_champ_name)
        champ_match.find_element_by_class_name("Item.show").click()  # 클래스에 띄어쓰기 있으면 . 붙이자

        # 전적 한번에 20개씩 뜸
        MatchupFrame.find_matchup(MasterFrame.master[MasterFrame.master_idx]["name"].get())

        return "break"


class MatchupFrame(tk.Frame):
    load_cnt = 0
    Matchups = WebElement()

    def __init__(self, Parent, *args, **kwargs):
        tk.Frame.__init__(self, Parent, *args, **kwargs)
        self.Parent = Parent

        MatchupFrame.match_listbox = tk.Listbox(self, height=14, width=40)
        MatchupFrame.scroll = tk.Scrollbar(self, orient="vertical")

        tk.Button(
            self,
            text="전적 더 불러오기",
            relief="solid",
            bd=2,
            # command=lambda: more_match,
        ).pack(anchor="e", padx=20)
        MatchupFrame.match_listbox.pack(side="left")
        MatchupFrame.scroll.pack(side="left", fill="y")

    def find_matchup(master_name):
        if master_name != MasterFrame.master[MasterFrame.master_idx]["name"]:
            MatchupFrame.load_cnt = 0  # 새 장인 선택됐으니 전에 로드된거 초기화
            MatchupFrame.Matchups.clear()

        MatchupFrame.Matchups = driver.find_element_by_class_name("GameItemList")

        # print(type(GameItemList))
        """
        //*[@id="SummonerLayoutContent"]/div[2]/div[2]/div/div[2]/div[2]    

        //*[@id="SummonerLayoutContent"]/div[2]/div[2]/div/div[2]/div[3]
        //*[@id="SummonerLayoutContent"]/div[2]/div[2]/div/div[2]/div[4]
        """

        for k in range(MatchupFrame.load_cnt, MatchupFrame.load_cnt + 20):
            # Teams = match.find_elements_by_class_name('Team')

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
            if vs_champ == VsFrame.enemy_champ_name:
                MatchupFrame.match_listbox.insert()

            else:
                continue

            """
            //*[@id="SummonerLayoutContent"]/div[2]/div[2]/div/div[2]/div[3]/div[1]
            //*[@id="SummonerLayoutContent"]/div[2]/div[2]/div/div[2]/div[3]/div[2]
            //*[@id="SummonerLayoutContent"]/div[2]/div[2]/div/div[2]/div[3]/div[3]




            """


class RuneFrame(tk.Frame):
    def __init__(self, Parent, *args, **kwargs):
        tk.Frame.__init__(self, Parent, *args, **kwargs)
        self.Parent = Parent


class ItemFrame(tk.Frame):
    def __init__(self, Parent, *args, **kwargs):
        tk.Frame.__init__(self, Parent, *args, **kwargs)
        self.Parent = Parent


class SkillFrame(tk.Frame):
    def __init__(self, Parent, *args, **kwargs):
        tk.Frame.__init__(self, Parent, *args, **kwargs)
        self.Parent = Parent


########### Class ####################################################################################################################################################


class MainApplication(tk.Frame):
    load_cnt = 0
    master_list = []
    master_url_list = []

    def __init__(self, Parent, *args, **kwargs):
        tk.Frame.__init__(self, Parent, *args, **kwargs)
        self.Parent = Parent

        # GUI
        vs = VsFrame(self)
        tip = TipFrame(self)
        master = MasterFrame(self)
        matchtup = MatchupFrame(self)

        vs.pack(pady=20)
        tip.pack(side="left", anchor="nw", padx=20)
        master.pack(side="left", anchor="nw")
        matchtup.pack(side="left", anchor="nw")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("vsLOL")
    root.geometry("1080x720+400+50")
    root.resizable(False, False)
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
