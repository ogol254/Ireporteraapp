friends_list = []


class MyFriendsModel():
    """docstring for MyFriendsModel"""

    def __init__(self):
        self.db = friends_list

    def save(self, name, email, password):
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
