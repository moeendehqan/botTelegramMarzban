from pymongo import MongoClient
import requests
import json
import datetime
from persiantools.jdatetime import JalaliDate
client = MongoClient('mongodb://root:YgXs5qROdTNGqW13EADso3VM@sinai.liara.cloud:30651/my-app?authSource=admin')

db = client['bot']
pacing = {
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


def Token():
    token = requests.post('http://185.239.0.149:8000/api/admin/token',data={'username':'moeen', 'password':'Moeen....6168'})
    token = json.loads(token.content)
    token = token['access_token']
    return token

def bits_to_gigabytes(bits):
    bytes = bits * 9.3132257461548E-10
    return round(bytes,2)


def gigabytes_to_bits(gigabyte):
    bytes = gigabyte * (1/9.3132257461548E-10)
    return round(bytes,0)



def clean_sub(sub):
    sub = str(sub).replace('http://185.239.0.149:8000/sub/','')
    return sub


def UserGetUsage(sub):
    sub = clean_sub(sub)
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
    try:
        price = int(pacing[date][gig])
        return {'price':price,'date':date,'gig':gig}
    except:
        try:
            date = max(int(int(date)/30)*30,30)
            gig = int(int(gig)/10)*10
            price = int(pacing[date][gig])
            return {'price':price,'date':date,'gig':gig}
        except:
            try:
                date = int(int(date)/30)*30
                gig = int(int(gig)/10)*10
                price = int(round(((gig*GigP) + (date*DateP))/5000,0)*5000)
                return {'price':price,'date':date,'gig':gig}
            except:
                price = int(pacing[30][20])
                return {'price':price,'date':30,'gig':20}


def GetUser(sub):
    sub = clean_sub(sub)
    username = UserGetUsage(sub)['username']
    token = Token()
    header = {'accept':'application/json', 'Authorization':f'Bearer {token}'}
    respone = requests.get(url=f'http://185.239.0.149:8000/api/user/{username}', headers=header)
    user = json.loads(respone.content)
    return user



def ReNow(sub):
    sub = clean_sub(sub)
    userUsage = UserGetUsage(sub)
    get_price = GetPrice(userUsage['data_limit_gig'],userUsage['timing'])
    now = datetime.datetime.now()
    expire_last_day = userUsage['expire_last_day']
    expire = now + datetime.timedelta(days=get_price['date']+expire_last_day)
    expire = expire.timestamp()
    data_limit_avilabel = userUsage['data_limit_gig'] - userUsage['used_traffic_gig']
    data_limit = gigabytes_to_bits(get_price['gig'] + data_limit_avilabel)
    username = userUsage['username']
    token = Token()
    header = {'accept':'application/json', 'Authorization':f'Bearer {token}', 'Content-Type':'application/json'}
    data = json.dumps({'expire':expire, 'data_limit':data_limit})
    response = requests.put(url=f'http://185.239.0.149:8000/api/user/{username}', headers=header, data=data)

def reNew_to_db(username, date, gig, sub, price, chat_id):
    sub = clean_sub(sub)
    now = datetime.datetime.now()
    db['renew'].insert_one({'username':username, 'date':date, 'gig':gig,'sub':sub, 'price':price,'chat_id':chat_id, 'datetime':str(now), 'verify':False})


def start_to_db(js):
    try:
        db['start'].insert_one(js)
    except:
        pass

def sub_by_chat_set(sub, chat_id):
    sub = clean_sub(sub)
    now = str(datetime.datetime.now())
    db['sub_by_chat'].insert_one({'sub':sub,'chat_id':chat_id, 'datetime':now, 'timestump':datetime.datetime.now().timestamp()})

def sub_by_chat_lates_get(chat_id):
    try:
        sub = db['sub_by_chat'].find_one({'chat_id':chat_id},sort=[('timestump',-1)])['sub']
        return sub
    except:
        return False


def packing():
    pacNum = 1
    listE = []
    for d in pacing:
        for g in pacing[d]:
            dic = {'num':pacNum ,'gig':g, 'date':d, 'price':pacing[d][g]}
            pacNum = pacNum + 1
            listE.append(dic)
    return listE