#!/usr/bin/env python
"""
Weather data is provided by https://www.seniverse.com/,
below code are modified from https://github.com/seniverse/seniverse-api-demos

NOTE: user need provide shell environment `SENIVERSE_KEY` and `SENIVERSE_UID`\
 to using this API
"""
import os
import ipdb
import requests
import json
import pendulum

# KEY = os.getenv('SENIVERSE_KEY', '')  # API key
KEY = 'S9yZlXhp_aZZrVjnl'
UID = ""  # 用户ID, TODO: 当前并没有使用这个值,签名验证方式将使用到这个值

LOCATION = 'beijing'  # 所查询的位置，可以使用城市拼音、v3 ID、经纬度等
API = 'https://api.seniverse.com/v3/weather/daily.json'  # API URL，可替换为其他 URL
UNIT = 'c'  # 单位
LANGUAGE = 'zh-Hans'  # 查询结果的返回语言


def compute_relative_data(data_context):
    pass

def fetch_weather(location, start=0, days=15):
    result = requests.get(API, params={
        'key': KEY,
        'location': location,
        'language': LANGUAGE,
        'unit': UNIT,
        'start': start,
        'days': days
    }, timeout=2)
    return result.json()


def get_weather_by_day(location, day=1):
    if day >= 0:
        result = fetch_weather(location)
        normal_result = {
            "location": result["results"][0]["location"],
            "result": result["results"][0]["daily"][day]
        }
    else:
        result = fetch_weather(location)
        normal_result = {
            "location": result["results"][0]["location"],
            "result": result["results"][0]["daily"][abs(day)]
        }
        test_date = normal_result['result']['date']
        year, mouth, day_str = test_date.split('-')
        transformed_day = int(day_str) + day + day
        update_test_date = year + '-' + mouth + '-' + str(transformed_day) 
        normal_result['result']['date'] = update_test_date
    return normal_result


if __name__ == '__main__':
    default_location = "合肥"
    result = fetch_weather(default_location)
    print(json.dumps(result, ensure_ascii=False))

    default_location = "合肥"
    result = get_weather_by_day(default_location)
    print(json.dumps(result, ensure_ascii=False))
