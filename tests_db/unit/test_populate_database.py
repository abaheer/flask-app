from sqlalchemy import select, inspect

from music.adapters.orm import metadata

def test_database_populate_inspect_table_names(database_engine):

    # Get table information (sorting in alphabetical order)
    inspector = inspect(database_engine)
    assert inspector.get_table_names() == ['album', 'artist', 'genre', 'track', 'track_genre', 'user']

def test_database_populate_select_all_genres(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_genres_table = inspector.get_table_names()[2]

    with database_engine.connect() as connection:
        # query for records in table tags
        select_statement = select([metadata.tables[name_of_genres_table]])
        result = connection.execute(select_statement)

        all_genre_names = []
        for row in result:
            all_genre_names.append(row['genre_name'])

        assert all_genre_names == ['Avant-Garde', 'Pop', 'Folk', 'Hip-Hop', 'Noise', 'Experimental Pop', 'Singer-Songwriter']

def test_database_populate_select_all_users(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_users_table = inspector.get_table_names()[5]

    with database_engine.connect() as connection:
        # query for records in table users
        select_statement = select([metadata.tables[name_of_users_table]])
        result = connection.execute(select_statement)

        all_users = []
        for row in result:
            all_users.append(row['user_name'])

        assert all_users == ['man', 'woman']

def test_database_populate_select_all_albums(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_albums_table = inspector.get_table_names()[0]

    with database_engine.connect() as connection:
        # query for records in table comments
        select_statement = select([metadata.tables[name_of_albums_table]])
        result = connection.execute(select_statement)

        all_albums = []
        for row in result:
            all_albums.append((row['id'], row['title'], row['type'], row['release_year']))

        assert len(all_albums) == 5
        assert all_albums[1] == (4, 'Niris', 'Album', 2009)

def test_database_populate_select_all_artists(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_artists_table = inspector.get_table_names()[1]

    with database_engine.connect() as connection:
        # query for records in table comments
        select_statement = select([metadata.tables[name_of_artists_table]])
        result = connection.execute(select_statement)

        all_artists = []
        for row in result:
            all_artists.append((row['id'], row['full_name']))

        assert len(all_artists) == 5
        assert all_artists[1] == (4, 'Nicky Cook')

def test_database_populate_select_all_tracks(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_track_table = inspector.get_table_names()[3]

    with database_engine.connect() as connection:
        # query for records in table articles
        select_statement = select([metadata.tables[name_of_track_table]])
        result = connection.execute(select_statement)

        all_tracks = []
        for row in result:
            all_tracks.append((row['id'], row['title'], row['album_id'], row['artist_id']))

        assert len(all_tracks) == 10

        assert all_tracks[0] == (2, 'Food', 1, 1)



