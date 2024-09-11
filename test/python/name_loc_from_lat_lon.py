#code from article : https://stackoverflow.com/questions/69409255/how-to-get-city-state-and-country-from-a-list-of-latitude-and-longitude-coordi
import pandas as pd
import io
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="PhotoAndVideoAnlysis")

s = """Latitude   Longitude  
42.022506  -88.168156  
41.877445  -87.723846  
29.986801  -90.166314
41.393513  9.13319722"""

df = pd.read_csv(io.StringIO(s), sep='\s+')

def city_state_country(row):
    coord = f"{row['Latitude']}, {row['Longitude']}"
    location = geolocator.reverse(coord, exactly_one=True)
    address = location.raw['address']
    city = address.get('town', '')
    state = address.get('state', '')
    country = address.get('country', '')
    row['address'] = address
    row['city'] = city
    row['state'] = state
    row['country'] = country
    return row

df = df.apply(city_state_country, axis=1)
print(df)