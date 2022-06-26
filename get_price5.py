import requests
import json

APP_KEY = "PSuEp1LlfF5qjERlPjilJB8eB5Eqm5mvN6bi"
APP_SECRET = "hTEKH4DPushXKUWdyOPJZCJ5fbJK1EIN8jcIp9xOpVfvViDcv49B+GcCodlOkMR9CJPBfqR7ZG8c+OLPlNdOd1oHTKHeADikVQEAqDy5w3H8dJt2h9E6qaKaRH9kLogvYidabegbdJkWv8izszK4vYpiGJr9CJEYXSi+JVdvrpT4/kxfoUo="
URL_BASE = "https://openapi.koreainvestment.com:9443"

headers = {"content-type":"application/json"}
body = {"grant_type":"client_credentials",
        "appkey":APP_KEY, 
        "appsecret":APP_SECRET}

PATH = "oauth2/tokenP"
URL = f"{URL_BASE}/{PATH}"

res = requests.post(URL, headers=headers, data=json.dumps(body))
res.text

ACCESS_TOKEN = res.json()["access_token"]

datas = {
    "CANO": '00000000',
    "ACNT_PRDT_CD": "01",
    "OVRS_EXCG_CD": "SHAA",
    "PDNO": "00001",
    "ORD_QTY": "500",
    "OVRS_ORD_UNPR": "52.65",
    "ORD_SVR_DVSN_CD": "0"}

headers = {
    'content-Type' : 'application/json',
    'appKey' : APP_KEY,
    'appSecret' : APP_SECRET}

PATH = "uapi/hashkey"
URL = f"{URL_BASE}/{PATH}"

res = requests.post(URL, headers=headers, data=json.dumps(datas))
res.text

HASHKEY = res.json()["HASH"]
print(hashkey)

headers = {"Content-Type": "application/json",
            "authorization": f"Bearer {ACCESS_TOKEN}",
            "appKey": APP_KEY,
            "appSecret": APP_SECRET,
            "tr_id": "HHDFS00000300",
#            "hashkey": hashkey(data)}
            "hashkey": HASHKEY}

body = {"AUTH": "",
        "EXCD": "NAS",
        "SYMB": "TQQQ"}

PATH = "uapi/overseas-price/v1/quotations/price"
URL = f"{URL_BASE}/{PATH}"
res = requests.post(URL, headers=headers, data=json.dumps(body))
#res = requests.get(URL, headers=headers, data=json.dumps(body))
print(res.text)
