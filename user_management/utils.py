import requests
from geoposition import Geoposition


def query_zip_code(zip_code):
    if not zip_code.isdigit():
        return
    r = requests.get('http://api.zippopotam.us/de/%s' % zip_code)
    if r.status_code == 200:
        result = r.json()['places'][0]
        return Geoposition(result['latitude'], result['longitude'])
