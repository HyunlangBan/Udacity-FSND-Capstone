import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Restaurant, Reservation, Customer


class RerservationServiceTestCase(unittest.TestCase):

    def setUp(self):
        self.client = self.app.test_client
        self.database_path = os.environ.get('HEROKU_POSTGRESQL_MAROON_URL')
        setup_db(self.app, self.database_path)

        self.new_rest = {
            'name': 'test_rest',
            'address': 'test_address',
            'category': 'test_category',
            'photo': 'https://example.com',
            'tel': '231-423-5234',
            'menu': '{test1, test2}',
            'capacity': 10,
            'open_time': '10:00:00',
            'close_time': '20:00:00'
        }

        self.edit_rest = {
            'name': 'edit_rest1',
            'address': 'edit_address',
            'category': 'edit_category',
            'photo': 'https://example.com',
            'tel': '111-111-1111',
            'menu': '{edit1, edit2}',
            'capacity': 10,
            'open_time': '10:00:00',
            'close_time': '20:00:00'
        }

        self.new_reservation = {
            'email': 'eamil@eamil.com',
            'name': 'edit_rest1',
            'rest_id': 1,
            'customer_id': 1,
            'number': 3,
            'time': '2020-12-20 12:00:00'
        }

        self.new_customer = {
            'name': 'new customer',
            'phone': '131-1413-1414',
            'email': 'new@email.com'
        }

        self.customer_auth_header = {'Authorization': "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ikt1QzhKTEQtVFVkZVpCTzJmbWpxRiJ9.eyJpc3MiOiJodHRwczovL2hyYmFuLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWExMWJmNDA0NGFhNDBjOGVkNDY1MDMiLCJhdWQiOiJyZXNlcnZhdGlvbiIsImlhdCI6MTU4Nzk5OTE0NiwiZXhwIjoxNTg4MDg1NTQ2LCJhenAiOiJ4bkRVTk92ajlwOUhBa3FITHZGYWJmaDV6dXdhdDl1USIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZWRpdDpjdXN0b21lciIsImVkaXQ6cmVzZXJ2YXRpb24iLCJnZXQ6cmVzZXJ2YXRpb25zIiwiZ2V0OnJlc3RhdXJhbnQiLCJnZXQ6cmVzdGF1cmFudHMiLCJtYWtlOnJlc2VydmF0aW9uIiwicG9zdDpjdXN0b21lciIsInBvc3Q6cmV2aWV3Iiwic2VhcmNoOnJlc3RhdXJhbnRzIl19.mQ9uivHAnOewY4HrlNfq04xcQw_h_FqH7XamYBJ49fBRqcehHaiEBT-19OIZyeU2DfWooqa0f59JncY1tMVvQoXqcuKAavCrehhsg3L9GuFbKdUSELos-FHvbh6pxRz5LDsHwLhkPA8A7zfa7wIsHCdHOntrRNrPGRuMPFHaSiKCK9O5MH8QYRWxX-byYOL4W_ILmrmrcBEOpXlrGp50SObY0vI3YP413gyJibOkCalL22WGVtubHuhRckOxHSdn3co8VA93TD8quiW6OG2XVOHKc8fOpdJvP4wvTbk0kDJtQPZqP5L5vsDPnBhR-7AbkfiMGwoiuvAOXVw89o5ERg"}
        self.admin_auth_header = {'Authorization': "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ikt1QzhKTEQtVFVkZVpCTzJmbWpxRiJ9.eyJpc3MiOiJodHRwczovL2hyYmFuLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWExMWM1MTA4Y2ExMDBjNmRlYTBhOTciLCJhdWQiOiJyZXNlcnZhdGlvbiIsImlhdCI6MTU4Nzk5ODA5MSwiZXhwIjoxNTg4MDg0NDkxLCJhenAiOiJ4bkRVTk92ajlwOUhBa3FITHZGYWJmaDV6dXdhdDl1USIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiY2hlY2s6cmVzZXJ2YXRpb25zIiwiZGVsZXRlOmN1c3RvbWVyIiwiZGVsZXRlOnJlc3RhdXJhbnQiLCJlZGl0OmN1c3RvbWVyIiwiZWRpdDpyZXNlcnZhdGlvbiIsImVkaXQ6cmVzdGF1cmFudCIsImdldDpyZXNlcnZhdGlvbnMiLCJnZXQ6cmVzdGF1cmFudCIsImdldDpyZXN0YXVyYW50cyIsIm1ha2U6cmVzZXJ2YXRpb24iLCJwb3N0OmN1c3RvbWVyIiwicG9zdDpyZXN0YXVyYW50cyIsInBvc3Q6cmV2aWV3Iiwic2VhcmNoOnJlc3RhdXJhbnRzIl19.hmuzam9BYPT7DV6GY5PVJywl0tnMt5rG7MZrREIzUjAebvxEiHqQC6wG2aB_LXQc5KwaE6wZb5B5QezVpT0Wg0PsBex_y0OqYFxKVe0W97og4Av7AmKmMlbP7OYTs4hvwF-alihFXosODhEWN2Evi70WN1f7k6HfEEn57B4BqN8NRK1TjBat5GdVuXXn76qDiZs606dRT-LamcnSYBTSUizUhRjQoHheBpPSI5204hGVuNkrjqzrDBMX_89aXTNXi2KcnS41RmPnf1Gw6bj5ULHKGPkPgKCzFXAv1mzoEkavJhUVTlRS739K67FemaspTmwIAWfng-aw82pO4bwH7g"}
        self.owner_auth_header = {'Authorization': "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ikt1QzhKTEQtVFVkZVpCTzJmbWpxRiJ9.eyJpc3MiOiJodHRwczovL2hyYmFuLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWExMWMzYjA0NGFhNDBjOGVkNDY1ODciLCJhdWQiOiJyZXNlcnZhdGlvbiIsImlhdCI6MTU4Nzk4MzMxMiwiZXhwIjoxNTg4MDY5NzEyLCJhenAiOiJ4bkRVTk92ajlwOUhBa3FITHZGYWJmaDV6dXdhdDl1USIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiY2hlY2s6cmVzZXJ2YXRpb25zIiwiZWRpdDpyZXN0YXVyYW50IiwiZ2V0OnJlc3RhdXJhbnRzIiwicG9zdDpyZXN0YXVyYW50cyJdfQ.SPAUU0NlsAdXBM31qqGnRdJsJvpDsX3QpO4SFTa0S8DgZSKpUhRz8cps2Q5-TqxhcvpPOAWN5_42T5YfpuVeDVTCUSoAAuX6Mm1XOWeZEJhCHtAtWwiDxc6HKjLC6UDf834ZB_eqPz4YkzaUEeYv90XdFHZjAmvDC3bzFxukiu0mBPfEendYZciMNLKLmis6SSzhOPmndh_TQc_nKkHJGYjvYtSXGBryLXNfLQZggCduOb-GicKcD17HE5C-FD99xqPDB2eGuu5YSfPhUaf38dh3x-0As9UPbBcQu8xgldFnyZuURapvS0SvgHv8yY4kZKnf45Dq7voZQjLLWw2s4w"}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            # self.db.create_all()

    def tearDown(self):
        pass

    def test_admin_get_restaurants_list(self):
        res = self.client().get('/restaurants', headers=self.admin_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['restaurants'])
        self.assertTrue(data['total_restaurants'])

    def test_customer_get_restaurants_list(self):
        res = self.client().get('/restaurants', headers=self.customer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['restaurants'])
        self.assertTrue(data['total_restaurants'])

    def test_no_auth_get_restaurants_list(self):
        res = self.client().get('/restaurants')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_customer_create_restaurant(self):
        res = self.client().post('/restaurants/create', json=self.new_rest,
                                 headers=self.customer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_owner_create_restaurant(self):
        res = self.client().post('/restaurants/create', json=self.new_rest,
                                 headers=self.owner_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['current_restaurants'])
        self.assertTrue(data['total_restaurants'])
        self.assertTrue(data['result'])

    def test_owner_get_restaurant(self):
        res = self.client().get('/restaurants/1', headers=self.owner_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_customer_get_restaurant(self):
        res = self.client().get('/restaurants/1', headers=self.customer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['restaurant'])
        self.assertTrue(data['rest_id'])

    def test_owner_delete_restaurant(self):
        res = self.client().delete('/restaurants/2', headers=self.owner_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_customer_delete_restaurant(self):
        res = self.client().delete('/restaurants/2', headers=self.customer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_admin_delete_restaurant(self):
        res = self.client().delete('/restaurants/2', headers=self.admin_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['current_restaurants'])
        self.assertTrue(data['total_restaurants'])
        self.assertTrue(data['deleted'])

    def test_customer_edit_restaurant(self):
        res = self.client().patch('/restaurants/1/edit', json=self.edit_rest,
                                  headers=self.customer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_owner_edit_restaurant(self):
        res = self.client().patch('/restaurants/1/edit', json=self.edit_rest,
                                  headers=self.owner_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['current_restaurants'])
        self.assertTrue(data['edited'])

    def test_owner_search_restaurant(self):
        res = self.client().post('/restaurants/search?searchTerm=rest',
                                 headers=self.owner_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_customer_search_restaurant(self):
        res = self.client().post('/restaurants/search?searchTerm=rest',
                                 headers=self.customer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['current_restaurants'])
        self.assertTrue(data['total_restaurants'])

    def test_customer_create_reservation(self):
        res = self.client().post('/reservations/create?customer_email=email@email.com&rest_name=rest1',
                                 json=self.new_reservation, headers=self.customer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['reservation_detils'])

    def test_owner_create_reservation(self):
        res = self.client().post('/reservations/create?customer_email=email@email.com&rest_name=rest1',
                                 json=self.new_reservation, headers=self.owner_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_owner_get_reservations(self):
        res = self.client().get('/reservations/1', headers=self.owner_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_customer_get_reservation(self):
        res = self.client().get('/reservations/1', headers=self.customer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['past_reservations'])
        self.assertTrue(data['upcoming_reservations'])

    def test_owner_check_reservation(self):
        res = self.client().get('/reservations/1/owner', headers=self.owner_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['past_reservations'])
        self.assertTrue(data['upcoming_reservations'])

    def test_customer_check_reservations(self):
        res = self.client().get('/reservations/1/owner', headers=self.customer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_customer_post_review(self):
        res = self.client().patch('/reservations/1/review',
                                  json={'review': 'Good Day!'}, headers=self.customer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['reservation'])

    def test_owner_post_review(self):
        res = self.client().patch('/reservations/1/review',
                                  json={'review': 'Good Day!'}, headers=self.owner_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_owner_edit_reservation(self):
        res = self.client().patch('/reservations/1/edit',
                                  json={'number': 5}, headers=self.owner_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_customer_edit_reservation(self):
        res = self.client().patch('/reservations/1/edit',
                                  json={'number': 5, 'time': '2020-08-15 17:00:00'}, headers=self.customer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['reservation'])

    def test_customer_create_customer(self):
        res = self.client().post('/customers/create', json=self.new_customer,
                                 headers=self.customer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['customer'])

    def test_owner_create_customer(self):
        res = self.client().post('/customers/create', json=self.new_customer,
                                 headers=self.owner_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_owner_edit_customer(self):
        res = self.client().post('/customers/1/edit',
                                 json={'name': 'John', 'phone': '111-111-1111', 'email': 'json@email.com'}, headers=self.owner_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_customer_edit_customer(self):
        res = self.client().post('/customers/1/edit',
                                 json={'name': 'John', 'phone': '111-111-1111', 'email': 'json@email.com'}, headers=self.customer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['customer'])

    def test_customer_delete_customer(self):
        res = self.client().delete('/customers/1', headers=self.customer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_admin_delete_customer(self):
        res = self.client().delete('/customers/2', headers=self.admin_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])


# Error Hadling

    def test_404_if_restarant_does_not_exist(self):
        res = self.client().get('/restaurants/100', headers=self.admin_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    def test_404_if_restaurant_id_is_not_valid(self):
        res = self.client().delete('/restaurants/400', headers=self.admin_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    def test_404_if_reservation_does_not_exist(self):
        res = self.client().get('/reservations/100', headers=self.admin_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    def test_404_if_reservations_for_owner_does_not_exist(self):
        res = self.client().get('/reservations/100/owner', headers=self.admin_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    def test_404_if_email_is_not_valid(self):
        res = self.client().post('/reservation/create',
                                 json={'email': 'uuuu'}, headers=self.admin_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    def test_404_if_name_is_not_valid(self):
        res = self.client().post('/reservation/create',
                                 json={'email': 'john@email.com', 'name': 'error'}, headers=self.admin_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    def test_404_if_name_is_not_valid(self):
        res = self.client().patch('/reservation/300/create',
                                  json={'number': 5, 'time': '2020-08-15 17:00:00'}, headers=self.admin_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    def test_405_if_restaurant_deletion_not_allowed(self):
        res = self.client().delete('/restaurants', headers=self.admin_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)

    def test_422_if_restaurants_creation_failed(self):
        res = self.client().post('/restaurants/create', headers=self.admin_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)

    def test_401_auth_error(self):
        res = self.client().post('/restaurants/create')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
