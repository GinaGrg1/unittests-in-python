from models.store import StoreModel
from models.user import UserModel
from models.item import ItemModel
from tests.base_test import BaseTest

import json


class ItemTest(BaseTest):
    def setUp(self):
        # Runs before every test.
        super(ItemTest, self).setUp()  # Use the setUp() of the super class, BaseTest.
        with self.app() as client:
            with self.app_context():
                UserModel('gurung', 'abcde').save_to_db()
                auth_request = client.post('/auth',
                                           data=json.dumps({'username': 'gurung', 'password': 'abcde'}),
                                           headers={'Content-Type': 'application/json'})
                auth_token = json.loads(auth_request.data)['access_token']
                self.access_token = f'JWT {auth_token}'

    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/item/McDonalds')
                self.assertEqual(response.status_code, 401)

    def test_get_item_not_found(self):
        # headers={'WWW-Authenticate': 'JWT realm="%s"' % realm}
        # Authorization is required in all the GET requests.
        with self.app() as client:
            with self.app_context():
                response = client.get('/item/McDonalds', headers={'Authorization': self.access_token})

                self.assertEqual(response.status_code, 404)

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('McDonalds', 19.99, 1).save_to_db()

                response = client.get('/item/McDonalds', headers={'Authorization': self.access_token})

                self.assertEqual(response.status_code, 200)

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('McDonalds', 19.99, 1).save_to_db()

                response = client.delete('/item/test')

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({
                    'message': 'Item deleted'
                }, json.loads(response.data))

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('junk-food').save_to_db()

                response = client.post('/item/junk-food', data={'price': 17.99, 'store_id': 1})

                self.assertEqual(response.status_code, 201)
                self. assertDictEqual({'name': 'junk-food', 'price': 17.99},
                                      json.loads(response.data))

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('junk-food').save_to_db()
                ItemModel('junk-food', 17.99, 1).save_to_db()

                response = client.post('/item/junk-food', data={'price': 17.99, 'store_id': 1})

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({'message': 'An item with name \'junk-food\' already exists.'},
                                     json.loads(response.data))

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('junk-food').save_to_db()
                response = client.put('/item/junk-food', data={'price': 17.99, 'store_id': 1})

                self.assertEqual(response.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('junk-food').price, 17.99)
                self.assertDictEqual({'name': 'junk-food', 'price': 17.99},
                                     json.loads(response.data))

    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('junk-food').save_to_db()
                ItemModel('junk-food', 6.99, 1)  # create item with different price.
                response = client.put('/item/junk-food', data={'price': 17.99, 'store_id': 1})

                self.assertEqual(response.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('junk-food').price, 17.99)
                self.assertDictEqual({'name': 'junk-food', 'price': 17.99},
                                     json.loads(response.data))

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('junk-food').save_to_db()
                ItemModel('junk-food', 6.99, 1).save_to_db()

                response = client.get('/items')

                self.assertDictEqual({'items': [{'name': 'junk-food', 'price': 6.99}]},
                                     json.loads(response.data))


