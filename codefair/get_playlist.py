from bs4 import BeautifulSoup

# HTML 파일 경로
html_file = 'takeout_data/YouTube/watch-history.html'

# HTML 파일 읽기
with open(html_file, 'r', encoding='utf-8') as file:
    soup = BeautifulSoup(file, 'lxml')

# 시청 기록 추출
videos = soup.find_all('div', class_='content')

# 시청 기록 출력
for video in videos:
    title = video.find('h3').text
    url = video.find('a')['href']
    date = video.find('span', class_='date').text
    print(f'제목: {title}\nURL: {url}\n날짜: {date}\n')
