from mongoengine import Document, StringField

class File(Document):
    title = StringField(required=True)
    content = StringField(required=True)

    def to_json(self):
        return {
            "id": str(self.id),
            "title": self.title,
            "content": self.content
        }
