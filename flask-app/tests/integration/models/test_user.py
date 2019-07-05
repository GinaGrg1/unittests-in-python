from models.user import UserModel
from tests.base_test import BaseTest


class UserTest(BaseTest):
    def test_crud(self):
        with self.app_context():  # since we are hitting the database
            user = UserModel("gurung", "abcde")

            # First make sure the username & the user_id does not exist
            self.assertIsNone(UserModel.find_by_username("gurung"))
            self.assertIsNone(UserModel.find_by_id(1))

            # Save to database
            user.save_to_db()

            # Check that the username & user_id now exist
            self.assertIsNotNone(UserModel.find_by_username("gurung"))
            self.assertIsNotNone(UserModel.find_by_id(1))

