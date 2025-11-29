from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma
import uuid

from db import db

class Quests(db.Model):
    __tablename__ = "Quests"

    quest_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    location_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Locations.location_id", ondelete='SET NULL'))
    quest_name = db.Column(db.String(), unique=True, nullable=False)
    difficulty = db.Column(db.String())
    reward_gold = db.Column(db.Integer())
    is_completed = db.Column(db.Boolean(), default=False)

    location = db.relationship("Locations", back_populates="quests")
    heroes = db.relationship("HeroesQuests", back_populates="quest", cascade="all")

    def __init__(self, location_id, quest_name, difficulty, reward_gold, is_completed=False):
        self.location_id = location_id
        self.quest_name = quest_name
        self.difficulty = difficulty
        self.reward_gold = reward_gold
        self.is_completed = is_completed

    def new_quest_obj():
        return Quests("", "", "", 0, False)
    

class QuestsSchema(ma.Schema):
    class Meta:
        fields = ['quest_id', 'location_id', 'quest_name', 'difficulty', 'reward_gold', 'is_completed', 'location', 'heroes']

    quest_id = ma.fields.UUID()
    location_id = ma.fields.UUID()
    quest_name = ma.fields.String(required=True)
    difficulty = ma.fields.String()
    reward_gold = ma.fields.Integer()
    is_completed = ma.fields.Boolean(dump_default=False)

    location = ma.fields.Nested("LocationsSchema", exclude=['quests'])
    heroes = ma.fields.Nested("HeroesQuestsSchema", many=True, exclude=['quest'])
    

quest_schema = QuestsSchema()
quests_schema = QuestsSchema(many=True)
