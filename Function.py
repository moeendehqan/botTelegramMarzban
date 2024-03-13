from pymongo import MongoClient
import requests
import json
import datetime
from persiantools.jdatetime import JalaliDate
client = MongoClient()

db = client['bot']

def bits_to_gigabytes(bits):
    bytes = bits * 9.3132257461548E-10

    return round(bytes,2)

def Message2db(messageJson):
    db['message'].insert_one(messageJson)


def UserGetUsage(sub):
    response = requests.get(f'http://185.239.0.149:8000/sub/{sub}/info')
    if response.status_code != 200:
        return False
    dic = json.loads(response.content)
    del dic['proxies']
    del dic['inbounds']
    del dic['links']
    del dic['excluded_inbounds']
    dic['expire_jalali'] = str(JalaliDate.fromtimestamp(int(dic['expire'])))
    dic['expire_last_day'] = (datetime.datetime.fromtimestamp(int(dic['expire'])) - datetime.datetime.now()).days
    dic['data_limit_gig'] = bits_to_gigabytes(int(dic['data_limit']))
    dic['used_traffic_gig'] = bits_to_gigabytes(int(dic['used_traffic']))
    dic['used_traffic_rate'] = round((int(dic['used_traffic']) / int(dic['data_limit'])) * 100,1)
    try:
        dic['sub_updated_at_last_day'] = (datetime.datetime.now() - datetime.datetime.fromisoformat(dic['sub_updated_at'])).days
    except:
        dic['sub_updated_at_last_day'] = " - "
    return dic

UserGetUsage('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJVc2VyQXNHNzkwIiwiYWNjZXNzIjoic3Vic2NyaXB0aW9uIiwiaWF0IjoxNzEwMzU4NTcyfQ.I4yWQILNEJwIYubd6d-NU96Tb5uEwwSzcVEQH5r020Q')