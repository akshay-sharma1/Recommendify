from . import db
from flask_login import UserMixin


# TODO: remove storage of spotify_id
class SpotifyUser(UserMixin, db.Model):
    __tablename__ = "SpotifyUser"
    id = db.Column(db.Integer,
                   primary_key=True)

    spotify_id = db.Column(db.String(64),
                           unique=True,
                           nullable=False)

    display_name = db.Column(db.String(64),
                             index=False,
                             unique=False,
                             nullable=True)

    last_login = db.Column(db.DateTime,
                           index=False,
                           unique=False,
                           nullable=True)

    def __repr__(self):
        return '<User {}>'.format(self.spotify_id)


