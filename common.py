import os
import sys
import datetime
import json

api_key = "rXXqTgQZUPZ89lzB"

headers = {
    "Accept-Encoding": "gzip",
    "Accept-Language": "en-US,fi-FI;q=0.9,cs-CZ;q=0.79999995",
    "Connection": "Keep-Alive",
    "Host": "api.nextbike.net",
    "User-Agent": "nextbike/a.v4-v4.31.2/Google Pixel 4a",
}


def get_envvar_or_die(name):
    value = os.getenv(name)
    if value is None:
        print(f"Environment variable {name} is not set.")
        sys.exit(1)
    return value


def df_from_list():
    import haversine as hs
    from haversine import Unit
    import pandas as pd
    with open("list.json", "r") as f:
        data = json.load(f)
    its = data["account"]["items"]
    rs = [i for i in its if i['node'] == 'rental']

    totaldist = 0
    totaltime = None

    d = dict(
        datetime=[],
        duration=[],
        distance=[],
    )

    for r in rs:
        unixst = r["start_time"]
        unixet = r["end_time"]
        st = datetime.datetime.fromtimestamp(unixst)
        et = datetime.datetime.fromtimestamp(unixet)

        duration = et - st
        if duration.total_seconds() < 60:
            # we skip short rentals
            continue

        sla = r["start_place_lat"]
        slo = r["start_place_lng"]
        ela = r["end_place_lat"]
        elo = r["end_place_lng"]

        if sla == 0:
            # we skip rentals with missing start location, that's some bug
            continue
        dist = hs.haversine((sla, slo), (ela, elo), unit=Unit.KILOMETERS)

        if totaltime is None:
            totaltime = duration
        else:
            totaltime += duration
        totaldist += dist
        d["datetime"].append(st)
        d["duration"].append(duration)
        d["distance"].append(dist)
    print(f"Total distance: {totaldist:.2f} km")
    print(f"Total time: {totaltime}")
    return pd.DataFrame(d)
