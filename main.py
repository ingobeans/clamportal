from request_data import *
from requests_ntlm import HttpNtlmAuth
from urllib.parse import unquote
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

portal1 = first_skolportal()
hag_cookies = parse_cookies(portal1.headers["Set-Cookie"])
portal2 = second_skolportal(hag_cookies)
portal3 = third_skolportal(hag_cookies, session)
portal_home = home_skolportal(hag_cookies)
portal_me = me_skolportal(hag_cookies)
#portal_set_me = set_me_attributes_skolportal(hag_cookies, {
#   "plugin-splash-color":"#008000",
#   "plugin-splash-text":"howdy !!",
#   "hello hello hello":"can anybody hear me?"
#})
#
skola1 = first_skola24()
skola_cookies = parse_cookies(skola1.headers["Set-Cookie"])
skola2 = second_skola24(skola_cookies)
skola3 = third_skola24(skola_cookies)
skola_login = skola24_login(skola_cookies)
skola_saml1 = first_skola24_saml()
saml_data1 = skola_saml1.text.split("lue=\"",1)[1].split("\"",1)[0]
skola_saml2 = second_skola24_saml(hag_cookies, saml_data1)
saml_data2 = skola_saml2.text.split("lue=\"",1)[1].split("\"",1)[0]
skola_saml3 = third_skola24_saml(saml_data2)
sign_in_url = unquote(skola_saml3.headers["Location"])
skola_signin = skola24_signin(sign_in_url.split("?t=",1)[1], skola_cookies)
# load timetable
#skola_info = skola24_info(skola_cookies)
years = timetable_years(skola_cookies)
timetables = timetable_timetables(skola_cookies)
key = timetable_key(skola_cookies)

years_data = years.json()
timetables_data = timetables.json()
key_data = key.json()

timetable = timetable(skola_cookies, years_data, timetables_data, key_data)

explore()