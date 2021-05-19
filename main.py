from bs4 import BeautifulSoup
from selenium import webdriver


champ_name = input("챔피언 이름: ") # wrong input 처리
opggURL = f'https://www.op.gg/champion/{champ_name}/statistics'

options = webdriver.ChromeOptions()
options.add_argument('headless')    # 웹 브라우저를 띄우지 않는 headless chrome 옵션 적용
options.add_argument('disable-gpu')    # GPU 사용 안함
options.add_argument('lang=ko_KR')    # 언어 설정
options.add_experimental_option("excludeSwitches", ["enable-logging"]) #로그 안뜨게

driver = webdriver.Chrome('chromedriver.exe', options=options)
driver.implicitly_wait(1) # 로딩 완료되면 1초 기다리기
driver.get(opggURL)


while(driver.current_url == 'https://www.op.gg/champion/statistics'): #챔 이름 잘못침
    print("wrong input!!!")
    champ_name = input("챔피언 이름: ")
    opggURL = f'https://www.op.gg/champion/{champ_name}/statistics'
    driver.get(opggURL)



croll_masters = driver.find_elements_by_class_name("champion-stats-summary-ranking__table__summoner")
#print(croll_masters)

master_list = []
for master in croll_masters:
    master_url = master.find_element_by_tag_name('a').get_attribute('href')
    master_list.append([master.text,master_url])


print("<장인 리스트>")
for i in range(0,len(master_list)):
    print(f"#{i+1}.{master_list[i][0]}")

pick_master = int(input("장인을 고르세요: #"))
while(pick_master not in range(0,5)):
    print("Wrong input!!!")
    pick_master = int(input("장인을 고르세요: #"))
driver.get(master_list[pick_master-1][1])

enemy = input("상대 챔피언 이름: ")
psURL=f"https://lol.ps/versus/?champ1={champ_name}&champ2={enemy}"

driver.execute_script('window.open("about:blank", "_blank");')
tabs = driver.window_handles # <-- 탭 관리

driver.switch_to.window(tabs[1]) #lol.ps 탭으로 이동
driver.get(psURL)

vstip = driver.find_element_by_class_name("guide-text") #상대법 크롤링
print(vstip.text)
driver.close()


driver.quit()




