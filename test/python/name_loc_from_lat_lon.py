#code from article : https://stackoverflow.com/questions/69409255/how-to-get-city-state-and-country-from-a-list-of-latitude-and-longitude-coordi
import pandas as pd
import io
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="PhotoAndVideoAnlysis")

s = """Latitude   Longitude  
42.022506  -88.168156  
41.877445  -87.723846  
29.986801  -90.166314
41.393513  9.13319722
51.665077  -2.870025"""

df = pd.read_csv(io.StringIO(s), sep='\s+')

def coalesce(*arg):
  for el in arg:
    if el is not None and len(el)>0:
      return el
  return None

def city_state_country(row):
    coord = f"{row['Latitude']}, {row['Longitude']}"
    print("{}".format(coord))
    location = geolocator.reverse(coord, exactly_one=True, addressdetails=True)
    address = location.raw['address']
    city = address.get('city', '')
    town = address.get('town', '')
    village = address.get('village', '')
    state = address.get('state', '')
    country = address.get('country', '')
    row['address'] = address
    row['city'] = coalesce(city,town,village)
    row['state'] = state
    row['country'] = country
    return row

df = df.apply(city_state_country, axis=1)
print(df)