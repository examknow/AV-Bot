import requests

configfile = open('config.csv', 'r')
for line in configfile:
  setting = line.split(';')
  print(setting)
  if setting[0] == 'username':
    username = setting[1]
  if setting[0] == 'flagpass':
    flagpass = setting[1]
  if setting[0] == 'noflagpass':
    noflagpass = setting[1]

def revertChange(page, user):




S = requests.Session()

URL = "https://test.miraheze.org/w/api.php"

PARAMS = {
    "format": "json",
    "rcprop": "title|ids|sizes|flags|user|comment",
    "list": "recentchanges",
    "action": "query",
    "rclimit": "3"
}

R = S.get(url=URL, params=PARAMS)
DATA = R.json()

RECENTCHANGES = DATA['query']['recentchanges']

for rc in RECENTCHANGES:
    print(str(rc['title']) + ' with the comment: ' + str(rc['comment']))
    if str(rc['comment']) == 'reset':
        print("ALERT! Vandalism found on " + str(rc['title']))
