from datetime import date, datetime

import pytest

import music.adapters.repository as repo
from music.adapters.database_repository import SqlAlchemyRepository
from music.domainmodel.track import Track, Genre
from music.domainmodel.artist import Artist
from music.domainmodel.album import Album
from music.domainmodel.user import User

from music.adapters.repository import RepositoryException

def test_repository_can_retrieve_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    assert repo.get_user('man').user_id == 0
    assert repo.get_user('woman').user_id == 1

def test_repository_can_add_and_retrieve_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    repo.add_user('dave', 'Password1')
    repo.add_user('jimmy', 'Password321321')
    assert repo.get_user('dave').user_id == 2
    assert repo.get_user('jimmy').user_id == 3

def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('idk this guy')
    assert user is None

def test_repository_can_retrieve_tracks(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    tracks = repo.get_tracks(0, None, None, None)
    assert len(tracks) == 15    # 15 tracks should be retrieved for each page

    tracks = repo.list_of_tracks(0, None, None, None)
    assert len(tracks) == 2000    # 2000 total tracks in test tracks csv

def test_repository_does_not_retrieve_a_non_existent_track(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    tracks = repo.get_tracks(100001, None, None, None)
    assert tracks == []

def test_repository_retrieves_by_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    genre = Genre(21, 'Hip-Hop')
    tracks_by_genre = repo.list_of_tracks(0, None, None, genre.genre_id)

    assert len(tracks_by_genre) == 41   # 41 instances of hip-hop genre in tracks csv file


def test_repository_retrieves_by_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    genre = Genre(99919, 'UK Drill study music')  # genre does not exist in csv files
    tracks_by_genre = repo.get_tracks(0, None, None, genre.genre_id)

    assert len(tracks_by_genre) == 0

def test_repository_retrieves_by_album(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    album = Album(4, 'Niris')  # album in csv files
    tracks_by_album = repo.list_of_tracks(0, album.album_id, None, None)

    assert len(tracks_by_album) == 5    # 5 tracks in test csv files with Niris album

def test_repository_retrieves_by_album(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    album = Album(99919, 'a really bad album you should not listen to')  # album does not exist in csv files
    tracks_by_album = repo.get_tracks(0, album.album_id, None, None)

    assert len(tracks_by_album) == 0

def test_repository_retrieves_by_artist(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    artist = Artist(1, 'AWOL')  # artist with 4 tracks in the tracks csv file
    tracks_by_artist = repo.get_tracks(0, None, artist.artist_id, None)

    assert len(tracks_by_artist) == 4

def test_repository_does_not_retrieve_non_existent_artist(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    artist = Artist(99919, 'a real clown')  # artist does not exist in csv files
    tracks_by_artist = repo.get_tracks(0, None, artist.artist_id, None)

    assert len(tracks_by_artist) == 0