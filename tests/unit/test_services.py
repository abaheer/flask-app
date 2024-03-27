from datetime import date

import pytest

from music.domainmodel.track import Track
from music.auth.services import AuthenticationException
from music.auth.services import UnknownUserException
from music.tracks import services as tracks_services
from music.auth import services as auth_services
from music.tracks.services import NonExistentTrackException


def test_can_retrieve_existing_user(in_memory_repo):
    try:
        auth_services.get_user('thorke', in_memory_repo)
    except UnknownUserException:
        assert False


def test_cannot_retrieve_non_existing_user(in_memory_repo):
    with pytest.raises(auth_services.UnknownUserException):
        auth_services.get_user('who is this guy', in_memory_repo)


def test_can_add_user(in_memory_repo):
    new_user_name = 'jz'
    new_password = 'abcd1A23'

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    user_as_dict = auth_services.get_user(new_user_name, in_memory_repo)
    assert user_as_dict['user_name'] == new_user_name

    # Check that password has been encrypted.
    assert user_as_dict['password'].startswith('pbkdf2:sha256:')


def test_cannot_add_user_with_existing_name(in_memory_repo):
    user_name = 'thorke'
    password = 'abcd1A23'

    with pytest.raises(auth_services.NameNotUniqueException):
        auth_services.add_user(user_name, password, in_memory_repo)


def test_authentication_with_valid_credentials(in_memory_repo):
    new_user_name = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    try:
        auth_services.authenticate_user(new_user_name, new_password, in_memory_repo)
    except AuthenticationException:
        assert False


def test_authentication_with_invalid_credentials(in_memory_repo):
    new_user_name = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(new_user_name, '0987654321', in_memory_repo)


def test_home_display_tracks(in_memory_repo):
    home_tracks = tracks_services.get_home(in_memory_repo)

    assert len(home_tracks) == 3
    for track in home_tracks:
        assert isinstance(track, Track)


def test_get_genres_valid_start(in_memory_repo):
    # check correct amount of genres displayed per page
    genres = tracks_services.get_genres(in_memory_repo, 0)
    assert len(genres) == 14

    genres2 = tracks_services.get_genres(in_memory_repo, 14)
    assert len(genres) == 14

    # check next page contains correct first genre
    next_page = tracks_services.all_genres(in_memory_repo)[14]
    assert genres[len(genres) - 1] != next_page
    assert genres2[0] == next_page


def test_get_genres_invalid_start(in_memory_repo):
    with pytest.raises(tracks_services.NonExistentTrackException):
        tracks_services.get_genres(in_memory_repo, 1000)


def test_get_albums_valid_start(in_memory_repo):
    albums = tracks_services.get_albums(in_memory_repo, 0)
    assert len(albums) == 15

    albums2 = tracks_services.get_albums(in_memory_repo, 15)
    assert len(albums) == 15

    next_page = tracks_services.all_albums(in_memory_repo)[15]
    assert albums[len(albums) - 1] != next_page
    assert albums2[0] == next_page


def test_get_albums_invalid_start(in_memory_repo):
    with pytest.raises(tracks_services.NonExistentTrackException):
        tracks_services.get_albums(in_memory_repo, 1000)


def test_get_artists_valid_start(in_memory_repo):
    artists = tracks_services.get_artists(in_memory_repo, 0)
    assert len(artists) == 14

    artists2 = tracks_services.get_artists(in_memory_repo, 14)
    assert len(artists2) == 14

    next_page = tracks_services.all_artists(in_memory_repo)[14]
    assert artists[len(artists) - 1] != next_page
    assert artists2[0] == next_page


def test_get_artists_invalid_start(in_memory_repo):
    with pytest.raises(tracks_services.NonExistentTrackException):
        tracks_services.get_artists(in_memory_repo, 1000)


def test_get_tracks_valid_start(in_memory_repo):
    tracks = tracks_services.get_tracks(in_memory_repo, 0, None, None, None)
    assert len(tracks) == 15

    tracks2 = tracks_services.get_tracks(in_memory_repo, 15, None, None, None)
    assert len(tracks2) == 15

    next_page = tracks_services.all_tracks(in_memory_repo, 0, None, None, None)[15]
    assert tracks[len(tracks) - 1] != next_page
    assert tracks2[0] == next_page


def test_get_tracks_invalid_start(in_memory_repo):
    with pytest.raises(tracks_services.NonExistentTrackException):
        tracks_services.get_tracks(in_memory_repo, 10000, None, None, None)


def test_get_tracks_by_invalid_genre(in_memory_repo):
    with pytest.raises(tracks_services.NonExistentTrackException):
        tracks_services.get_tracks(in_memory_repo, 0, None, None, 100000)


def test_get_tracks_by_invalid_album(in_memory_repo):
    with pytest.raises(tracks_services.NonExistentTrackException):
        tracks_services.get_tracks(in_memory_repo, 0, 10000, None, None)


def test_get_tracks_by_invalid_artist(in_memory_repo):
    with pytest.raises(tracks_services.NonExistentTrackException):
        tracks_services.get_tracks(in_memory_repo, 0, None, 100000, None)