from werkzeug.security import safe_str_cmp
from user import User

###because we are using database therefor no mapping and in memory is required
# users=[
#     User(1, 'devesh', 'abcd')
# ]
#
# #it allows us to retrive user by its username and its id and we use mapping when we use in memory to store data
# username_mapping={u.username:u for u in users}
# userid_mapping={u.id:u for u in users}


def authenticate(username, password):
    user = User.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    user_id = payload['identity']
    return User.find_by_id(user_id)
