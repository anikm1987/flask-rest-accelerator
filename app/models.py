# app/models.py

from app import db


class Bloglist(db.Model):
    """This class represents the bloglist table."""

    __tablename__ = 'bloglists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    def __init__(self, name):
        """initialize with name."""
        self.name = name

    def save(self):
        """The save() method will be used to add a new bloglist to the DB."""
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        """The get_all() method is a static method that'll be used to get all the bloglists in a single query."""
        return Bloglist.query.all()

    def delete(self):
        """ The delete() method will be used to delete an existing blog from the DB"""
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        """The __repr__ method represents the object instance of the model whenever it is queried."""
        return "<Bloglist: {}>".format(self.name)