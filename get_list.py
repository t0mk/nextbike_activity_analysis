#!/usr/bin/env python3

import json
import requests
import common

login_key = common.get_envvar_or_die("LOGIN_KEY")

list_url = "https://api.nextbike.net/api/v1.1/list.json"

params = {
    "apikey": common.api_key,
    "loginkey": login_key,
    "limit": 10000000000
}

resp = requests.get(list_url, params=params, headers=common.headers)

try:
    resp.raise_for_status()
except requests.exceptions.HTTPError as err:
    print(err)
    print(resp.text)

json_resp = resp.json()

with open("list.json", "w") as f:
    json.dump(json_resp, f, indent=4)
