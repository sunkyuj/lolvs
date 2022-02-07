import tkinter as tk
import chrome_auto_upgrade
from funcs import croll_all_champ, focus_next_window, focus_prev_window
from PIL import Image

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# from selenium.webdriver.support.relative_locator import with_tag_name

'''
셀레니움 비동기 크롤링
result = dirver.execute_async_script(""" 
var done = arguments[0]; 
require(["foo"], function (foo) {
     done(foo.computeSomething());
    });
 """)
'''

"""
def datetime_decorator(func):
    def decorated():
        animation(count)
        func()
        stop_animation()
        
    return decorated
"""

###############################################################################################################################


driver = chrome_auto_upgrade.get_driver(
    show_browser=0,  # show: 웹 브라우저를 띄우지 않는 headless chrome 옵션 적용
)
# driver = webdriver.Chrome("chromedriver.exe", options=options)
# driver.implicitly_wait(1)  # 로딩 완료되면 1초 기다리기

driver.get("https://www.op.gg/champion/statistics")  # op.gg
driver.execute_script('window.open("about:blank", "_blank");')  # new tab for lol.ps
tabs = driver.window_handles  # <-- 탭 관리
driver.switch_to.window(tabs[0])


champ_list = croll_all_champ(driver)


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
        VsFrame.my_ent.bind("<Tab>", focus_next_window)
        VsFrame.my_ent.bind("<Return>", self.press_enter)
        VsFrame.my_ent.focus()
        # pyautogui.press(["alt", "shift"])  # 한 영
        # VsFrame.my_ent.
        VsFrame.my_ent.pack(side="left", fill="both", expand=True)
        tk.Label(self, text="vs").pack(side="left", fill="both", expand=True)

        VsFrame.enemy_ent.bind("<Tab>", focus_next_window)
        VsFrame.enemy_ent.bind("<Shift-Tab>", focus_prev_window)
        VsFrame.enemy_ent.bind("<Return>", self.press_enter)
        VsFrame.enemy_ent.pack(side="left", fill="both", expand=True)
        tk.Button(
            self,
            text="search",
            command=lambda: self.search_vs(),
            overrelief="solid",
        ).pack(side="bottom")

    """
    def focus_next_window(self, event):
        event.widget.tk_focusNext().focus()
        return "break"

    def focus_prev_window(self, event):
        event.widget.tk_focusPrev().focus()
        return "break"
    """

    def press_enter(self, event):
        if event.widget == VsFrame.my_ent and self.enemy_ent.get() == "":
            return focus_next_window(event)
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
            width=60,
            height=14,
            wraplength=400,
            textvariable=TipFrame.tip_txt,
            pady=10,
            bg="lightgrey",
        )

        tk.Label(self, text="<상대법>").pack(anchor="w")
        TipFrame.vs_tip_lb.pack(side="left", anchor="nw")

        TipFrame.scroll = tk.Scrollbar(self, orient="vertical")
        TipFrame.scroll.pack(side="left", fill="y")

    def get_vs_tip(my_champ_name, enemy_champ_name):  # called by vs
        psURL = f"https://lol.ps/versus/?champ1={my_champ_name}&champ2={enemy_champ_name}"  # need vs!!!!!!!!!!
        driver.switch_to.window(tabs[1])  # lol.ps 탭으로 이동
        driver.get(psURL)

        txt = driver.find_element_by_css_selector(
            "body > main > div.contents > div.versus-text > div"
        ).text  # 상대법 크롤링
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

        croll_masters = driver.find_element_by_css_selector(
            "body > div.l-wrap.l-wrap--champion > div.l-container > div > div.tabWrap._recognized > div.l-champion-statistics-content.tabItems > div.tabItem.Content.championLayout-overview > div > div.l-champion-statistics-content__side > div.champion-box.champion-stats-player-ranking > div.champion-box-content > table"
        ).find_elements_by_tag_name("a")

        name_list = []
        url_list = []
        for master in croll_masters:
            name_list.append(master.text)
            master_url = master.get_attribute("href")
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

        champ_match = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "#SummonerLayoutContent > div.tabItem.Content.SummonerLayoutContent.summonerLayout-summary > div.RealContent > div > div.Header.Box > div > div > div > div",
                )
            )
        )

        """champ_match = driver.find_element_by_css_selector(
            "#SummonerLayoutContent > div.tabItem.Content.SummonerLayoutContent.summonerLayout-summary > div.RealContent > div > div.Header.Box > div > div > div > div"
        )"""
        champ_match.find_element_by_class_name("Input").send_keys(VsFrame.my_champ_name)
        champ_match.find_element_by_class_name("Item.show").click()  # 클래스에 띄어쓰기 있으면 . 붙이자

        MatchupFrame.matchup_ListBox_clear()
        MatchupFrame.find_matchup(MasterFrame.master[MasterFrame.master_idx]["name"].get())

        return "break"


