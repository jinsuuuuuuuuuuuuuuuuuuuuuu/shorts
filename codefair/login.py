from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pickle  # 쿠키를 저장하고 로드하기 위해 사용

# ChromeDriver 자동 설치
import chromedriver_autoinstaller
chromedriver_autoinstaller.install()

# ChromeDriver 경로 자동 설정
driver_path = chromedriver_autoinstaller.install()
service = Service(driver_path)
chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--headless")  # 백그라운드에서 실행 (선택 사항)
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # 구글 로그인 페이지로 이동
    driver.get('https://accounts.google.com/signin/v2/identifier')

    # 로그인 과정 (여기서는 사용자의 개입이 필요할 수 있습니다)
    # 예시: ID 입력
    email_field = driver.find_element(By.ID, 'identifierId')
    email_field.send_keys('jsu200801@gmail.com')
    email_field.send_keys(Keys.RETURN)

    # 잠시 대기
    time.sleep(10)

    # 예시: 비밀번호 입력
    password_field = driver.find_element(By.NAME, 'password')
    password_field.send_keys('j94410978!')
    password_field.send_keys(Keys.RETURN)

    # 로그인 완료까지 대기
    time.sleep(10)  # 로그인 완료까지 충분히 대기

    # 로그인 후 쿠키 저장
    with open('cookies.pkl', 'wb') as file:
        pickle.dump(driver.get_cookies(), file)

    print("쿠키 저장 완료.")

finally:
    # 드라이버 종료
    driver.quit()
