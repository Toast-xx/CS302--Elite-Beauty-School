# Model for campus information.
# Represents a campus with name, description, and location.
# Used for user association, product availability, and delivery options.
# Includes helper methods for string representation and serialization.

from app import db


class Campus(db.Model):
    __tablename__ = "campuses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(200), nullable=False)
    products = db.relationship(
        'Product',
        secondary='product_campus',
        back_populates='campuses'
    )

    def __repr__(self):
        return f"<Campus {self.name}>"

    def to_dict(self):
        # Converts campus instance to dictionary for API or template use
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "location": self.location,
        }