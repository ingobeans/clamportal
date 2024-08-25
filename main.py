from request_data import *
from requests_ntlm import HttpNtlmAuth
import json

with open("config.json","r") as f:
    config = json.load(f)
session = requests.Session()
session.auth = HttpNtlmAuth(config["username"], config["password"])

def explore():
    while True:
        try:
            print(eval(input(">")))
        except Exception as e:
            print(str(e))

def parse_cookies(cookie_header: str) -> dict:
    cookies = {}
    cookie_pairs = cookie_header.split(', ')
    for cookie in cookie_pairs:
        key_value_pair = cookie.split(';', 1)[0]
        key, value = key_value_pair.split('=', 1)
        
        
        cookies[key] = value
    return cookies

s1 = first_skolportal()
hag_cookies = parse_cookies(s1.headers["Set-Cookie"])
s2 = second_skolportal(hag_cookies)
s3 = third_skolportal(hag_cookies, session)
hs = home_skolportal(hag_cookies)
me = me_skolportal(hag_cookies)
explore()