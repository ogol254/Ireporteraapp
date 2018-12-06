from ....db_config import init_db
from .base_model import BaseModel


class IncidentModel(BaseModel):
    """This class encapsulates the functions of the user model"""

    def __init__(self, created_by="created_by", incident_type="incident_type",
                 description="description", status="status", location="location"):
        """initialize the user model"""
        self.created_by = created_by
        self.incident_type = incident_type
        self.description = description
        self.status = status
        self.location = location
        self.db = init_db()

    def get_specific_incident(self, incident_id):
        """return an incident from the db given a id"""
        database = self.db
        curr = database.cursor()
        curr.execute(
            """SELECT incident_id, created_by, description, type, status, location, created_on \
            FROM incidents WHERE incident_id = '%s'""" % (incident_id))
        data = curr.fetchone()
        if data:
            incident = dict(
                incident_id=int(data[0]),
                created_by=data[1],
                incident_type=data[3],
                description=data[2],
                status=data[4],
                location=data[5],
                created_on=str(data[6])
            )
            return incident
            curr.close()
        else:
            return "Incident does not exists"

    def save_incident(self):
        """Add incident details to the database"""
        incident = {
            "created_by": self.created_by,
            "description": self.description,
            "type": self.incident_type,
            "status": self.status,
            "location": self.location
        }
        # check if incident exists
        if BaseModel().check_exists(table="incidents", field="description", data=incident['description']):
            return False
        database = self.db
        curr = database.cursor()
        query = """INSERT INTO incidents (created_by, description, type, status, location) \
            VALUES ( %(created_by)s, %(description)s,\
            %(type)s, %(status)s, %(location)s) RETURNING incident_id;
            """
        curr.execute(query, incident)
        incident_id = curr.fetchone()[0]
        database.commit()
        curr.close()
        return incident_id

    def get_all_incidents_by_user(self, created_by):
        """return all incidents from the db given a username"""
        database = self.db
        curr = database.cursor()
        curr.execute(
            """SELECT incident_id, description, type, status, location, created_on \
            FROM incidents WHERE created_by = '%s'""" % (created_by))
        data = curr.fetchall()
        resp = []

        for i, items in enumerate(data):
            incident_id, description, type, status, location, created_on = items
            incidents = dict(
                incident_id=int(incident_id),
                type=type,
                description=description,
                status=status,
                location=location,
                created_on=created_on
            )
            resp.append(incidents)
        return resp

    def get_all_incidents(self):
        """return all incidents from the db """
        database = self.db
        curr = database.cursor()
        curr.execute("""SELECT incident_id, description, created_by, type, status, location, created_on FROM incidents ;""")
        data = curr.fetchall()
        resp = []

        for i, items in enumerate(data):
            incident_id, description, created_by, type, status, location, created_on = items
            incidents = dict(
                incident_id=int(incident_id),
                created_by=created_by,
                incident_type=type,
                description=description,
                status=status,
                location=location,
                created_on=str(created_on)

            )
            resp.append(incidents)
        return resp
