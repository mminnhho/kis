import requests
import json

APP_KEY = "PSuEp1LlfF5qjERlPjilJB8eB5Eqm5mvN6bi"
APP_SECRET = "hTEKH4DPushXKUWdyOPJZCJ5fbJK1EIN8jcIp9xOpVfvViDcv49B+GcCodlOkMR9CJPBfqR7ZG8c+OLPlNdOd1oHTKHeADikVQEAqDy5w3H8dJt2h9E6qaKaRH9kLogvYidabegbdJkWv8izszK4vYpiGJr9CJEYXSi+JVdvrpT4/kxfoUo="
URL_BASE = "https://openapi.koreainvestment.com:9443"

headers = {"content-type": "application/json"}

body = {"grant_type": "client_credentials",
        "appkey": APP_KEY,
        "appSecret": APP_SECRET}

PATH = "oauth2/token"
#PATH = "uapi/overseas-price/v1/quotations/price"

URL = f"{URL_BASE}/{PATH}"
print(URL)

res = requests.post(URL, headers=headers, data=json.dumps(body))
#res.text
print(res.text)

ACCESS_TOKEN = res.json()["access_token"]

headers = {"Content-Type": "application/json", 
           "authorization": f"Bearer {ACCESS_TOKEN}",
           "appKey": APP_KEY,
           "appSecret": APP_SECRET,
           "tr_id": "HHDFS00000300"}

body = {"AUTH": "",
        "EXCD": "NAS",
        "SYMB": "TQQQ"}

#PATH = "oauth2/tokenP"
#URL = f"{URL_BASE}/{PATH}"
#
#res = requests.post(URL, headers=headers, data=json.dumps(body))
#res.text
#print(res.text)
#
#ACCESS_TOKEN = res.json()["access_token"]
#
#headers = {"Content-Type":"application/json", 
#           "authorization": f"Bearer {ACCESS_TOKEN}",
#           "appKey":APP_KEY,
#           "appSecret":APP_SECRET,
#           "tr_id":"FHKST01010100"}
#           
##PATH = "uapi/domestic-stock/v1/quotations/inquire-price"
#PATH = "uapi/overseas-price/v1/quotations/price"
#URL = f"{URL_BASE}/{PATH}"
#print(URL)
#
#params = {
#    "fid_cond_mrkt_div_code":"J",
#    "fid_input_iscd":"TQQQ"
#}
#
#res = requests.get(URL, headers=headers, params=params)
#res.json()['output']['stck_prpr']
#print(res.json()['output']['stck_prpr'])
