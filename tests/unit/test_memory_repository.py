from datetime import date, datetime
from typing import List

import pytest

from music.domainmodel.track import Track, Genre
from music.domainmodel.user import User
from music.domainmodel.album import Album
from music.domainmodel.artist import Artist

from music.adapters.repository import RepositoryException


def test_repository_can_add_a_user(in_memory_repo):
    in_memory_repo.add_user('dave', 'Password1')

    assert in_memory_repo.get_user('dave').user_id == 1


def test_repository_can_retrieve_a_user(in_memory_repo):
    user = in_memory_repo.get_user('thorke')
    assert user.user_id == 0

    in_memory_repo.add_user('dave', 'Password1')
    assert in_memory_repo.get_user('dave').user_id == 1


def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user('who is this guy')
    assert user is None


def test_repository_retrieves_tracks(in_memory_repo):
    tracks = in_memory_repo.get_tracks(0, None, None, None)
    assert len(tracks) == 15    # 15 tracks should be retrieved for each page

    tracks = in_memory_repo.list_of_tracks(0, None, None, None)
    assert len(tracks) == 2000    # 2000 total tracks in test tracks csv


def test_repository_does_not_retrieve_non_existent_tracks(in_memory_repo):
    tracks = in_memory_repo.get_tracks(100001, None, None, None)
    assert tracks == []


def test_repository_retrieves_by_genre(in_memory_repo):
    genre = Genre(21, 'Hip-Hop')
    tracks_by_genre = in_memory_repo.list_of_tracks(0, None, None, genre.genre_id)

    assert len(tracks_by_genre) == 41   # 41 instances of hip-hop genre in tracks csv file


def test_repository_does_not_retrieve_non_existent_genre(in_memory_repo):
    genre = Genre(99919, 'hillbilly drum and bass')  # genre does not exist in csv files
    tracks_by_genre = in_memory_repo.get_tracks(0, None, None, genre.genre_id)

    assert len(tracks_by_genre) == 0


def test_repository_retrieves_by_album(in_memory_repo):
    album = Album(4, 'Niris')  # album in csv files
    tracks_by_album = in_memory_repo.list_of_tracks(0, album.album_id, None, None)

    assert len(tracks_by_album) == 5    # 5 tracks in test csv files with Niris album


def test_repository_does_not_retrieve_non_existent_album(in_memory_repo):
    album = Album(99919, 'a really bad album you should not listen to')  # genre does not exist in csv files
    tracks_by_album = in_memory_repo.get_tracks(0, album.album_id, None, None)

    assert len(tracks_by_album) == 0


def test_repository_retrieves_by_artist(in_memory_repo):
    artist = Artist(1, 'AWOL')  # artist with 4 tracks in the tracks csv file
    tracks_by_artist = in_memory_repo.get_tracks(0, None, artist.artist_id, None)

    assert len(tracks_by_artist) == 4


def test_repository_does_not_retrieve_non_existent_artist(in_memory_repo):
    artist = Artist(99919, 'a real clown')  # genre does not exist in csv files
    tracks_by_artist = in_memory_repo.get_tracks(0, None, artist.artist_id, None)

    assert len(tracks_by_artist) == 0
