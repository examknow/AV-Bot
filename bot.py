import requests

lastdiff = 0

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

def warnUser(page, user):
  global username
  global flagpass
  global noflagpass
  S = requests.Session()

  URL = "https://test.miraheze.org/w/api.php"
  PARAMS_0 = {
      "action": "query",
      "meta": "tokens",
      "type": "login",
      "format": "json"
  }

  R = S.get(url=URL, params=PARAMS_0)
  DATA = R.json()

  LOGIN_TOKEN = DATA['query']['tokens']['logintoken']
  PARAMS_1 = {
      "action": "login",
      "lgname": username,
      "lgpassword": flagpass,
      "lgtoken": LOGIN_TOKEN,
      "format": "json"
  }

  R = S.post(URL, data=PARAMS_1)

  PARAMS_2 = {
      "action": "query",
      "meta": "tokens",
      "format": "json"
  }

  R = S.get(url=URL, params=PARAMS_2)
  DATA = R.json()

  CSRF_TOKEN = DATA['query']['tokens']['csrftoken']

  PARAMS_3 = {
      "action": "edit",
      "title": "User talk:" + user,
      "token": CSRF_TOKEN,
      "format": "json",
      "bot": "true",
      "appendtext": "\n== {{subst:CURRENTMONTHNAME}} {{subst:CURRENTYEAR}} == \n{{subst:User:EkWikiBot/WarnVandal|" + page + "}}"
  }

  R = S.post(URL, data=PARAMS_3)
  DATA = R.json()

  print(DATA)

def revertChange(page, user):
  global username
  global flagpass
  global noflagpass
  S = requests.Session()

  URL = "https://test.miraheze.org/w/api.php"

  PARAMS_1 = {
      "action": "query",
      "meta": "tokens",
      "type": "login",
      "format": "json"
  }

  R = S.get(url=URL, params=PARAMS_1)
  DATA = R.json()

  LOGIN_TOKEN = DATA['query']['tokens']['logintoken']
  PARAMS_2 = {
      "action": "login",
      "lgname": username,
      "lgpassword": noflagpass,
      "lgtoken": LOGIN_TOKEN,
      "format": "json"
  }

  R = S.post(URL, data=PARAMS_2)

  PARAMS_3 = {
      "action": "query",
      "meta": "tokens",
      "format": "json"
  }

  R = S.get(url=URL, params=PARAMS_3)
  DATA = R.json()

  CSRF_TOKEN = DATA["query"]["tokens"]["csrftoken"]

  R = S.post(URL, data=PARAMS_3)

  PARAMS_4 = {
      "action": "query",
      "meta": "tokens",
      "type": "rollback",
      "format": "json"
  }

  R = S.get(url=URL, params=PARAMS_4)
  DATA = R.json()

  ROLLBACK_TOKEN = DATA['query']['tokens']['rollbacktoken']

  # Step 5: POST request to rollback a page
  PARAMS_5 = {
      "action": "rollback",
      "format": "json",
      "title": page,
      "user": user,
      "token": ROLLBACK_TOKEN,
  }

  R = S.post(URL, data=PARAMS_5)
  DATA = R.json()

  print(DATA)


while True:
  S = requests.Session()

  URL = "https://test.miraheze.org/w/api.php"

  PARAMS = {
      "format": "json",
      "rcprop": "title|ids|sizes|flags|user|comment",
      "list": "recentchanges",
      "action": "query",
      "rctoponly": "true",
      "rcdir": "newer"
      
  }

  R = S.get(url=URL, params=PARAMS)
  DATA = R.json()

  RECENTCHANGES = DATA['query']['recentchanges']

  for rc in RECENTCHANGES:
      if str(rc['revid']) < lastdiff:
        pass
      print(str(rc['title']) + ' with the comment: ' + str(rc['comment']))
      if str(rc['comment']) == 'reset':
          print("ALERT! Vandalism found on " + str(rc['title']))
          rolluser = str(rc['user'])
          rollpage = str(rc['title'])
          revertChange(rollpage, rolluser)
          warnUser(rollpage, rolluser)
