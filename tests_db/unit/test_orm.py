import pytest

import datetime

from sqlalchemy.exc import IntegrityError

import music.adapters.repository as repo
from music.adapters.database_repository import SqlAlchemyRepository
from music.domainmodel.track import Track, Genre
from music.domainmodel.artist import Artist
from music.domainmodel.album import Album
from music.domainmodel.user import User


def insert_user(empty_session, values=None):
    new_id = 0
    new_name = "Andrew"
    new_password = "1234"

    if values is not None:
        new_id = values[0]
        new_name = values[1]
        new_password = values[2]

    empty_session.execute('INSERT INTO user (id, user_name, password) VALUES (:id, :user_name, :password)',
                          {'id': new_id, 'user_name': new_name, 'password': new_password})
    row = empty_session.execute('SELECT id from user where user_name = :user_name',
                                {'user_name': new_name}).fetchone()
    return row[0]


def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO user (id, user_name, password) VALUES (:id, :user_name, :password)',
                              {'id': value[0], 'user_name': value[1], 'password': value[2]})
    rows = list(empty_session.execute('SELECT id from user'))
    keys = tuple(row[0] for row in rows)
    return keys


def make_user():
    user = User(0, "some guy", "password1")
    return user


def make_track():
    track = Track(
        0, "cool song"
    )

    track.album = make_album()
    track.artist = make_artist()
    track.add_genre(make_genre())
    track.track_url = 'google.com'
    track.track_duration = 55

    return track


def make_album():
    album = Album(1, "cool album")
    return album


def make_artist():
    artist = Artist(1, "cool artist")
    return artist


def make_genre():
    genre = Genre(0, "cool genre")
    return genre


def insert_track(empty_session):
    track = make_track()

    empty_session.merge(track)
    empty_session.commit()

    row = empty_session.execute('SELECT id from track').fetchone()
    return row[0]


def insert_album(empty_session):
    album = make_album()

    empty_session.merge(album)
    empty_session.commit()

    row = empty_session.execute('SELECT id from album').fetchone()
    return row[0]


def insert_artist(empty_session):
    artist = make_artist()

    empty_session.merge(artist)
    empty_session.commit()

    row = empty_session.execute('SELECT id from artist').fetchone()
    return row[0]


def insert_genre(empty_session):
    genre = make_genre()

    empty_session.merge(genre)
    empty_session.commit()

    row = empty_session.execute('SELECT id from genre').fetchone()
    return row[0]


def test_loading_of_users(empty_session):
    users = list()
    users.append((0, "Andrew", "1234"))
    users.append((1, "Cindy", "1111"))
    insert_users(empty_session, users)

    expected = [
        User(0, "Andrew", "1234"),
        User(1, "Cindy", "999")
    ]
    assert empty_session.query(User).all() == expected


def test_saving_of_users(empty_session):
    user = make_user()
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT id, user_name, password FROM user'))
    assert rows == [(0, "some guy", "password1")]


def test_saving_of_users_with_common_user_name(empty_session):
    empty_session.add(User(66, "Johnny", "aPassword4yuo"))
    empty_session.commit()

    with pytest.raises(IntegrityError):
        user = User(1, "Johnny", "aPassword4yuo")
        empty_session.add(user)
        empty_session.commit()


def test_loading_of_track(empty_session):
    track_key = insert_track(empty_session)
    expected_track = make_track()
    fetched_track = empty_session.query(Track).one()

    assert expected_track == fetched_track
    assert track_key == fetched_track.track_id


def test_loading_of_album(empty_session):
    album_key = insert_album(empty_session)
    expected_album = make_album()
    fetched_album = empty_session.query(Album).one()

    assert expected_album == fetched_album
    assert album_key == fetched_album.album_id


def test_loading_of_artist(empty_session):
    artist_key = insert_artist(empty_session)
    expected_artist = make_artist()
    fetched_artist = empty_session.query(Artist).one()

    assert expected_artist == fetched_artist
    assert artist_key == fetched_artist.artist_id


def test_loading_of_genre(empty_session):
    genre_key = insert_genre(empty_session)
    expected_genre = make_genre()
    fetched_genre = empty_session.query(Genre).one()

    assert expected_genre == fetched_genre
    assert genre_key == fetched_genre.genre_id

