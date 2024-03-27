import abc
from typing import List
from datetime import date

from music.domainmodel.track import Track
from music.domainmodel.album import Album

repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def list_of_tracks(self, start, album_id, artist_id, genre_id) -> list:
        """ Return list of all tracks which fit parameters """
        raise NotImplementedError

    @abc.abstractmethod
    def get_tracks(self, start: int, album_id, artist_id, genre_id) -> list:
        """ returns x amount of track objects from a list of tracks """
        raise NotImplementedError

    @abc.abstractmethod
    def every_track(self) -> list:
        """ returns every track """
        raise NotImplementedError

    @abc.abstractmethod
    def get_3_tracks(self, index1, index2, index3) -> list:
        """ returns 3 track objects from a list of tracks (for homepage) """
        raise NotImplementedError

    @abc.abstractmethod
    def get_albums(self, start: int) -> list:
        """ Return a list of all albums to be displayed """
        raise NotImplementedError

    @abc.abstractmethod
    def get_artists(self, start: int) -> list:
        """ Return a list of all albums to be displayed """
        raise NotImplementedError

    @abc.abstractmethod
    def get_genres(self, start: int) -> list:
        """ Return a list of all genres to be displayed """
        raise NotImplementedError

    def list_of_artists(self):
        """ Return a list of all artists """
        raise NotImplementedError

    @abc.abstractmethod
    def list_of_albums(self) -> list:
        """ Return a list of all albums """
        raise NotImplementedError

    @abc.abstractmethod
    def list_of_genres(self) -> list:
        """ Return a list of all genres """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username):
        """ Return user """
        raise NotImplementedError

    @abc.abstractmethod
    def add_user(self, username, password):
        """ add user to list of users """
        raise NotImplementedError

    @abc.abstractmethod
    def get_reader(self, reader):
        """ get datasets from csv file """
        raise NotImplementedError

    @abc.abstractmethod
    def add_track(self, track):
        """ add track to repo """
        raise NotImplementedError

    @abc.abstractmethod
    def add_album(self, album):
        """ add album to repo """
        raise NotImplementedError

    @abc.abstractmethod
    def add_artist(self, artist):
        """ add artist to repo """
        raise NotImplementedError

    @abc.abstractmethod
    def add_genre(self, genre):
        """ add genre to repo """
        raise NotImplementedError


    # @abc.abstractmethod
    # def populate(self, albums_file, tracks_file):
    #     """ populate abstract repo """
    #     raise NotImplementedError

    # @abc.abstractmethod
    # def get_track(self, id: int) -> Track:
    #     """ return track corresponding to input track id """
    #     raise NotImplementedError
