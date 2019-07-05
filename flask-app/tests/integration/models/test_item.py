from models.item import ItemModel
from models.store import StoreModel
from tests.integration_base_test import BaseTest


class ItemTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            StoreModel('Kathmandu').save_to_db()  # Save to stores table.
            item = ItemModel('Kathmandu', 44.56, 1)

            # First make sure the item does not exist in the db before saving.
            self.assertIsNone(ItemModel.find_by_name('Kathmandu'),
                              f"Found an item with name {item.name}, but expected not to.")

            item.save_to_db()
            self.assertIsNotNone(ItemModel.find_by_name('Kathmandu'))

            item.delete_from_db()
            self.assertIsNone(ItemModel.find_by_name('Kathmandu'))

    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel('test_store')
            item = ItemModel('Kathmandu', 44.56, 1)

            store.save_to_db()
            item.save_to_db()

            self.assertEqual(item.store.name, 'test_store')
