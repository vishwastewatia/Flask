from flask import request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import psycopg2 as pg2
from itemModel import ItemModel

class Item(Resource):
    # by defining parser here we can use it anywhere now it belongs to Item class
    parser = reqparse.RequestParser()
    parser.add_argument('price', type = float, required= True,
                         help='This filed can''t be blank'
                       )
    parser.add_argument('store_id', type = int, required= False,
                         help='every item need a store '
                       ) 

    @jwt_required()                 #decorator for awt for authorization 
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message':'Item Not Found'},404
            
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "Item with name '{}' already exist".format(name)}, 400

        data= Item.parser.parse_args()          #using parser to check input
        item = ItemModel(name, data['price'], data['store_id'])
        try:
            item.save_to_db()
        except:
            return{'message':'An error accured during insert'},500  #internal server error=500     
        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            ItemModel.delete_from_db(item)
        return {'message': 'Item Deleted'}

    def put(self, name):
        
        data= Item.parser.parse_args()
        
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']

        ItemModel.save_to_db(item)
        return item.json()

   

class ItemList(Resource):
    def get(self):               
        return {'item':[item.json() for item in ItemModel.query.all()]}
