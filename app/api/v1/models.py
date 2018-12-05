usres_list = []


class UsersModel():
    """docstring for MyFriendsModel"""

    def __init__(self):
        self.db = usres_list

    def save(self, name, email, password):
        is_valid = self.user_validator(name)

        if is_valid == True:
            return 'User already exist'
        else:

            data = {
                "name": name,
                "id": len(self.db) + 1,
                "email": email,
                "password": password
            }

            self.db.append(data)

            return self.db

    def get_friends(self):
        return self.db

    def get_single_user(self, id):
        for user in self.db:
            if (user['id'] == id):
                return user
            else:
                return "No such user"

    def user_validator(name):
        for user in self.db:
            if (name == user['name']):
                return True
            else:
                return False
