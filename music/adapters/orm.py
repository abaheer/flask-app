from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime,
    ForeignKey
)
from sqlalchemy.orm import mapper, relationship, synonym

from music.domainmodel.user import User
from music.domainmodel.track import Track, Genre
from music.domainmodel.artist import Artist
from music.domainmodel.album import Album
#from music.domainmodel.genre import Genre

# global variable giving access to the MetaData (schema) information of the database
metadata = MetaData()

user_table = Table(
    'user', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_name', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False)
)

artist_table = Table(
    'artist', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('full_name', String(255), nullable=False)
)

album_table = Table(
    'album', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', String(255), nullable=False),
    Column('type', String(255), nullable=True),
    Column('release_year', Integer, nullable=True)
)

genre_table = Table(
    'genre', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(255), nullable=False)
)

track_table = Table(
    'track', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('artist_id', ForeignKey('artist.id'), nullable=False),
    Column('album_id', ForeignKey('album.id'), nullable=True),
    Column('title', String(255), nullable=False),
    Column('duration', Integer, nullable=False),
    Column('url', String(255), nullable=True)
)

# many-to-many relationship between tracks and genres

track_genres_table = Table(
    'track_genre', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('track_id', ForeignKey('track.id')),
    Column('genre_id', ForeignKey('genre.id'))
)


def map_model_to_tables():
    mapper(User, user_table, properties={
        '_User__user_id': user_table.c.id,
        '_User__user_name': user_table.c.user_name,
        '_User__password': user_table.c.password
    })
    mapper(Artist, artist_table, properties={
        '_Artist__artist_id': artist_table.c.id,
        '_Artist__full_name': artist_table.c.full_name,
    })
    mapper(Album, album_table, properties={
        '_Album__album_id': album_table.c.id,
        '_Album__title': album_table.c.title,
        '_Album__album_type': album_table.c.type,
        '_Album__release_year': album_table.c.release_year,
    })
    mapper(Genre, genre_table, properties={
        '_Genre__genre_id': genre_table.c.id,
        '_Genre__name': genre_table.c.name,
        '_Genre__genre_tracks': relationship(
            Track,
            secondary=track_genres_table,
            back_populates="_Track__genres"
        )
    })
    mapper(Track, track_table, properties={
        '_Track__track_id': track_table.c.id,
        '_Track__title': track_table.c.title,
        '_Track__track_duration': track_table.c.duration,
        '_Track__track_url': track_table.c.url,
        '_Track__album': relationship(Album),
        '_Track__artist': relationship(Artist),
        '_Track__genres': relationship(
            Genre, secondary=track_genres_table,
            back_populates='_Genre__genre_tracks'
        )
    })
