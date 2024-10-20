from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pickle  # 쿠키를 저장하고 로드하기 위해 사용
import chromedriver_autoinstaller

# ChromeDriver 자동 설치
chromedriver_autoinstaller.install()

# ChromeDriver 경로 자동 설정
driver_path = chromedriver_autoinstaller.install()
service = Service(driver_path)
chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless")  # 백그라운드에서 실행 (선택 사항)
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Google Takeout 페이지로 이동
    driver.get('https://takeout.google.com/')

    # 쿠키 로드
    with open('cookies.pkl', 'rb') as file:
        cookies = pickle.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)

    # 페이지 새로고침
    driver.refresh()

    # Google Takeout 작업 진행
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
    import requests
    response = requests.get(download_url)
    with open('takeout.zip', 'wb') as file:
        file.write(response.content)

    print("파일 다운로드 완료.")

finally:
    # 드라이버 종료
    driver.quit()
