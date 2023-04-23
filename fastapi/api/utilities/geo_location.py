from geopy.geocoders import Nominatim


def get_geolocation_from_city(city: str) -> tuple:
    """get geolocation by city name"""
    try:
        geo_locator = Nominatim(user_agent="app_geo")
        location = geo_locator.geocode(city)
        return location.latitude, location.longitude
    except:
        return (None, None)
