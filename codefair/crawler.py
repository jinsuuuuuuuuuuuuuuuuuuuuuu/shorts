import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import requests
import zipfile
import os

# ChromeDriver 자동 설치
driver_path = chromedriver_autoinstaller.install()

# Selenium 웹 드라이버 설정
chrome_options = Options()
# chrome_options.add_argument("--headless")  # 백그라운드에서 실행 (선택 사항)

# ChromeDriver 경로 자동 설정
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Google 로그인 페이지로 이동
    driver.get('https://accounts.google.com/signin/v2/identifier')

    # 로그인 과정 (여기서는 사용자의 개입이 필요할 수 있습니다)
    # 예시: ID 입력
    email_field = driver.find_element(By.ID, 'identifierId')
    email_field.send_keys('jgk200801@gmail.com')
    email_field.send_keys(Keys.RETURN)

    # 잠시 대기
    time.sleep(3)

    # 예시: 비밀번호 입력
    password_field = driver.find_element(By.NAME, 'password')
    password_field.send_keys('j94410978!')
    password_field.send_keys(Keys.RETURN)

    # 로그인 완료 후, Google Takeout 페이지로 이동
    driver.get('https://takeout.google.com/')

    # Takeout 페이지 로드 대기
    time.sleep(10)  # 이 시간을 적절히 조정해야 할 수 있습니다.

    # Google Takeout에서 내보내기 요청 진행 (여기서도 수동 설정이 필요할 수 있습니다)
    # 예시: '모두 선택' 클릭
    select_all_button = driver.find_element(By.XPATH, '//button[contains(text(), "모두 선택")]')
    select_all_button.click()

    # 예시: 내보내기 진행 클릭
    export_button = driver.find_element(By.XPATH, '//button[contains(text(), "내보내기 시작")]')
    export_button.click()

    # 다운로드 페이지로 이동하여 다운로드 링크를 찾습니다.
    time.sleep(10)  # 내보내기 요청이 처리되는 동안 대기합니다.

    # 다운로드 링크 확인
    download_link = driver.find_element(By.XPATH, '//a[contains(@href, "takeout-download-link")]')
    download_url = download_link.get_attribute('href')

    # 다운로드
    response = requests.get(download_url)
    with open('takeout.zip', 'wb') as file:
        file.write(response.content)

    # 다운로드된 파일의 압축 해제
    with zipfile.ZipFile('takeout.zip', 'r') as zip_ref:
        zip_ref.extractall('takeout_data')

    print("파일 다운로드 및 압축 해제 완료.")

finally:
    # 드라이버 종료
    driver.quit()
