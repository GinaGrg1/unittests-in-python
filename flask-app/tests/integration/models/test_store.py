from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest


class StoreTest(BaseTest):
    def test_create_store_items_empty(self):
        store = StoreModel('test')

        self.assertListEqual(store.items.all(), [],
                             "ERROR: store table is not empty")

    def test_crud(self):
        with self.app_context():  # This comes from BaseTest
            store = StoreModel('test')

            # First check that 'test' doesn't exist
            self.assertIsNone(StoreModel.find_by_name('test'))

            store.save_to_db()
            # Check that it exists, so should not return None
            self.assertIsNotNone(StoreModel.find_by_name('test'))

            store.delete_from_db()
            # Check it doesn't exist
            self.assertIsNone(StoreModel.find_by_name('test'))

    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel('test')
            item = ItemModel('Kathmandu', 44.56, 1)

            store.save_to_db()
            item.save_to_db()

            self.assertEqual(store.items.count(), 1)
            self.assertEqual(store.items.first().name, 'Kathmandu')  # store is an object here.

    def test_store_json(self):
        store = StoreModel('test')
        expected = {
            'name': 'test',
            'items': []
        }

        self.assertDictEqual(store.json(), expected, "ERROR: Not Equal!")

    def test_store_json_with_item(self):
        with self.app_context():
            store = StoreModel('test')
            item = ItemModel('Kathmandu', 44.56, 1)

            store.save_to_db()
            item.save_to_db()

            expected = {
                'name': 'test',
                'items': [{'name': 'Kathmandu', 'price': 44.56}]
            }

            self.assertDictEqual(store.json(), expected, "ERROR: Items not equal.")

