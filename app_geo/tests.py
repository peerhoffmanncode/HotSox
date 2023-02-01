from django.test import TestCase, RequestFactory
from .utilities import GeoLocation, GeoMap


class Test(TestCase):
    def test_get_ip_address(self):
        factory = RequestFactory()
        request = factory.get("/")
        self.assertEqual(GeoLocation.get_ip_address(request), "127.0.0.1")
        self.assertEqual(GeoLocation.get_ip_address(request=None), None)

    def test_get_geolocation_from_city(self):
        self.assertEqual(
            GeoLocation.get_geolocation_from_city("Mainz"), (50.0012314, 8.2762513)
        )
        self.assertEqual(
            GeoLocation.get_geolocation_from_city("Greenwich"), (51.4820845, -0.0045417)
        )
        self.assertNotEqual(
            GeoLocation.get_geolocation_from_city("MatrixReload"),
            (85.4820845, 14.0045417),
        )
        self.assertEqual(GeoLocation.get_geolocation_from_city("MatrixReload"), (0, 0))

    def test_get_geolocation_from_ip(self):
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
            GeoLocation.get_geolocation_from_ip("256.256.256.256"), ({"city": ""}, 0, 0)
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
