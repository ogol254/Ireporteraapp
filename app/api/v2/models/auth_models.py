from werkzeug.security import generate_password_hash, check_password_hash

from ....db_config import init_db
from base_model import BaseModel


class UserModel(BaseModel):
    """This class encapsulates the functions of the user model"""

    def __init__(self, username="user", first_name="first",
                 last_name="last", password="pass", email="em@ai.l"):
        """initialize the user model"""
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.password = generate_password_hash(password)
        self.email = email
        self.db = init_db()

    def get_user_by_username(self, username):
        """return user from the db given a username"""
        database = self.db
        curr = database.cursor()
        curr.execute(
            """SELECT user_id, first_name, last_name, password, username \
            FROM users WHERE username = '%s'""" % (username))
        data = curr.fetchone()
        curr.close()
        return data

    def check_exists(self, username):
        """Check if the records exist"""
        curr = self.db.cursor()
        query = "SELECT username FROM users WHERE username = '%s'" % (username)
        curr.execute(query)
        return curr.fetchone() is not None

    def save_user(self):
        """Add user details to the database"""
        user = {
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password,
            "isadmin": True
        }
        # check if user exists
        if self.check_exists(user['username']):
            return False
        database = self.db
        curr = database.cursor()
        query = """INSERT INTO users (first_name, last_name, username, email, password, is_admin) \
            VALUES ( %(first_name)s, %(last_name)s,\
            %(username)s, %(email)s, %(password)s, %(isadmin)s) RETURNING username;
            """
        curr.execute(query, user)
        username = curr.fetchone()[0]
        database.commit()
        curr.close()
        return ("{} saved sucessfully".format(username))
