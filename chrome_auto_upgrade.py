from selenium import webdriver
import chromedriver_autoinstaller


def get_driver(show=False):
    options = webdriver.ChromeOptions()
    if not show:
        options.add_argument("headless")  # 웹 브라우저를 띄우지 않는 headless chrome 옵션 적용
    options.add_argument("disable-gpu")  # GPU 사용 안함
    options.add_argument("lang=ko_KR")  # 언어 설정
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])  # 로그 안뜨게
    # 크롬드라이버 버전 확인
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split(".")[0]

    try:
        return webdriver.Chrome(f"./{chrome_ver}/chromedriver.exe", options=options)
    except:
        chromedriver_autoinstaller.install(True)
        return webdriver.Chrome(f"./{chrome_ver}/chromedriver.exe", options=options)
