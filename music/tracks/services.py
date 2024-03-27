from typing import List, Iterable
import random

from music.adapters.repository import AbstractRepository
from music.domainmodel import album
from music.domainmodel.track import Track
from music.domainmodel.review import Review


class NonExistentTrackException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def get_tracks(repo: AbstractRepository, start: int, album_id, artist_id, genre_id):
    if start < 0:
        start = 0
    cur_tracks = repo.get_tracks(start, album_id, artist_id, genre_id)

    if cur_tracks is None or cur_tracks == []:
        raise NonExistentTrackException

    # return track_to_dict(cur_track)
    return cur_tracks


def all_tracks(repo: AbstractRepository, cursor, album_id, artist_id, genre_id):
    return repo.list_of_tracks(cursor, album_id, artist_id, genre_id)


def get_albums(repo: AbstractRepository, start: int):
    if start < 0:
        start = 0

    albums = repo.get_albums(start)

    if albums is None or albums == []:
        raise NonExistentTrackException

    return albums


def all_albums(repo: AbstractRepository):
    return repo.list_of_albums()


def get_artists(repo: AbstractRepository, start: int):
    if start < 0:
        start = 0

    artists = repo.get_artists(start)

    if artists is None or artists == []:
        raise NonExistentTrackException

    return artists


def all_artists(repo: AbstractRepository):
    return repo.list_of_artists()


def get_genres(repo: AbstractRepository, start: int):
    if start < 0:
        start = 0

    genres = repo.get_genres(start)

    if genres is None or genres == []:
        raise NonExistentTrackException

    return genres


def all_genres(repo: AbstractRepository):
    return repo.list_of_genres()


def get_home(repo: AbstractRepository):

    every_track = repo.every_track()
    nums = random.sample(range(len(every_track)), 3)

    return repo.get_3_tracks(nums[0], nums[1], nums[2])

# def get_track(track_id: int, repo: AbstractRepository):
#     track = repo.get_track(track_id)
#
#     if track is None:
#         raise NonExistentTrackException
#
#     return track
#
#
# def add_comment(track_id: int, comment_text: str, user_name: str, repo: AbstractRepository):
#     # Check that the article exists.
#     track = repo.get_track(track_id)
#     if track is None:
#         raise NonExistentTrackException
#
#     user = repo.get_user(user_name)
#     if user is None:
#         raise UnknownUserException
#
#     # Create comment.
#     comment = Review(track, comment_text, user)
#
#     # Update the repository.
#     repo.add_comment(comment)