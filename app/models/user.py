from app import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(50), nullable=False)
    campus_id = db.Column(db.BigInteger, db.ForeignKey("campuses.id"), nullable=True)

    campus = db.relationship("Campus", backref=db.backref("users", lazy=True))

    def __repr__(self):
        return f"<User {self.name}, email={self.email}>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "campus_id": self.campus_id,
        }
