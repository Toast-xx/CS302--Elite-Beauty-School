from app import db


class Campus(db.Model):
    __tablename__ = "campuses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<Campus {self.name}>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "location": self.location,
        }
