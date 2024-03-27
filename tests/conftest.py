import pytest

from music import create_app
from music.adapters import repository_populate
from music.adapters.memory_repository import MemoryRepository

from utils import get_project_root

# the csv files in the test folder are different from the csv files in the covid/adapters/data folder!
# tests are written against the csv files in tests, this data path is used to override default path for testing
TEST_ALBUMS_PATH = get_project_root() / "tests" / "data" / "raw_albums_excerpt.csv"
TEST_TRACKS_PATH = get_project_root() / "tests" / "data" / "raw_tracks_excerpt.csv"


@pytest.fixture
def in_memory_repo():
    repo = MemoryRepository()
    repository_populate.populate(str(TEST_ALBUMS_PATH), str(TEST_TRACKS_PATH), repo, False)
    repo.add_user('thorke', 'GoodPassword100')
    return repo


@pytest.fixture
def client():
    my_app = create_app({
        'TESTING': True,                                # Set to True during testing.
        'REPOSITORY': 'memory',
        'TEST_ALBUMS_PATH': str(TEST_ALBUMS_PATH),               # Path for loading test data into the repository.
        'TEST_TRACKS_PATH': str(TEST_TRACKS_PATH),
        'WTF_CSRF_ENABLED': False                       # test_client will not send a CSRF token, so disable validation.
    })

    return my_app.test_client()


class AuthenticationManager:
    def __init__(self, client):
        self.__client = client

    def register(self, user_name='thorke', password='cLQ^C#oFXloS'):
        return self.__client.post(
            '/authentication/register',
            data={'user_name': user_name, 'password': password}
        )

    def login(self, user_name='thorke', password='cLQ^C#oFXloS'):
        return self.__client.post(
            '/authentication/login',
            data={'user_name': user_name, 'password': password}
        )

    def logout(self):
        return self.__client.get('/authentication/logout')


@pytest.fixture
def auth(client):
    return AuthenticationManager(client)
