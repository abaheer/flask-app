from music.domainmodel.artist import Artist
#from music.domainmodel.genre import Genre
from music.domainmodel.album import Album
from typing import List


class Track:
    def __init__(self, track_id: int, track_title: str):
        if type(track_id) is not int or track_id < 0:
            raise ValueError
        self.__track_id = track_id

        self.__title = None
        if type(track_title) is str:
            self.__title = track_title.strip()

        self.__artist = None
        self.__album: Album | None = None
        self.__track_url: str | None = None
        # duration in seconds
        self.__track_duration: int | None = None
        self.__genres: list = []
        self.__cur_artist_id = None

    @property
    def track_id(self) -> int:
        return self.__track_id

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, book_title: str):
        self.__title = None
        if type(book_title) is str and book_title.strip() != '':
            self.__title = book_title.strip()

    @property
    def artist(self) -> Artist:
        return self.__artist

    @property
    def cur_artist_id(self):
        return self.__artist.artist_id

    @artist.setter
    def artist(self, new_artist):
        if isinstance(new_artist, Artist):
            self.__artist = new_artist
        else:
            self.__artist = None

    @property
    def album(self) -> Album:
        return self.__album

    @album.setter
    def album(self, new_album):
        if isinstance(new_album, Album):
            self.__album = new_album
        else:
            self.__album = None

    @property
    def track_url(self) -> str:
        return self.__track_url

    @track_url.setter
    def track_url(self, new_track_url: str):
        if type(new_track_url) is str:
            self.__track_url = new_track_url.strip()
        else:
            self.__track_url = None

    @property
    def track_duration(self) -> int:
        return self.__track_duration

    @track_duration.setter
    def track_duration(self, new_duration: int):
        self.__track_duration = None
        if type(new_duration) is int and new_duration >= 0:
            self.__track_duration = new_duration
        else:
            raise ValueError

    @property
    def genres(self) -> list:
        return self.__genres

    def add_genre(self, new_genre):
        if not isinstance(new_genre, Genre) or new_genre in self.__genres:
            return
        self.__genres.append(new_genre)

    def __repr__(self):
        return f"<Track {self.title}, track id = {self.track_id}>"

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.track_id == other.track_id

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return True
        return self.track_id < other.track_id

    def __hash__(self):
        return hash(self.track_id)


class Genre:

    def __init__(self, genre_id: int, genre_name: str):
        if type(genre_id) is not int or genre_id < 0:
            raise ValueError('Genre ID should be an integer!')
        self.__genre_id = genre_id

        if type(genre_name) is str:
            self.__name = genre_name.strip()
        else:
            self.__name = None

        self.__genre_tracks: List[Track] = list()

    @property
    def genre_id(self) -> int:
        return self.__genre_id

    @property
    def genre_tracks(self):
        return self.__genre_tracks

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str):
        self.__name = None
        if type(name) is str:
            name = name.strip()
            if name != '':
                self.__name = name

    def __repr__(self) -> str:
        return f'<Genre {self.name}, genre id = {self.genre_id}>'

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.genre_id == other.genre_id

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return True
        return self.genre_id < other.genre_id

    def __hash__(self):
        return hash(self.genre_id)

    def add_track_to_genre(self, track: Track):
        add = True

        for genre_track in self.__genre_tracks:
            if genre_track == track:
                add = False

        if add:
            self.__genre_tracks.append(track)

    def is_applied_to(self, track) -> bool:
        return track in self.__genre_tracks


class ModelException(Exception):
    pass


def make_genre_association(track, genre):
    if genre.is_applied_to(track):
        raise ModelException(f'genre {genre.name} already applied to track "{track.title}"')

    genre.add_track_to_genre(track)
    track.add_genre(genre)

