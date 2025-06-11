import json

with open('src/static/validators/user.json', 'r') as file:
    thefile = json.load(file)
    print(thefile)