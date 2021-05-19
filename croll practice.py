from bs4 import BeautifulSoup
from selenium import webdriver

URL = 'https://www.op.gg/champion/statistics'
options = webdriver.ChromeOptions()
options.add_argument('headless')    # 웹 브라우저를 띄우지 않는 headless chrome 옵션 적용
options.add_argument('disable-gpu')    # GPU 사용 안함
options.add_argument('lang=ko_KR')    # 언어 설정
driver = webdriver.Chrome('chromedriver.exe', options=options)
driver.get(URL)

champs=driver.find_elements_by_class_name("champion-index__champion-item")

k=[]
e=[]

for champ in champs:
    k_name = champ.get_attribute("data-champion-name")
    e_name = champ.get_attribute("data-champion-key")
    #print(k_name,e_name)
    k.append(k_name)
    e.append(e_name)
    
print(k)
print(e)

driver.quit()