# python test_bloglist.py
import unittest
import os
import json
from app import create_app, db


class BloglistTestCase(unittest.TestCase):
    """This class represents the bloglist test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.bloglist = {'name': 'Flask rest api with TDD'}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_bloglist_creation(self):
        """Test API can create a bloglist (POST request)"""
        res = self.client().post('/bloglists', data=self.bloglist)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Flask rest api with TDD', str(res.data))

    def test_api_can_get_all_bloglists(self):
        """Test API can get a bloglist (GET request)."""
        res = self.client().post('/bloglists', data=self.bloglist)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/bloglists')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Flask rest api with TDD', str(res.data))

    def test_api_can_get_bloglist_by_id(self):
        """Test API can get a single bloglist by using it's id."""
        rv = self.client().post('/bloglists', data=self.bloglist)
        self.assertEqual(rv.status_code, 201)
        result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            '/bloglists/{}'.format(result_in_json['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Flask rest api with TDD', str(result.data))

    def test_bloglist_can_be_edited(self):
        """Test API can edit an existing bloglist. (PUT request)"""
        rv = self.client().post(
            '/bloglists',
            data={'name': 'Hosting static website in cloud'})
        self.assertEqual(rv.status_code, 201)
        rv = self.client().put(
            '/bloglists/1',
            data={
                "name": "Hosting static website in Azure storage"
            })
        self.assertEqual(rv.status_code, 200)
        results = self.client().get('/bloglists/1')
        self.assertIn('Hosting static website', str(results.data))

    def test_bloglist_deletion(self):
        """Test API can delete an existing bloglist. (DELETE request)."""
        rv = self.client().post(
            '/bloglists',
            data={'name': 'Hosting static website in cloud'})
        self.assertEqual(rv.status_code, 201)
        res = self.client().delete('/bloglists/1')
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client().get('/bloglists/1')
        self.assertEqual(result.status_code, 404)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()