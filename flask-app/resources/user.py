from flask_restful import Resource, reqparse

from models.user import UserModel


class UserRegister(Resource):
    """
    This Resource allows users to register by sending a POST request
    with their username and password.
    """
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="username cannot be blank")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="password cannot be blank.")

    def post(self):
        data = UserRegister.parser.parse_args()

        # Check if the username already exists.
        if UserModel.find_by_username(data['username']):
            return {
                'message': 'A user with that username already exists'
            }, 400

        user = UserModel(**data)
        user.save_to_db()

        return {
            'message': 'User created successfully.'
        }, 201
