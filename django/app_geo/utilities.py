from django.contrib.gis.geoip2 import GeoIP2  # -> ip zu lat/long
from geopy.geocoders import Nominatim  # -> str zu lat/long
from geopy.distance import geodesic  # -> lat/long math
import geoip2  # sdk von MaxMind (database)
import folium  # html/Js map render
import socket
import os


# Helper functions
class GeoLocation:
    """generic class for GeoLocation functions"""

    @staticmethod
    def get_ip_address(request) -> str:
        """get ip address of a user"""
        try:
            x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR", None)
            if x_forwarded_for:
                ip = x_forwarded_for.split(",")[0]
            else:
                ip = request.META.get("REMOTE_ADDR")
            return ip
        except AttributeError:
            return None

    @staticmethod
    def get_geolocation_from_city(city: str) -> tuple:
        """get geolocation by city name"""
        try:
            geo_locator = Nominatim(user_agent="app_geo")
            location = geo_locator.geocode(city)
            return location.latitude, location.longitude
        except:
            return (0, 0)

    @staticmethod
    def get_geolocation_from_ip(ip) -> tuple:
        """get geolocation by ip address - less accurate"""

        try:
            geo_location = GeoIP2()
            city = geo_location.city(ip)
            latitude, longitude = geo_location.lat_lon(ip)
            return city, latitude, longitude
        except geoip2.errors.AddressNotFoundError:
            return ({"city": ""}, 0, 0)
        except socket.gaierror:
            return ({"city": ""}, 0, 0)

    @staticmethod
    def get_distance(get_location_a: tuple, get_location_b: tuple) -> float:
        """Get the distance (km) between to points"""
        try:
            if (
                90 >= get_location_a[0] >= -90
                and 90 >= get_location_b[0] >= -90
                and 180 >= get_location_a[1] >= -180
                and 180 >= get_location_b[1] >= -180
            ):
                return round(geodesic(get_location_a, get_location_b).km, 2)
            else:
                return None
        except ValueError:
            return None


class GeoMap:
    """generic class for GeoMap functions"""

    @staticmethod
    def get_location_center_coordinates(
        latA: float, longA: float, latB: float = None, longB: float = None
    ) -> tuple:
        """Get the center latitude and longitude between to points"""

        cord = (latA, longA)
        if latB and longB:
            cord = ((latA + latB) / 2, (longA + longB) / 2)
        return cord

    @staticmethod
    def get_location_zoomlevel(distance: float) -> int:
        """Calculate the zoom level for a give distance"""
        if distance <= 100:
            return 12
        elif distance > 100 and distance <= 2000:
            return 6
        elif distance >= 2001 and distance <= 5000:
            return 2
        else:
            return 1

    @staticmethod
    def get_geo_map(
        map_width: int = 800,
        map_height: int = 500,
        city_location: str = "You",
        geo_location_a: tuple = (0, 0),
        city_destination: str = "",
        geo_location_b: tuple = (None, None),
        add_line: bool = False,
    ):
        """Generate a HTML map for given point"""

        geo_map = folium.Map(
            width="100%",
            height="100%",
            location=GeoMap.get_location_center_coordinates(
                geo_location_a[0],
                geo_location_a[1],
                geo_location_b[0],
                geo_location_b[1],
            ),
            zoom_start=GeoMap.get_location_zoomlevel(
                GeoLocation.get_distance(geo_location_a, geo_location_b)
            ),
        )
        # wired hack to make the folium map work as expected!
        geo_map._parent.width = "100%"
        geo_map._parent.height = "100%"
        geo_map._parent.ratio = "60%"

        # create a hotsox user marker on the map
        folium.Marker(
            [geo_location_a[0], geo_location_a[1]],
            tooltip="click here for more",
            popup=city_location,
            icon=folium.Icon(color="purple", icon="fa-socks", prefix="fa"),
        ).add_to(geo_map)

        # create another hotsox user marker on the map
        if city_destination != "":
            folium.Marker(
                [geo_location_b[0], geo_location_b[1]],
                tooltip="click here for more",
                popup=city_destination,
                icon=folium.Icon(color="red", icon="fa-socks", prefix="fa"),
            ).add_to(geo_map)

        if add_line:
            line = folium.PolyLine(
                locations=[geo_location_a, geo_location_b], weight=1, color="blue"
            )
            geo_map.add_child(line)

        return geo_map._repr_html_()
