from pymongo import MongoClient
import requests
import json
import datetime
from persiantools.jdatetime import JalaliDate
client = MongoClient()

db = client['bot']

def Token():
    token = requests.post('http://185.239.0.149:8000/api/admin/token',data={'username':'moeen', 'password':'Moeen....6168'})
    token = json.loads(token.content)
    print(token)
    token = token['access_token']
    return token

def bits_to_gigabytes(bits):
    bytes = bits * 9.3132257461548E-10

    return round(bytes,2)

def Message2db(messageJson):
    #db['message'].insert_one(messageJson)
    pass


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
    dic['timing'] = (datetime.datetime.fromtimestamp(int(dic['expire'])) - datetime.datetime.strptime(dic['created_at'],"%Y-%m-%dT%H:%M:%S.%f")).days
    try:
        dic['sub_updated_at_last_day'] = (datetime.datetime.now() - datetime.datetime.fromisoformat(dic['sub_updated_at'])).days
    except:
        dic['sub_updated_at_last_day'] = " - "
    return dic

def GetPrice(gig,date):
    GigP = 1000
    DateP = 1800
    dic = {
        30:{
            20 : 60000,
            30 : 75000,
            50 : 95000,
            80 : 135000,
            130 : 195000,
            },
        60:{
            20 : 95000,
            30 : 110000,
            50 : 135000,
            80 : 170000,
            130 : 230000,
        },
        90:{
            20 : 135000,
            30 : 145000,
            50 : 170000,
            80 : 205000,
            130 : 270000,
        },
    }
    try:
        price = dic[date][gig]
        return price
    except:
        try:
            date = int(int(date)/30)*30
            gig = int(int(gig)/10)*10
            price = dic[date][gig]
            return price
        except:
            try:
                price = round(((gig*GigP) + (date*DateP))/5000,0)*5000
                return price
            except:
                return False


def GetUser(username):
    token = Token()
    print(token)
    user = requests.get(f'http://185.239.0.149:8000/api/user/{username}').content
    print(user)


GetUser('User-Jfr-106')