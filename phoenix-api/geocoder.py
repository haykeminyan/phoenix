from arcgis.geocoding import geocode
from arcgis.gis import GIS

gis = GIS(profile='HaykEminyan')


def get_coordinates_throughout_address(address):
    list_coordinates = geocode(address)
    return [list_coordinates[0]['location']['x'], list_coordinates[0]['location']['y']]
