from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from userRegister import UserRegister
from Security import authenticate, identity
from item import Item,ItemList
from Store import Store, StoreList
from db import db

app= Flask(__name__)
DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user='postgres',pw='postgre',url='127.0.0.1',db='flask')
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATION']= False
app.secret_key = 'jose'
api = Api(app)

'''
#Create all tables before first request call
@app.before_first_request
def create_tables():
    db.create_all()
'''
jwt = JWT(app, authenticate, identity)  #/auth          it create default endpoint /auth

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/store')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port= 5100, debug=True)
