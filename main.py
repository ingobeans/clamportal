import json, clam

with open("config.json","r") as f:
    config = json.load(f)

skolportal_session = clam.SkolportalSession(config["username"], config["password"], authmech=clam.Authmech.MICROSOFT)
skola24_session = clam.Skola24Session(skolportal_session)

print(skola24_session.get_timetable(18,600,600,1,2026))
last = None
while True:
    last = eval(input(">"))