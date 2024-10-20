import json
with open('시청기록.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
    shorts_strings = [s for s in data if '/shorts' in s['title']]
    print(shorts_strings[0]['title'])