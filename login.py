#!/usr/bin/env python3

import json
import requests
import common

# logout:
# https://api.nextbike.net/api/v1.1/logout.json?api_key=rXXqTgQZUPZ89lzB&loginkey=****************&device_id=********12af471e


# Mobile number must start with country code, e.g. +420
mobile = common.get_envvar_or_die("MOBILE")
pin = common.get_envvar_or_die("PIN")


login_url = "https://api.nextbike.net/api/v1.1/login.json"

params = {
    "api_key": common.api_key,
    "mobile": mobile,
    "pin": pin,
}

resp = requests.get(
    login_url,
    params=params,
    headers=common.headers,
)

try:
    resp.raise_for_status()
except requests.exceptions.HTTPError as err:
    print(err)
    print(resp.text)

json_resp = resp.json()

print(json.dumps(json_resp, indent=4))
