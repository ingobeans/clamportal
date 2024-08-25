from request_data import *
from requests_ntlm import HttpNtlmAuth
from urllib.parse import unquote
import json, datetime

with open("config.json","r") as f:
    config = json.load(f)

session = requests.Session()
session.auth = HttpNtlmAuth(config["username"], config["password"])

week_number = datetime.date.today().isocalendar()[1]

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
print("got skolportalen session")
portal2 = second_skolportal(hag_cookies)
portal3 = third_skolportal(hag_cookies, session)
print("authenticated skolportalen")
portal_home = home_skolportal(hag_cookies)
portal_me = me_skolportal(hag_cookies)

skola1 = first_skola24()
skola_cookies = parse_cookies(skola1.headers["Set-Cookie"])
print("got skola24 session")
skola2 = second_skola24(skola_cookies)
skola3 = third_skola24(skola_cookies)
skola_login = skola24_login(skola_cookies)
skola_saml1 = first_skola24_saml()
saml_data1 = skola_saml1.text.split("lue=\"",1)[1].split("\"",1)[0]
print("got skola24 saml data")
skola_saml2 = second_skola24_saml(hag_cookies, saml_data1)
saml_data2 = skola_saml2.text.split("lue=\"",1)[1].split("\"",1)[0]
print("got new skola24 saml data")
skola_saml3 = third_skola24_saml(saml_data2)
print("authenticated saml")
sign_in_url = unquote(skola_saml3.headers["Location"])
skola_signin = skola24_signin(sign_in_url.split("?t=",1)[1], skola_cookies)
print("signed in to skola24")
# load timetable
#skola_info = skola24_info(skola_cookies)
years = timetable_years(skola_cookies)
timetables = timetable_timetables(skola_cookies)
key = timetable_key(skola_cookies)

years_data = years.json()
timetables_data = timetables.json()
key_data = key.json()
print("got timetable data")

timetable = timetable(skola_cookies, years_data, timetables_data, key_data, week_number, 500, 500, 0)
print("got timetable")

explore()