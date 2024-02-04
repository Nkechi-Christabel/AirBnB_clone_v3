#!/usr/bin/python3
from api.v1.app import app as app
import unittest
import os


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                 "Testing FileStorage")
class FlaskTestCase(unittest.TestCase):
    data = {"name": "Test Place", "user_id": "user_id", "city_id": "city_id"}

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.app = app

    def test_post_method(self):
        tester = app.test_client(self)
        response = tester.post('/api/v1/cities/city_id/places', json=self.data)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.status_code, 201)

    def test_get_method_by_id(self):
        tester = app.test_client(self)
        response = tester.post('/api/v1/cities/city_id/places', json=self.data)
        data = response.get_json()
        place_id = data['id']

        response = tester.get(f'/api/v1/places/{place_id}')
        self.assertEqual(response.status_code, 200)

    def test_put_method(self):
        tester = app.test_client(self)
        response = tester.post('/api/v1/cities/city_id/places', json=self.data)
        data = response.get_json()
        place_id = data['id']

        response = tester.put(f'/api/v1/places/{place_id}',
                              json={'name': 'Updated Place'})
        self.assertEqual(response.status_code, 200)

    def test_delete_method(self):
        tester = app.test_client(self)
        response = tester.post('/api/v1/cities/city_id/places', json=self.data)
        data = response.get_json()
        place_id = data['id']

        response = tester.delete(f'/api/v1/places/{place_id}')
        self.assertEqual(response.status_code, 200)

    def test_search_places(self):
        tester = app.test_client(self)
        response = tester.post('/api/v1/places_search', json={"states": [],
                               "cities": ["city_id"], "amenities": []})
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
