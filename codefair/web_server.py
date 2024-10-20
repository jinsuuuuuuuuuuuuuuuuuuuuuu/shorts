from flask import Flask, jsonify
import json
from datetime import datetime, timedelta
from collections import defaultdict, Counter
# import requests
import aiohttp
import asyncio
import pytz 



#정리용
from collections import defaultdict
from datetime import datetime

def merge_datewise_data(dict1, dict2, dict3):
    # 결과를 저장할 딕셔너리
    merged_data = {}
    
    # 모든 날짜를 가져오기 위해 세 딕셔너리의 키를 합칩니다
    all_dates = set(dict1.keys()).union(set(dict2.keys())).union(set(dict3.keys()))
    
    # 각 날짜별로 리스트로 값을 합칩니다
    for date in all_dates:
        value1 = dict1.get(date, 0)
        value2 = dict2.get(date, 0)
        value3 = dict3.get(date, 0)
        merged_data[date] = [value1, value2, value3]
    
    return merged_data




from collections import defaultdict
from datetime import datetime

def group_watch_times_by_date(data):
    # 날짜별 시청 시간을 저장할 딕셔너리
    watch_times_by_date = defaultdict(list)
    
    # 총 시청 시간을 저장할 딕셔너리
    total_time_by_date = defaultdict(int)  

    for entry in data:
        time_str = entry['time']
        dt = datetime.fromisoformat(time_str)  # ISO 8601 형식 문자열을 datetime 객체로 변환
        date_key = dt.date().isoformat()  # 날짜 부분만 ISO 형식으로 추출
        
        # 해당 날짜의 시간과 분 저장
        hour, minute = dt.hour, dt.minute
        watch_times_by_date[date_key].append((hour, minute))  # (시간, 분) 튜플로 저장

    # 날짜별로 시청 시간을 처리
    for date, times in watch_times_by_date.items():
        # 비교를 위해 시간을 오름차순으로 정렬
        times.sort()
        
        # 시청 시간을 총 분으로 변환
        total_minutes = [(h * 60 + m) for h, m in times]

        # 인접한 시청 시간을 비교
        count_list = []  # 연속된 시청 시간을 저장할 임시 리스트

        for i in range(len(total_minutes) - 1):
            current_time = total_minutes[i]
            next_time = total_minutes[i + 1]

            # 다음 시청 시간이 현재 시청 시간에서 3분 이내인지 확인
            if next_time - current_time <= 3:
                count_list.append(current_time)
            else:
                # 3분 이내의 연속된 시청 시간이 있는 경우 총 시간을 계산
                if count_list:
                    count_list.append(current_time)
                    total_time_by_date[date] += count_list[-1] - count_list[0]
                    count_list.clear()  # 다음 시청 시간 그룹을 위해 리스트 초기화

        # 마지막 시청 시간 그룹 처리
        if count_list:
            total_time_by_date[date] += count_list[-1] - count_list[0]
            count_list.clear()

    # 디버깅 출력 (옵션)
    # print(total_time_by_date)  # 최종 시청 시간 데이터 출력

    return dict(total_time_by_date)  # 딕셔너리 형태로 반환






def date_group_count(json:dict): 
    date_counts = Counter()
    for activity in json:
        time_str = activity['time']
        date_str = datetime.fromisoformat(time_str[:-1]).date().isoformat()  # Remove 'Z' and convert to date
        date_counts[date_str] += 1

    # Print the counts
    # print(date_counts)

    return dict(date_counts)




#시간 많이 그ㅓㄱ
def most_viewed_times(jsons:dict):
    # 한국 시간대 설정
    kst = pytz.timezone('Asia/Seoul')

    # 날짜별 시청 시간을 저장할 딕셔너리입니다.
    date_hours = defaultdict(list)

    # 데이터를 처리하여 날짜와 시를 추출합니다.
    for entry in jsons:
        time_str = entry['time']
        # ISO 8601 형식의 시간 문자열을 datetime 객체로 변환
        dt = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
        # 한국 시간대 적용
        dt = dt.astimezone(kst)
        date_key = dt.date().isoformat()
        hour = dt.hour
        date_hours[date_key].append(hour)

    # 날짜별로 시의 최빈값을 계산합니다.
    date_most_common_hours = {}

    for date, hours in date_hours.items():
        count_hours = Counter(hours)
        most_common_hour = count_hours.most_common(1)[0][0]
        date_most_common_hours[date] = most_common_hour
    
    print(date_most_common_hours)

    return date_most_common_hours
    

#숏츠 분류
async def is_short(vid: str) -> bool:
    url = f'https://www.youtube.com/shorts/{vid}'
    async with aiohttp.ClientSession() as session:
        try:
            async with session.head(url) as response:
                return response.status == 200
        except Exception as e:
            # print(f'Error: {e}')
            return False
   
def get_video_code(data:dict):
    txt = data['titleUrl'].split("/")[3][8:]
    # print(txt)
    return txt

def Recently_Viewed_Data(data: dict, days=7):
    today = datetime.utcnow().date()
    one_week_ago = today - timedelta(days=days)  # 7일 전 날짜 계산

    # 오늘을 제외하고 7일 전부터 어제까지의 활동만 포함
    filtered_data = []
    for activity in data:
        time_str = activity['time']
        activity_date = datetime.fromisoformat(time_str[:-1]).date()  # 'Z' 제거 후 날짜로 변환
        
        # 7일 전부터 어제까지의 활동만 포함
        if one_week_ago <= activity_date < today:
            filtered_data.append(activity)

    return filtered_data

def check_titleURL(jsons: dict):
    # 'titleUrl' 키가 있는 항목들을 반환
    return [item for item in jsons if 'titleUrl' in item]





app = Flask(__name__)

@app.route('/')
def get_playlists():
    today = datetime.utcnow().date()
    # JSON 파일에서 데이터 읽기
    with open('시청기록.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        filter_data = check_titleURL(Recently_Viewed_Data(data))
        
        shorts_json=[i for i in filter_data if is_short(get_video_code(i))] 
        # date_group_count(shorts_json)
        # group_watch_times_by_date(shorts_json)
    # print(shorts_json)
    result = merge_datewise_data(date_group_count(shorts_json), most_viewed_times(shorts_json), group_watch_times_by_date(shorts_json))
    del result[today.strftime(f'%Y-%m-%d')]
    return jsonify(result)


if __name__ == '__main__':
    app.run(host="172.30.1.88",debug=True)

