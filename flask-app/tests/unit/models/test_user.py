from models.user import UserModel
from tests.unit.unit_base_test import UnitBaseTest


class UserTest(UnitBaseTest):
    def test_create_user(self):
        user = UserModel('gurung', 'abcde')

        self.assertEqual(user.username, 'gurung', "ERROR: Username does not match.")
        self.assertEqual(user.password, 'abcde', "ERROR: Password does not match.")
