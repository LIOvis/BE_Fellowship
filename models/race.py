from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma
import uuid

from db import db

class Races(db.Model):
    __tablename__ = "Races"

    race_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    race_name = db.Column(db.String(), unique=True, nullable=False)
    homeland = db.Column(db.String())
    lifespan = db.Column(db.Integer())

    heroes = db.relationship("Heroes", back_populates="race")

    def __init__(self, race_name, homeland, lifespan):
        self.race_name = race_name
        self.homeland = homeland
        self.lifespan = lifespan

    def new_race_obj():
        return Races("", "", 0)
    

class RacesSchema(ma.Schema):
    class Meta:
        fields = ['race_id', 'race_name', 'homeland', 'lifespan', 'heroes']

    race_id = ma.fields.UUID()
    race_name = ma.fields.String(required=True)
    homeland = ma.fields.String()
    lifespan = ma.fields.Integer()

    heroes = ma.fields.Nested("HeroesSchema", many=True, exclude=['race'])


race_schema = RacesSchema()
races_schema = RacesSchema(many=True)
