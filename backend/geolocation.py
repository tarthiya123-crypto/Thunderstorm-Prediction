# geolocation.py

def pixel_to_latlon(x, y):
    WIDTH = 3062
    HEIGHT = 3207

    MIN_LAT = -50.0
    MAX_LAT = 50.0

    MIN_LON = 20.0
    MAX_LON = 130.0

    lon = MIN_LON + (x / WIDTH) * (MAX_LON - MIN_LON)

    lat = MAX_LAT - (y / HEIGHT) * (MAX_LAT - MIN_LAT)

    return lat, lon