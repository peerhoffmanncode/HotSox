from django.test import TestCase, RequestFactory
from .utilities import GeoLocation, GeoMap
import os


class Test(TestCase):
    def test_get_ip_address(self):
        factory = RequestFactory()
        request = factory.get("/")
        self.assertEqual(GeoLocation.get_ip_address(request), "127.0.0.1")
        self.assertEqual(GeoLocation.get_ip_address(request=None), None)

    def test_get_geolocation_from_city(self):
        if not os.getenv("GITHUB_WORKFLOW"):
            self.assertEqual(
                GeoLocation.get_geolocation_from_city("Mainz"), (50.0012314, 8.2762513)
            )
            self.assertEqual(
                GeoLocation.get_geolocation_from_city("Greenwich"),
                (51.4820845, -0.0045417),
            )
            self.assertNotEqual(
                GeoLocation.get_geolocation_from_city("MatrixReload"),
                (85.4820845, 14.0045417),
            )
            self.assertEqual(
                GeoLocation.get_geolocation_from_city("MatrixReload"), (0, 0)
            )

    def test_get_geolocation_from_ip(self):
        if not os.getenv("GITHUB_WORKFLOW"):
            self.assertEqual(
                GeoLocation.get_geolocation_from_ip("8.8.8.8"),
                (
                    {
                        "city": None,
                        "continent_code": "NA",
                        "continent_name": "North America",
                        "country_code": "US",
                        "country_name": "United States",
                        "dma_code": None,
                        "is_in_european_union": False,
                        "latitude": 37.751,
                        "longitude": -97.822,
                        "postal_code": None,
                        "region": None,
                        "time_zone": "America/Chicago",
                    },
                    37.751,
                    -97.822,
                ),
            )

            self.assertEqual(
                GeoLocation.get_geolocation_from_ip("256.256.256.256"),
                ({"city": ""}, 0, 0),
            )

    def test_get_distance(self):
        self.assertEqual(
            GeoLocation.get_distance((50.0012314, 8.2762513), (50.0012314, 8.2762513)),
            0.0,
        )

        self.assertEqual(
            GeoLocation.get_distance((0.0, 0.0), (90.0, 0.0)),
            10001.97,
        )

        self.assertEqual(
            GeoLocation.get_distance((91.0, -180.1), (90.0, 0.0)),
            None,
        )

    def test_geomap_get_location_center_coordinates(self):
        # middle between two valid coordinates
        self.assertEqual(
            GeoMap.get_location_center_coordinates(20, 20, 40, 40),
            (30, 30),
        )
        # middle between two valid coordinates
        self.assertNotEqual(
            GeoMap.get_location_center_coordinates(40, 40, 20, 20),
            (31, 31),
        )

        # middle between one valid coordinate!
        self.assertEqual(
            GeoMap.get_location_center_coordinates(20, 20, None, None),
            (20, 20),
        )

    def test_geomap_get_location_zoomlevel(self):
        # middle between two valid coordinates
        self.assertEqual(
            GeoMap.get_location_zoomlevel(100),
            12,
        )
        self.assertEqual(
            GeoMap.get_location_zoomlevel(101),
            6,
        )
        self.assertEqual(
            GeoMap.get_location_zoomlevel(5001),
            2,
        )

    def test_geomap_get_geo_map(self):
        test_map1 = GeoMap.get_geo_map(
            map_width=250,
            map_height=250,
            city_location="Mainz",
            geo_location_a=(50.0012314, 8.2762513),
            city_destination="Hamburg",
            geo_location_b=(53.550341, 10.000654),
        )
        # deprecated because of the bugs inside folium!
        # self.assertIn("width: 250.0px;", test_map1)
        # self.assertIn("height: 250.0px;", test_map1)
        self.assertIn("[51.7757862, 9.138452650000001]", test_map1)
        self.assertIn("zoom: 6", test_map1)
        self.assertIn("Mainz", test_map1)
        self.assertIn("Hamburg", test_map1)
