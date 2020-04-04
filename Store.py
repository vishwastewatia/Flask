from flask_restful import Resource
from storeModel import StoreModel
from flask_jwt import jwt_required

class Store(Resource):
    def get(self, name):
        store=StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store Not Found'}, 404

    def post(self,name):
        if StoreModel.find_by_name(name):
            return {'message': "Store with name '{}' already exist".format(name)}, 400

        store = StoreModel(name,)
        try:
            store.save_to_db()
        except:
            return {'message':'An error occured'}, 500

        return store.json(),201

    @jwt_required()
    def delete(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        else:
            return {'message':'store Not Found'}, 404

        return {'message':'Store Deletd'}


class StoreList(Resource):
    def get(self):
        return {'store': list(map(lambda x: x.json(), StoreModel.query.all()))}
