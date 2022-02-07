from selenium import webdriver
import chromedriver_autoinstaller


def get_driver(show_browser=False):
    options = webdriver.ChromeOptions()
    if not show_browser:
        options.add_argument("headless")  # 웹 브라우저를 띄우지 않는 headless chrome 옵션 적용
    options.add_argument("disable-gpu")  # GPU 사용 안함
    options.add_argument("lang=ko_KR")  # 언어 설정
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])  # 로그 안뜨게
    # options.page_load_strategy = "none"

    # 크롬드라이버 버전 확인
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split(".")[0]

    # 속도 향상을 위한 옵션 해제
    prefs = {
        "profile.default_content_setting_values": {
            "cookies": 2,
            "images": 2,
            "plugins": 2,
            "popups": 2,
            "geolocation": 2,
            "notifications": 2,
            "auto_select_certificate": 2,
            "fullscreen": 2,
            "mouselock": 2,
            "mixed_script": 2,
            "media_stream": 2,
            "media_stream_mic": 2,
            "media_stream_camera": 2,
            "protocol_handlers": 2,
            "ppapi_broker": 2,
            "automatic_downloads": 2,
            "midi_sysex": 2,
            "push_messaging": 2,
            "ssl_cert_decisions": 2,
            "metro_switch_to_desktop": 2,
            "protected_media_identifier": 2,
            "app_banner": 2,
            "site_engagement": 2,
            "durable_storage": 2,
        }
    }
    options.add_experimental_option("prefs", prefs)

    try:
        return webdriver.Chrome(f"./{chrome_ver}/chromedriver.exe", options=options)
    except:
        chromedriver_autoinstaller.install(True)
        return webdriver.Chrome(f"./{chrome_ver}/chromedriver.exe", options=options)
