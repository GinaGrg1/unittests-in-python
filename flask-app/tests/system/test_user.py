import json

from models.user import UserModel
from tests.base_test import BaseTest


class UserTest(BaseTest):
    def test_register_user(self):
        with self.app() as client:
            with self.app_context():
                request = client.post('/register', data={'username': 'gurung', 'password': 'abcde'})

                self.assertEqual(request.status_code, 201)
                self.assertIsNone(UserModel.find_by_username('gurung'))
                self.assertDictEqual({'message': 'User created successfully.'}, json.loads(request.data))

    def test_register_and_login(self):
        pass

    def test_register_duplicate_user(self):
        pass
