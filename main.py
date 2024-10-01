import json, clam

with open("config.json","r") as f:
    config = json.load(f)

skolportal_session = clam.SkolportalSession(config["username"], config["password"])
print(skolportal_session.get_user_attributes())
skola24_session = clam.Skola24Session(skolportal_session)
print(skola24_session.get_info())