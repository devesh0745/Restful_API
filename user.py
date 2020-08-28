import sqlite3
from flask_restful import Resource,reqparse

# for logging in
class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls,username):
        connection=sqlite3.connect("data.db")
        cursor=connection.cursor()

        query="SELECT * FROM users WHERE username=?"
        result=cursor.execute(query, (username,))
        row=result.fetchone()
        if row is not None:
            # user=User(row[0],row[1],row[2])
            user= cls(*row)

        else:
            user= None

        connection.close()
        return user


    @classmethod
    def find_by_id(cls,id):
        connection=sqlite3.connect('data.db')
        cursor=connection.cursor()

        query="SELECT * FROM users WHERE id=?"
        result=cursor.execute(query,(id,))
        row=result.fetchone()
        if row is not None:
            # user=User(row[1],row[2],row[3])
            user=cls(*row)
        else:
            user=None
        connection.close()
        return user

# for sign up
class UserRegister(Resource):

    parser=reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="this field cannot be blank"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="this field cannot be blank"
                        )

    def post(self):
        data=UserRegister.parser.parse_args()

        if User.find_by_username(data['username']) is not None:
            return {'message':'this username already exist'}
        connection=sqlite3.connect("data.db")
        cursor=connection.cursor()

        query="INSERT INTO users VALUES(NULL,?,?)"
        cursor.execute(query,(data['username'],data['password']))

        connection.commit()
        connection.close()

        return {'message':'user created successfully'},201