"""
This module defines the base model and associated functions
"""
from datetime import datetime, timedelta
import jwt
import os

from ....db_config import init_db


class BaseModel(object):
    """
    This class encapsulates the functions of the base model
    that will be shared across all other models
    """

    def __init__(self):
        """initialize the database"""
        self.db = init_db()

    def update_item(self, table, field, data, item_field, item_id):
        """update the field of an item given the item_id"""

        dbconn = self.db
        curr = dbconn.cursor()
        updated = curr.execute("UPDATE {} SET {}='{}' \
                     WHERE {} = {} ;".format(table, field, data, item_field, item_id))
        dbconn.commit()
        if updated:
            return True

    def delete_item(self, table_name, field, field_value):
        """delete the field of an item given the item_id"""

        dbconn = self.db
        curr = dbconn.cursor()
        query = "DELETE FROM {} WHERE {}={};".format(table_name, field, field_value)
        updated = curr.execute(query)
        dbconn.commit()
        if updated:
            return True

    def check_item_exists(self, table, field, data):
        """Check if the records exist"""
        curr = self.db.cursor()
        query = "SELECT * FROM {} WHERE {}={};".format(table, field, data)
        curr.execute(query)
        data = curr.fetchone()
        if data:
            return True
        else:
            return False

    @staticmethod
    def encode_auth_token(user_id):
        """Function to generate Auth token
        """
        # import pdb;pdb.set_trace()
        try:
            payload = {
                "exp": datetime.utcnow() + timedelta(days=1),
                "iat": datetime.utcnow(),
                "sub": user_id
            }
            token = jwt.encode(
                payload,
                os.getenv("SECRET_KEY"),
                algorithm="HS256"
            )
            resp = token
        except Exception as e:
            resp = e

        return resp

    def blacklisted(self, token):
        dbconn = self.db
        curr = dbconn.cursor()
        query = """
                SELECT * FROM blacklist WHERE tokens = %s;
                """
        curr.execute(query, [token])
        if curr.fetchone():
            return True
        return False

    def decode_auth_token(self, auth_token):
        """This function takes in an auth
        token and decodes it
        """
        if self.blacklisted(auth_token):
            return "Token has been blacklisted"
        secret = os.getenv("SECRET_KEY")
        try:
            payload = jwt.decode(auth_token, secret)
            return payload['sub']  # user id
        except jwt.ExpiredSignatureError:
            return "The token has expired"
        except jwt.InvalidTokenError:
            return "The token is invalid"

    def _type(self):
        """returns the name of the inheriting class"""
        return self.__class__.__name__

    def close_db(self):
        """This function closes the database"""
        self.db.close()
        pass
