#!/usr/bin/env python3

"""Model Objects."""
import datetime

from digital_lotus import db, bcrypt


class User(db.Model):
    """User object."""

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, username, first_name, last_name, password, admin=False):
        """Initializer for User object."""
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = bcrypt.generate_password_hash(password)
        self.admin = admin
        self.registered_on = datetime.datetime.now()

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return True

    def is_active(self):
        """True, as all users are active."""
        return True

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    def get_id(self):
        """Return the id to satisfy Flask-Login's requirements."""
        return str(self.id)

    @property
    def is_admin(self):
        """Method to check if user is admin."""
        return (self.admin == True)

    def save(self):
        """Overriding save method to set created on."""
        if not self.id:
            db.session.add(self)
        return db.session.commit()

    def check_password(self, password):
        """Method to check password."""
        return bcrypt.check_password_hash(self.password, password)

    def delete(self):
        """Delete entry."""
        db.session.delete(self)
        return db.session.commit()

    def __repr__(self):
        """Representation of User object."""
        return 'User - email: {}'.format(self.email)
