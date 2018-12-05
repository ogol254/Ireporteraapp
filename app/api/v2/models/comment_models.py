

from ....db_config import init_db
from base_model import BaseModel


class CommentModel(BaseModel):
    """This class encapsulates the functions of the user model"""

    def __init__(self, created_by="created_by", incident_id="incident_id",
                 comment="comment"):
        """initialize the user model"""
        self.created_by = created_by
        self.incident_id = incident_id
        self.comment = comment
        self.db = init_db()

    def check_comment_exists(self, comment):
        """Check if the records exist"""
        curr = self.db.cursor()
        query = "SELECT comment FROM comments WHERE comment = '%s'" % (comment)
        curr.execute(query)
        return curr.fetchone() is not None

    def save_comment(self):
        """Add incident details to the database"""
        comment = {
            "created_by": self.created_by,
            "incident_id": self.incident_id,
            "comment": self.comment,
        }
        # check if incident exists
        in_exist = BaseModel().check_item_exists(table="incidents", field="incident_id", data=comment['incident_id'])

        if (in_exist == True):
            if self.check_comment_exists(comment['comment']):
                return False
            else:
                database = self.db
                curr = database.cursor()
                query = """INSERT INTO comments (created_by, incident_id, comment) \
                    VALUES ( %(created_by)s, %(incident_id)s, %(comment)s) RETURNING comment_id;
                    """
                curr.execute(query, comment)
                comment_id = curr.fetchone()[0]
                database.commit()
                curr.close()
                return "Comment saved successfully"

        else:
            return "No incident with an ID of {}".format(comment['incident_id'])

    def get_all_comments_by_incident(self, incident_id):
        """return all incidents from the db given a username"""
        database = self.db
        curr = database.cursor()
        curr.execute(
            """SELECT comment_id, created_by, comment, date_created \
            FROM comments WHERE incident_id = '%s'""" % (incident_id))
        data = curr.fetchall()
        resp = []

        for i, items in enumerate(data):
            comment_id, created_by, comment, date_created = items
            comments = dict(
                incident_id=int(incident_id),
                comment_id=int(comment_id),
                created_by=created_by,
                comment=comment,
                date_created=str(date_created)
            )
            resp.append(comments)
        return resp
