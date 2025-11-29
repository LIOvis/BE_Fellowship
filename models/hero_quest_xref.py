from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma
import uuid

from db import db

class HeroesQuests(db.Model):
    __tablename__ = "HeroesQuests"

    hero_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Heroes.hero_id"), primary_key=True)
    quest_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Quests.quest_id"), primary_key=True)
    date_joined = db.Column(db.DateTime())

    hero = db.relationship("Heroes", back_populates="quests")
    quest = db.relationship("Quests", back_populates="heroes")

    def __init__(self, hero_id, quest_id, date_joined=None):
        self.hero_id = hero_id
        self.quest_id = quest_id
        self.date_joined = date_joined

    def new_hero_quest_obj():
        return HeroesQuests("", "", "")
    

class HeroesQuestsSchema(ma.Schema):
    class Meta:
        fields = ['hero_id', 'quest_id', 'date_joined', 'hero', 'quest']

    hero_id = ma.fields.UUID()
    quest_id = ma.fields.UUID()
    date_joined = ma.fields.DateTime()

    hero = ma.fields.Nested("HeroesSchema", exclude=['quests'])
    quest = ma.fields.Nested("QuestsSchema", exclude=['heroes'])


hero_quest_schema = HeroesQuestsSchema()
heroes_quests_schema = HeroesQuestsSchema(many=True)
    
