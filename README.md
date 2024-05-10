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

# My results January 2023 - May 2024

- Total aerial distance ridden: 820.23 km, "map" distance ~ 1116 km [0]
- Total rented bike time: 3 days, 9:34:26
- Total rentals: 410

[0] I measured that my most common ride is 3.01 km aerial and 4.1 km on the map, so I factor by 1.36