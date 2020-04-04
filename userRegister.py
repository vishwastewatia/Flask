import psycopg2 as pg2
from flask_restful import Resource,reqparse
from user import UserModel


class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username', type = str, required= True,
                         help='This filed can''t be blank'
                        )
    parser.add_argument('password', type = str, required= True,
                         help='This filed can''t be blank'
                        )

    def post(self):
        data= UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'User already exist'},400

        user= UserModel(data['username'], data['password'])
        UserModel.save_to_db(user)


        return {'message':'User created Sucessfully'},201
        
