from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma
import uuid

from db import db

class Locations(db.Model):
    __tablename__ = "Locations"

    location_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    realm_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Realms.realm_id"))
    location_name = db.Column(db.String(), unique=True, nullable=False)
    danger_level = db.Column(db.Integer())

    realm = db.relationship("Realms", back_populates="locations")
    quests = db.relationship("Quests", back_populates="location")

    def __init__(self, realm_id, location_name, danger_level):
        self.realm_id = realm_id
        self.location_name = location_name
        self.danger_level = danger_level

    def new_location_obj():
        return Locations("", "", 0)
    

class LocationsSchema(ma.Schema):
    class Meta:
        fields = ['location_id', 'realm_id', 'location_name', 'danger_level', 'realm', 'quests']

    location_id = ma.fields.UUID()
    realm_id = ma.fields.UUID()
    location_name = ma.fields.String(required=True)
    danger_level = ma.fields.Integer()

    realm = ma.fields.Nested("RealmsSchema", exclude=['locations'])
    quests = ma.fields.Nested("QuestsSchema", many=True, exclude=['location'])


location_schema = LocationsSchema()
locations_schema = LocationsSchema(many=True)