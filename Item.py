import sqlite3
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                type=float,
                required=True,
                help='this field can not be left blank'
                )
    @jwt_required()
    def get(self,name):

# #        for item in items:
# #           if item['name'] == name:
# #using lambda function instead
#         item=next(filter(lambda x:x['name'] == name,items),None)
#         return {'item':item},200 if item else 404  ##no longer required because we will be storing it into database

        item=self.find_by_name(name)
        if item:
            return item
        return {'message':'item does not exist'}


    @classmethod
    def find_by_name(cls,name):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:  # means if row is not none
            return {'item': {'name': row[0], 'price': row[1]}}

    def post(self,name):

        if Item.find_by_name(name):
            return {'message':"An item with name'{}'already exist.".format(name)},400

        data=Item.parser.parse_args()
        item={'name':name,'price':data['price']}

        connection=sqlite3.connect("data.db")
        cursor=connection.cursor()
        query="INSERT INTO items VALUES(?,?)"
        cursor.execute(query,(item['name'],item['price']))

        connection.commit()
        connection.close()

        return item,201

    @jwt_required()
    def delete(self,name):
        global items
        items=list(filter(lambda x:x['name'] != name, items))
        return {'message':'item deleted'}

    def put(self,name):
        data=Item.parser.parse_args()
        item = next(filter(lambda x:x['name'] == name,items),None)
        if item is None:
            item = {'name':name,'price':data['price']}
            items.append(item)
        else:
            item.update(data)
        return item

class Item_list(Resource):
    def get(self):
        return {'items':items}
