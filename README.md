# nextbike login and activity analysis

In this repo I show how to log in and get list of rentals from nextbike API. I ride it a lot and wanted to have some statistics.

I took inspiration from other nextbike projects:
- https://github.com/bdmbdsm/nextbike_api
- https://github.com/cybre-finn/nextbike-api-reverse-engineering

[login.py](login.py) will print login response from which you can find a "login key", and then use it with [get_list.py](get_list.py). [get_list.py](get_list.py) will download list of your activities to `list.json`. You can then analyze the file.

## login.py

Run as `MOBILE="+420735589654" PIN=232523 ./login.py` and find `login_key` in the output.

## get_list.py

Run as `LOGIN_KEY=sg9032rj32r09rj3 ./get_list.py` and see file `list.json`.

Between January 2023 and May 2024 I did
- Total aerial distance: 820.23 km
- Total rented bike time: 3 days, 9:34:26