from pathlib import Path

from music.adapters import database_repository
from music.adapters.repository import AbstractRepository
from music.adapters.csvdatareader import TrackCSVReader
from music.adapters.database_repository import SqlAlchemyRepository
from music.adapters.memory_repository import MemoryRepository
from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime,
    ForeignKey
)
from sqlalchemy.orm import mapper, relationship, synonym

from music.domainmodel.artist import Artist


def populate(albums_file, tracks_file, repo: AbstractRepository, database_mode):
    reader = TrackCSVReader(albums_file, tracks_file)
    reader.read_csv_files()

    if not database_mode:
        repo.get_reader(reader)

    # print("THESE ARE THE TRACKS" , reader.dataset_of_tracks)
    # print("THESE ARE THE ARTISTS", reader.list_of_artists())
    # print("THESE ARE THE albums", reader.list_of_albums())
    # print("THESE ARE THE genres", reader.list_of_genres())

    if database_mode:
        for artist in reader.list_of_artists():
            repo.add_artist(artist)

        for album in reader.list_of_albums():
            repo.add_album(album)

        for genre in reader.list_of_genres():
            repo.add_genre(genre)

        for track in reader.dataset_of_tracks:
            repo.add_track(track)
