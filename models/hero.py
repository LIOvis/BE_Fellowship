from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma
import uuid

from db import db

class Heroes(db.Model):
    __tablename__ = "Heroes"

    hero_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    race_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Races.race_id", ondelete='SET NULL'))
    hero_name = db.Column(db.String(), unique=True, nullable=False)
    age = db.Column(db.Integer())
    health_points = db.Column(db.Integer())
    is_alive = db.Column(db.Boolean(), default=True)

    race = db.relationship("Races", back_populates="heroes")
    abilities = db.relationship("Abilities", back_populates="hero", cascade="all")
    quests = db.relationship("HeroesQuests", back_populates="hero", cascade="all")

    def __init__(self, race_id, hero_name, age, health_points, is_alive=True):
        self.race_id = race_id
        self.hero_name = hero_name
        self.age = age
        self.health_points = health_points
        self.is_alive = is_alive

    def new_hero_obj():
        return Heroes("", "", 0, 0, True)
    

class HeroesSchema(ma.Schema):
    class Meta:
        fields = ['hero_id', 'race_id', 'hero_name', 'age', 'health_points', 'is_alive', 'race', 'abilities', 'quests']

    hero_id = ma.fields.UUID()
    race_id = ma.fields.UUID()
    hero_name = ma.fields.String(required=True)
    age = ma.fields.Integer()
    health_points = ma.fields.Integer()
    is_alive = ma.fields.Boolean(dump_default=True)

    race = ma.fields.Nested("RacesSchema", exclude=['heroes'])
    abilities = ma.fields.Nested("AbilitiesSchema", many=True, exclude=['hero'])
    quests = ma.fields.Nested("HeroesQuestsSchema", many=True, exclude=['hero'])

hero_schema = HeroesSchema()
heroes_schema = HeroesSchema(many=True)