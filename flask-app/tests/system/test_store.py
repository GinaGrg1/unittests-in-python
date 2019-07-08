import json

from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest


class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/store/McDonalds')

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name('McDonalds'))
                self.assertDictEqual({'id':1, 'name': 'McDonalds', 'items': []}, json.loads(response.data))

    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/McDonalds')
                response = client.post('/store/McDonalds')

                self.assertEqual(response.status_code, 400)

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('McDonalds').save_to_db()  # First save to db
                response = client.delete('/store/McDonalds')

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'message': 'Store deleted'}, json.loads(response.data))

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('McDonalds').save_to_db()
                response = client.get('/store/McDonalds')
                #print(response.data)
                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'id': 1, 'name': 'McDonalds', 'items': []}, json.loads(response.data))

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/store/McDonalds')

                self.assertEqual(response.status_code, 404)

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('McDonalds').save_to_db()
                ItemModel('McDonalds', 19.99, 1).save_to_db()

                response = client.get('/store/McDonalds')
                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'id': 1, 'name': 'McDonalds', 'items': [{'name': 'McDonalds', 'price': 19.99}]},
                                     json.loads(response.data))

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('McDonalds').save_to_db()

                response = client.get('/stores')
                self.assertDictEqual({'stores': [{'id': 1, 'name': 'McDonalds', 'items': []}]},
                                     json.loads(response.data))

    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('McDonalds').save_to_db()
                ItemModel('McDonalds', 19.99, 1).save_to_db()

                response = client.get('/stores')

                self.assertDictEqual({'stores': [{'id': 1, 'name': 'McDonalds', 'items': [{'name': 'McDonalds', 'price': 19.99}]}]},
                                     json.loads(response.data))
