from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate,identity
from user import UserRegister
from Item import Item, Item_list

app=Flask(__name__)
app.secret_key= 'devesh'
api=Api(app)

jwt=JWT(app, authenticate, identity) #/auth


api.add_resource(Item,'/item/<string:name>')
api.add_resource(Item_list,'/items')
api.add_resource(UserRegister,'/register')

if __name__=='__main__': ##when we import app file then __name__ is not equals to __main__ because main is th entire code
    app.run(port=4999,debug=True)
