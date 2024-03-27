import csv
from pathlib import Path
from datetime import date, datetime
from typing import List
from music.adapters.csvdatareader import TrackCSVReader

from bisect import bisect, bisect_left, insort_left

from music.adapters.repository import AbstractRepository, RepositoryException
from music.domainmodel.review import Review
from music.domainmodel.track import Track
from music.domainmodel.user import User


class MemoryRepository(AbstractRepository):

    def __init__(self):

        self.reader = None
        self.num_tracks = 15  # number of items per page
        self.__users = list()
        # self.__comments = list()

    def get_reader(self, reader):
        self.reader = reader

    def list_of_tracks(self, start, album_id, artist_id, genre_id):
        if album_id is None and artist_id is None and genre_id is None:
            return self.reader.dataset_of_tracks

        display = []

        if album_id:
            for track in self.reader.dataset_of_tracks:
                if track.album:
                    if track.album.album_id == int(album_id):
                        display.append(track)

        if artist_id:
            for track in self.reader.dataset_of_tracks:
                if track.artist:
                    if track.artist.artist_id == int(artist_id):
                        display.append(track)

        if genre_id:
            for track in self.reader.dataset_of_tracks:
                if track.genres:
                    for genres in track.genres:
                        if genres.genre_id == int(genre_id):
                            display.append(track)

        return display

    def every_track(self):
        return self.reader.dataset_of_tracks

    def get_tracks(self, start, album_id, artist_id, genre_id):
        return self.list_of_tracks(start, album_id, artist_id, genre_id)[start:start + self.num_tracks]

    def get_3_tracks(self, index1, index2, index3):
        every_track = self.every_track()
        return [every_track[index1], every_track[index2], every_track[index3]]

    def list_of_albums(self):
        return self.reader.list_of_albums()

    def list_of_artists(self):
        return self.reader.list_of_artists()

    def list_of_genres(self):
        return self.reader.list_of_genres()

    def get_albums(self, start):
        return self.reader.list_of_albums()[start:start + self.num_tracks]

    def get_artists(self, start):
        return self.reader.list_of_artists()[start:start + self.num_tracks - 1]

    def get_genres(self, start):
        return self.reader.list_of_genres()[start:start + self.num_tracks - 1]

    def get_user(self, username):
        return next((user for user in self.__users if user.user_name == username), None)

    def add_user(self, username, password):
        user = User(len(self.__users), username, password)
        self.__users.append(user)

    def add_track(self, track):
        pass

    def add_album(self, album):
        pass

    def add_artist(self, artist):
        pass

    def add_genre(self, genre):
        pass

    # def get_track(self, id: int) -> Track:
    #
    #     for track in self.reader.dataset_of_tracks:
    #         if track.track_id == id:
    #             return track
    #
    #     return None
    #
    # def add_comment(self, comment):
    #     self.__comments.append(comment)
    #
    # def get_comments(self):
    #     return self.__comments

# # #
# m = MemoryRepository()
# a = m.list_of_genres()
# print(a)
# m.add_comment(Review(m.get_track(2), "swag", User(5, "coolman", "password")))
# m.add_comment(Review(m.reader.dataset_of_tracks[1], "wooooow", User(6, "notcoolman", "good2")))
#
# print(m.get_comments())

#print(m.list_of_genres())
# # a = m.get_albums(2)
# # b = m.get_tracks
# # # print(b)
# # # print(a)
# n = (m.list_of_albums())
# print('hello')
# a = m.list_of_genres()
# print(len(a))
# n = m.get_tracks(0, None, None, 2)

# print(n)