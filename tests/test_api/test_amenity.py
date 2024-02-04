#!/usr/bin/python3
from api.v1.app import app
import unittest
import os


class FlaskTestCase(unittest.TestCase):
    data = {"name": "Some Amenity"}

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.app = app

    def test_post_method(self):
        tester = app.test_client(self)
        response = tester.post('/api/v1/amenities', json=self.data)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.status_code, 201)

    def test_get_method_by_id(self):
        tester = app.test_client(self)
        response = tester.post('/api/v1/amenities', json=self.data)
        response = tester.get('/api/v1/amenities')
        self.assertEqual(response.status_code, 200)
        data1 = response.data.decode('UTF-8')
        amenities = ast.literal_eval(data1)
        amenity_id = amenities[-1]['id']

        response = tester.get('/api/v1/amenities/{}'.format(amenity_id))
        self.assertEqual(response.status_code, 200)

    def test_put_method(self):
        tester = app.test_client(self)
        response = tester.post('/api/v1/amenities', json=self.data)
        response = tester.get('/api/v1/amenities')
        data1 = response.data.decode('UTF-8')
        amenities = ast.literal_eval(data1)
        amenity_id = amenities[-1]['id']

        response = tester.put('/api/v1/amenities/{}'.format(amenity_id),
                              json={'name': 'Updated Amenity'})
        self.assertEqual(response.status_code, 200)

    def test_delete_method(self):
        tester = app.test_client(self)
        response = tester.post('/api/v1/amenities', json=self.data)
        response = tester.get('/api/v1/amenities')
        data1 = response.data.decode('UTF-8')
        amenities = ast.literal_eval(data1)
        amenity_id = amenities[-1]['id']

        response = tester.delete('/api/v1/amenities/{}'.format(amenity_id))
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
