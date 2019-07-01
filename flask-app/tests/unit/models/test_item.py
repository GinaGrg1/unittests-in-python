from tests.unit.unit_base_test import UnitBaseTest

from models.item import ItemModel


class ItemTest(UnitBaseTest):
    def test_create_item(self):
        item = ItemModel('Kathmandu', 44.56, 1)

        self.assertEqual(item.name, 'Kathmandu', "ERROR MSG: Not Equal")
        self.assertEqual(item.price, 44.56, "ERROR MSG: Not Equal")
        self.assertEqual(item.store_id, 1)
        self.assertIsNone(item.store)

    def test_item_json(self):

        item = ItemModel('Kathmandu', 44.56, 1)
        expected = {
            'name': 'Kathmandu',
            'price': 44.56
        }

        self.assertEqual(item.json(), expected, "The JSON export is incorrect. Received {}, expected {}"
                         .format(item.json(), expected))
