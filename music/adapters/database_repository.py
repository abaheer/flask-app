from datetime import date
from typing import List

from sqlalchemy import desc, asc
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from sqlalchemy.orm import scoped_session

from music.domainmodel.user import User
from music.domainmodel.track import Track, Genre
from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.adapters.repository import AbstractRepository

from music.adapters.csvdatareader import TrackCSVReader


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)
        self.num_tracks = 15

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_user(self, user_name, password):

        number_of_users = self._session_cm.session.query(User).count()
        user = User(number_of_users, user_name, password)
        with self._session_cm as scm:
            scm.session.merge(user)
            scm.commit()

    def add_track(self, track):
        with self._session_cm as scm:
            scm.session.merge(track)
            scm.commit()

    def add_album(self, album):
        with self._session_cm as scm:
            scm.session.merge(album)
            scm.commit()

    def add_artist(self, artist):
        with self._session_cm as scm:
            scm.session.merge(artist)
            scm.commit()

    def add_genre(self, genre):
        with self._session_cm as scm:
            scm.session.merge(genre)
            scm.commit()

    def get_user(self, user_name: str) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter(User._User__user_name == user_name).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return user

    def list_of_tracks(self, start, album_id, artist_id, genre_id):
        if album_id is None and artist_id is None and genre_id is None:
            return self.every_track()

        if album_id:
            return self._session_cm.session.query(Track).filter(Track.album_id == album_id).all()

        if artist_id:
            return self._session_cm.session.query(Track).filter(Track.album_id == artist_id).all()

        if genre_id:
            track_ids = []
            # Use native SQL to retrieve track ids, since there is no mapped class for the track_genre table.
            row = self._session_cm.session.execute('SELECT id FROM genre WHERE id = :genre_id',
                                                   {'genre_id': genre_id}).fetchone()

            if row is None:
                return []

            else:
                genre_id = row[0]
                # Retrieve track ids of articles associated with the genre.
                track_ids = self._session_cm.session.execute(
                    'SELECT track_id FROM track_genre WHERE genre_id = :genre_id ORDER BY track_id ASC',
                    {'genre_id': genre_id}
                ).fetchall()
                track_ids = [trackID[0] for trackID in track_ids]
            return self._session_cm.session.query(Track).filter(Track._Track__track_id.in_(track_ids)).all()

        return []

    def every_track(self):
        return self._session_cm.session.query(Track).all()

    def get_tracks(self, start, album_id, artist_id, genre_id):
        return self.list_of_tracks(start, album_id, artist_id, genre_id)[start:start + self.num_tracks]

    def get_3_tracks(self, index1, index2, index3):
        every_track = self.every_track()
        return [every_track[index1], every_track[index2], every_track[index3]]

    def list_of_albums(self):
        albums = self._session_cm.session.query(Album).all()
        return albums

    def list_of_artists(self):
        artists = self._session_cm.session.query(Artist).all()
        return artists

    def list_of_genres(self):
        genres = self._session_cm.session.query(Genre).all()
        return genres

    def get_albums(self, start):
        return self.list_of_albums()[start:start + self.num_tracks]

    def get_artists(self, start):
        return self.list_of_artists()[start:start + self.num_tracks - 1]

    def get_genres(self, start):
        return self.list_of_genres()[start:start + self.num_tracks - 1]

    def get_reader(self, reader):
        pass
