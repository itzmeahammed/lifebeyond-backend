from mongoengine import Document, StringField, ReferenceField, ListField, EmbeddedDocument, EmbeddedDocumentField
import datetime
from Models.user_model import User

class Message(EmbeddedDocument):
    from_role = StringField(choices=['user', 'doctor', 'lawyer', 'admin'], required=True)
    text = StringField(required=True)
    timestamp = StringField(default=str(datetime.datetime.utcnow()))

class Chat(Document):
    person1 = ReferenceField(User, required=True, reverse_delete_rule=2)
    person2 = ReferenceField(User, required=True, reverse_delete_rule=2)
    messages = ListField(EmbeddedDocumentField(Message))
    
    def to_json(self):
        return {
            "id": str(self.id),
            "person1": self.person1.to_json() if self.person1 else None,
            "person2": self.person2.to_json() if self.person2 else None,
            "messages": [{"from": msg.from_role, "text": msg.text, "timestamp": msg.timestamp} for msg in self.messages]
        }
