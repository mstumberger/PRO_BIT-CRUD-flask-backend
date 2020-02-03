from flask_restful import Resource, reqparse
from models import User, Car, RevokedTokenModel
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)

parser = reqparse.RequestParser()
parser.add_argument('username', help='This field cannot be blank', required=True)
parser.add_argument('password', help='This field cannot be blank', required=True)
parser.add_argument('email', help='This field cannot be blank', required=True)


class UserRegistration(Resource):
    def post(self):
        data = parser.parse_args()
        
        if User.find_by_email(data['email']):
            return {'message': 'User {} already exists'.format(data['username'])}
        
        new_user = User(
            username=data['username'],
            password=User.generate_hash(data['password']),
            email=data['email'],
        )
        
        try:
            new_user.save_to_db()
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                'message': 'User {} was created'.format(data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token
                }
        except Exception as e:
            return {'message': 'Something went wrong', 'exception': e}, 500


class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()
        current_user = User.find_by_username(data['username'])

        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}
        
        if User.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity = data['username'])
            refresh_token = create_refresh_token(identity = data['username'])
            return {
                'message': 'Logged in as {}'.format(current_user.username),
                'access_token': access_token,
                'refresh_token': refresh_token
                }
        else:
            return {'message': 'Wrong credentials'}


class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'access_token': access_token}


class AllUsers(Resource):
    def get(self):
        return User.return_all()
    
    def delete(self):
        return User.delete_all()


car_parser = reqparse.RequestParser()
car_parser.add_argument('maker', help='This field cannot be blank', required=True)
car_parser.add_argument('model', help='This field cannot be blank', required=True)
car_parser.add_argument('fuelType', help='This field cannot be blank', required=True)
car_parser.add_argument('transmission', help='This field cannot be blank', required=True)
car_parser.add_argument('description', help='This field cannot be blank', required=True)


class AddCar(Resource):
    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        data = car_parser.parse_args()
        print(current_user, data)

        # current_user = User.find_by_username(data['username'])
        new_car = Car(
            maker=data['maker'],
            model=data['model'],
            fuel_type=data['fuelType'],
            transmission=data['transmission'],
            description=data['description'],
            user_id=User.find_by_username(current_user).id
        )

        try:
            new_car.save_to_db()
            return {
                'message': 'Car {} {} was added. ID: {}'.format(new_car.maker, new_car.model, new_car.id),
            }
        except Exception as e:
            return {'message': 'Something went wrong', 'exception': e}, 500


class AllCars(Resource):
    def get(self):
        return Car.return_all()

    def delete(self):
        return Car.delete_all()


class SecretResource(Resource):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        return {
            'answer': 42,
            'user': current_user
        }