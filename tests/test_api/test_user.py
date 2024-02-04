#!/usr/bin/python3
from api.v1.app import app
import unittest
import os


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                 "Testing FileStorage")
class FlaskTestCase(unittest.TestCase):
    data = {"email": "test@example.com", "password": "testpassword"}

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.app = app

    def test_post_method(self):
        tester = app.test_client(self)
        response = tester.post('/api/v1/users', json=self.data)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.status_code, 201)

    def test_get_method_by_id(self):
        tester = app.test_client(self)
        response = tester.post('/api/v1/users', json=self.data)
        data = response.get_json()
        user_id = data['id']

        response = tester.get(f'/api/v1/users/{user_id}')
        self.assertEqual(response.status_code, 200)

    def test_put_method(self):
        tester = app.test_client(self)
        response = tester.post('/api/v1/users', json=self.data)
        data = response.get_json()
        user_id = data['id']

        response = tester.put(f'/api/v1/users/{user_id}',
                              json={'email': 'updated@example.com'})
        self.assertEqual(response.status_code, 200)

    def test_delete_method(self):
        tester = app.test_client(self)
        response = tester.post('/api/v1/users', json=self.data)
        data = response.get_json()
        user_id = data['id']

        response = tester.delete(f'/api/v1/users/{user_id}')
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
