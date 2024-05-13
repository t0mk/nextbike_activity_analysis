import os
import sys
import datetime
import json
import pandas as pd
import numpy as np
import random

api_key = "rXXqTgQZUPZ89lzB"

headers = {
    "Accept-Encoding": "gzip",
    "Accept-Language": "en-US,fi-FI;q=0.9,cs-CZ;q=0.79999995",
    "Connection": "Keep-Alive",
    "Host": "api.nextbike.net",
    "User-Agent": "nextbike/a.v4-v4.31.2/Google Pixel 4a",
}


def time_agg(indf, freq, format_string):
    agg1 = pd.NamedAgg(column='real_distance_km', aggfunc='sum')
    agg2 = pd.NamedAgg(column='duration_minutes', aggfunc='sum')
    agg3 = pd.NamedAgg(column='datetime', aggfunc='count')
    res_agg = indf.groupby(pd.Grouper(key="datetime", freq=freq)).agg(
        real_distance_km=agg1, duration_minutes=agg2, trips=agg3
    ).reset_index()
    res_agg.index = res_agg["datetime"].dt.strftime(format_string)
    # we skip slots with zero distance - days/months where we didn't ride
    res_agg = res_agg[res_agg['real_distance_km'] > 0]
    # drop datetime
    res_agg = res_agg.drop(columns=['datetime'])

    return res_agg


def get_envvar_or_die(name):
    value = os.getenv(name)
    if value is None:
        print(f"Environment variable {name} is not set.")
        sys.exit(1)
    return value


def df_from_list(fn):

    with open(fn, "r") as f:
        data = json.load(f)
    its = data["account"]["items"]
    rs = [i for i in its if i['node'] == 'rental']

    d = dict(
        datetime=[],
        duration_minutes=[],
        sla=[],
        slo=[],
        ela=[],
        elo=[],
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

        d["sla"].append(r["start_place_lat"])
        d["slo"].append(r["start_place_lng"])
        d["ela"].append(r["end_place_lat"])
        d["elo"].append(r["end_place_lng"])
        d["datetime"].append(st)
        d["duration_minutes"].append(duration.total_seconds() / 60)
    df = pd.DataFrame(d)
    return df


def interpolate_arc(lat1, lng1, lat2, lng2, n, height=0.1):
    # Convert latitude and longitude from degrees to radians
    lat1, lng1, lat2, lng2 = map(np.radians, [lat1, lng1, lat2, lng2])

    # Compute the midpoint (using average for simplicity)
    mid_lat = (lat1 + lat2) / 2
    mid_lng = (lng1 + lng2) / 2

    # Control point height adjustment (simplified calculation)
    dLat = lat2 - lat1
    dLng = lng2 - lng1
    random.seed()
    factor = random.uniform(.75, 1.25)
    # Determine height direction based on longitude difference
    # If lng2 > lng1, the curve should arc upwards/rightwards in typical web map visualization
    height_direction = np.sign(dLng)
    ctrl_lat = mid_lat + height_direction * height * dLng * factor
    ctrl_lng = mid_lng - height_direction * height * dLat * factor

    # Generate points along the Bezier curve
    t = np.linspace(0, 1, n)
    curve_lat = (1 - t)**2 * lat1 + 2 * (1 - t) * t * ctrl_lat + t**2 * lat2
    curve_lng = (1 - t)**2 * lng1 + 2 * (1 - t) * t * ctrl_lng + t**2 * lng2

    # Convert back to degrees
    curve_lat = np.degrees(curve_lat)
    curve_lng = np.degrees(curve_lng)
    return list(zip(curve_lat, curve_lng))
