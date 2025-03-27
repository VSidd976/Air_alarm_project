import pandas as pd
import numpy as np
import re
from math import radians, sin, cos, sqrt, atan2

def dms_to_decimal(degrees, minutes, seconds):
    return float(degrees) + float(minutes) / 60 + float(seconds) / 3600
    
def parse_coordinates(coord_str):
    match = re.match(r"(\d+)°(\d+)′(\d+(?:\.\d+)?)″\s*(\w+)\..*\s(\d+)°(\d+)′(\d+(?:\.\d+)?)″\s*(\w+)\..*", coord_str)
    if not match:
        raise ValueError(f"Invalid coordinate format: {coord_str}")
    
    lat_d, lat_m, lat_s, lat_dir, lon_d, lon_m, lon_s, lon_dir = match.groups()
    
    lat = dms_to_decimal(lat_d, lat_m, lat_s)
    lon = dms_to_decimal(lon_d, lon_m, lon_s)
    
    if lat_dir in ['ю', 'S']: 
        lat = -lat
    if lon_dir in ['з', 'W']:  
        lon = -lon

    return lat, lon

def haversine(lat1, lon1, lat2, lon2):
    R = 6371 
    
    φ1, φ2 = radians(lat1), radians(lat2)
    Δφ, Δλ = radians(lat2 - lat1), radians(lon2 - lon1)
    
    a = sin(Δφ/2) ** 2 + cos(φ1) * cos(φ2) * sin(Δλ/2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    return R * c


aerodromes = [
    '51°28′52″ пн. ш. 46°12′38″ сх. д.',
    '39°10′31″ пн. ш. 76°40′06″ зх. д.',
    '45°04′57″ пн. ш. 33°34′57″ сх. д.',
    '44°41′0″ пн. ш. 33°35′0″ сх. д.',
    '68°09′06″ пн. ш. 33°28′12″ сх. д.',
    '43°47′15″ пн. ш. 44°36′11″ сх. д.',
    '55°26′24″ пн. ш. 042°18′36″ сх. д.'
]

aerodrome_names = ["Engels2", "Baltimore", "Saki", "Belbek", "Olenya", "Mozdok", "Savasleyka"]

ukraine_cities = {
    "Kyiv": '50°27′00″ пн. ш. 30°31′25″ сх. д.',
    "Vinnytsia": '49°14′14″ пн. ш. 28°28′02″ сх. д.',
    "Cherkasy": '49°26′40″ пн. ш. 32°3′35″ сх. д.',
    "Chernihiv": '51°29′28″ пн. ш. 31°17′55″ сх. д.',
    "Chernivtsi": '48°17′27″ пн. ш. 25°56′04″ сх. д.',
    "Dnipro": '48°27′58″ пн. ш. 35°1′31″ сх. д.',
    "Donetsk": '48°0′32″ пн. ш. 37°48′15″ сх. д.',
    "Ivano-Frankivsk": '48°55′22″ пн. ш. 24°42′38″ сх. д.',
    "Kharkiv": '50°0′21″ пн. ш. 36°13′45″ сх. д.',
    "Kherson": '46°38′24″ пн. ш. 32°36′52″ сх. д.',
    "Khmelnytskyi": '49°25′10″ пн. ш. 26°58′46″ сх. д.',
    "Kropyvnytskyi": '48°30′36″ пн. ш. 32°16′00″ сх. д.',
    "Luhansk": '48°34′15.18″ пн. ш. 39°16′29.14″ сх. д.',
    "Lutsk": '50°44′52″ пн. ш. 25°19′28″ сх. д.',
    "Lviv": '49°50′33″ пн. ш. 24°01′56″ сх. д.',
    "Mykolaiv": '46°58′31″ пн. ш. 31°59′37″ сх. д.',
    "Odesa": '46°29′08.3″ пн. ш. 30°44′36.6″ сх. д.',
    "Poltava": '49°35′22″ пн. ш. 34°33′4″ сх. д.',
    "Rivne": '50°37′11″ пн. ш. 26°15′05″ сх. д.',
    "Simferopol": '44°57′0″ пн. ш. 34°6′0″ сх. д.',
    "Sumy": '50°54′43″ пн. ш. 34°48′12″ сх. д.',
    "Ternopil": '49°34′12″ пн. ш. 25°36′50″ сх. д.',
    "Uzhhorod": '48°37′26″ пн. ш. 22°17′42″ сх. д.',
    "Zaporizhzhia": '47°50′16″ пн. ш. 35°8′18″ сх. д.',
    "Zhytomyr": '50°15′16″ пн. ш. 28°39′28″ сх. д.'
}


aerodrome_coords = [parse_coordinates(a) for a in aerodromes]
city_coords = {name: parse_coordinates(coord) for name, coord in ukraine_cities.items()}


data = []
for city, (city_lat, city_lon) in city_coords.items():
    row = {"City": city}
    for aerodrome, (aero_lat, aero_lon) in zip(aerodrome_names, aerodrome_coords):
        row[aerodrome] = round(haversine(city_lat, city_lon, aero_lat, aero_lon), 2)
    data.append(row)


df = pd.DataFrame(data)
#print(df)
df.to_csv("distances.csv", index=False)