import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from music.adapters import database_repository, repository_populate
from music.adapters.orm import metadata, map_model_to_tables

from utils import get_project_root

# the csv files in the test folder are different from the csv files in the covid/adapters/data folder!
# tests are written against the csv files in tests, this data path is used to override default path for testing
TEST_ALBUMS_PATH = get_project_root() / "tests" / "data" / "raw_albums_excerpt.csv"
TEST_TRACKS_PATH = get_project_root() / "tests" / "data" / "raw_tracks_excerpt.csv"

TEST_ALBUMS_PATH_LIMITED = get_project_root() / "tests" / "data" / "raw_albums_test.csv"
TEST_TRACKS_PATH_LIMITED = get_project_root() / "tests" / "data" / "raw_tracks_test.csv"

TEST_DATABASE_URI_IN_MEMORY = 'sqlite://'
TEST_DATABASE_URI_FILE = 'sqlite:///music-app-test.db'

@pytest.fixture
def database_engine():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_FILE)
    metadata.create_all(engine)  # Conditionally create database tables.
    for table in reversed(metadata.sorted_tables):  # Remove any data from the tables.
        engine.execute(table.delete())
    map_model_to_tables()
    # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    # Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
    repo_instance = database_repository.SqlAlchemyRepository(session_factory)
    database_mode = True
    repository_populate.populate(str(TEST_ALBUMS_PATH_LIMITED), str(TEST_TRACKS_PATH_LIMITED), repo_instance, database_mode)
    repo_instance.add_user('man', 'GOODpassword2134124')
    repo_instance.add_user('woman', 'GOODpassword2134144')
    yield engine
    metadata.drop_all(engine)

@pytest.fixture
def session_factory():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables()
    # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    # Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
    repo_instance = database_repository.SqlAlchemyRepository(session_factory)
    database_mode = True
    repository_populate.populate(str(TEST_ALBUMS_PATH), str(TEST_TRACKS_PATH), repo_instance, database_mode)
    repo_instance.add_user('man', 'GOODpassword2134124')
    repo_instance.add_user('woman', 'GOODpassword2134144')
    yield session_factory
    metadata.drop_all(engine)

@pytest.fixture
def empty_session():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)

    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables()
    session_factory = sessionmaker(bind=engine)
    yield session_factory()
    metadata.drop_all(engine)