class MatchupFrame(tk.Frame):
    load_cnt = 0
    match20_list = []

    def __init__(self, Parent, *args, **kwargs):
        tk.Frame.__init__(self, Parent, *args, **kwargs)
        self.Parent = Parent

        MatchupFrame.match_listbox = tk.Listbox(self, height=14, width=60)
        MatchupFrame.scroll = tk.Scrollbar(self, orient="vertical")

        tk.Button(
            self,
            text="전적 더 불러오기",
            # relief="solid",
            overrelief="solid",
            state="normal",
            command=self.more_match,
        ).pack(anchor="e", padx=20)
        MatchupFrame.match_listbox.pack(side="left")
        MatchupFrame.scroll.pack(side="left", fill="y")

    def find_matchup(master_name):

        # 전부 크롤링하되 20개씩만 처리

        match20 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    f"#SummonerLayoutContent > div.tabItem.Content.SummonerLayoutContent.summonerLayout-summary > div.RealContent > div > div.Content > div:nth-child({MatchupFrame.load_cnt*2+5})",
                )
            )
        )

        matches_with_enemy = MatchupFrame.vs_enemy(match20)  # 20개 분석(상대챔이랑 뜨는거 몇개 있는지..)
        MatchupFrame.add_at_listbox(matches_with_enemy)  # 분석한것들 리스트박스에 추가

    def vs_enemy(match20):
        matches_with_enemy = []
        matches = match20.find_elements_by_class_name("GameItemWrap")
        for match in matches:
            if MatchupFrame.right_enemy(match):
                matches_with_enemy.append(match)

        return matches_with_enemy

    def right_enemy(match):
        enemy_idx = -1
        summoners = match.find_elements_by_class_name("Summoner")

        master_name = MasterFrame.master[MasterFrame.master_idx]["name"].get().split(".")[1]

        for i, s in enumerate(summoners):
            # s.text.split("\n")[0] == 챔피언 이름
            # s.text.split("\n")[1] == 닉네임

            if s.text.split("\n")[1] == master_name:
                enemy_idx = (i + 5) % 5
                break
        return summoners[enemy_idx].text.split("\n")[0] == VsFrame.enemy_champ_name

    def add_at_listbox(matches_with_enemy):
        # print(matches_with_enemy)
        for match in matches_with_enemy:
            info = match.text.split("\n")
            print(info)
            time_ago = info[1]
            match_result = info[2]
            kda = info[5]
            # idx 13 부터 챔 닉...
            bg_color = "lightblue"
            MatchupFrame.match_listbox.insert("end", time_ago + "   " + kda)
            if match_result == "패배":
                bg_color = "pink"
            MatchupFrame.match_listbox.itemconfig("end", {"bg": bg_color})

    def matchup_ListBox_clear():
        MatchupFrame.load_cnt = 0
        MatchupFrame.match20_list.clear()
        MatchupFrame.match_listbox.delete("0", "end")

    def more_match(self):
        if MasterFrame.master_idx == -1:
            return None
        driver.find_element_by_link_text("더 보기").click()
        MatchupFrame.load_cnt += 1
        MatchupFrame.find_matchup(MasterFrame.master[MasterFrame.master_idx]["name"].get())


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
        root.wm_attributes("-topmost", 0)


if __name__ == "__main__":
    root = tk.Tk()
    root.wm_attributes("-topmost", 1)
    root.title("vsLOL")
    root.geometry("1080x720+400+50")
    root.resizable(False, False)

    loading_img = "loading.gif"
    info = Image.open(loading_img)
    frames = info.n_frames
    print(frames)
    im = [tk.PhotoImage(file=loading_img, format=f"gif -index {i}") for i in range(frames)]

    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
