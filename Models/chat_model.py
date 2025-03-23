from mongoengine import Document, StringField, ReferenceField, ListField, EmbeddedDocument, EmbeddedDocumentField
import datetime
from Models.user_model import User

class Message(EmbeddedDocument):
    from_role = StringField(choices=['user', 'doctor', 'lawyer', 'admin'], required=True)
    text = StringField(required=True)
    timestamp = StringField(default=str(datetime.datetime.utcnow()))

class Chat(Document):
    user = ReferenceField(User, required=True, reverse_delete_rule=2)
    name = StringField(required=True)
    avatar = StringField()
    messages = ListField(EmbeddedDocumentField(Message))
    
    def to_json(self):
        return {
            "id": str(self.id),
            "user": self.user.to_json() if self.user else None,
            "name": self.name,
            "avatar": self.avatar,
            "messages": [{"from": msg.from_role, "text": msg.text, "timestamp": msg.timestamp} for msg in self.messages]
        }
