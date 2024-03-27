import pytest

from flask import session


def test_register(client):
    # Check that we retrieve the register page.
    response_code = client.get('/authentication/register').status_code
    assert response_code == 200

    # Check that we can register a user successfully, supplying a valid user name and password.
    response = client.post(
        '/authentication/register',
        data={'user_name': 'gmichael', 'password': 'CarelessWhisper1984'}
    )
    assert response.headers['Location'] == '/authentication/login'


@pytest.mark.parametrize(('user_name', 'password', 'message'), (
        ('', '', b'Your user name is required'),
        ('cj', '', b'Your user name is too short'),
        ('test', '', b'Your password is required'),
        ('test', 'test', b'Your password must be at least 8 characters, and contain an upper case letter,\
            a lower case letter and a digit'),
        ('thorke', 'Test#6^0', b'Your user name is already taken - please supply another'),
))
def test_register_with_invalid_input(client, user_name, password, message):
    # Check that attempting to register with invalid combinations of user name and password generate appropriate error
    # messages.
    old = client.post(
        '/authentication/register',
        data={'user_name': 'thorke', 'password': 'Password1'}
    )

    response = client.post(
        '/authentication/register',
        data={'user_name': user_name, 'password': password}
    )
    assert message in response.data


def test_login(client, auth):
    client.post(
        '/authentication/register',
        data={'user_name': 'logintest', 'password': 'Password1'}
    )

    # Check that we can retrieve the login page.
    status_code = client.get('/authentication/login').status_code
    assert status_code == 200

    # Check that a successful login generates a redirect to the homepage.
    response = client.post(
        '/authentication/login',
        data={'user_name': 'logintest', 'password': 'Password1'}
    )

    assert response.headers['Location'] == '/'

    # # Check that a session has been created for the logged-in user.
    with client:
        client.get('/')
        assert session['user_name'] == 'logintest'


def test_logout(client, auth):
    # register a user.
    client.post(
        '/authentication/register',
        data={'user_name': 'logintest', 'password': 'Password1'}
    )
    # Login
    client.post(
        '/authentication/login',
        data={'user_name': 'logintest', 'password': 'Password1'}
    )

    with client:
        client.get('/')
        assert session['user_name'] == 'logintest'

    client.get(
        '/authentication/logout',
    )

    with client:
        client.get('/')
        assert 'user_name' not in session


def test_tracks(client):
    # Check that we can retrieve the tracks page.
    response = client.get('/tracks')
    assert response.status_code == 200

    # check tracks display
    assert b'Food' in response.data
    assert b'Electric Ave' in response.data
    assert b'This World' in response.data


def test_albums(client):
    # Check that we can retrieve the albums page.
    response = client.get('/albums')
    assert response.status_code == 200

    # check albums display
    assert b'AWOL - A Way Of Life' in response.data
    assert b'Niris' in response.data
    assert b'unreleased demo' in response.data

    # Check we can successfully filter tracks by albums
    response_filter = client.get('/tracks?album_id=60')
    assert response.status_code == 200

    assert b'CandyAss' in response_filter.data
    assert b'Ohio' in response_filter.data
    assert b'AWOL' not in response_filter.data


def test_genres(client):
    # Check that we can retrieve the genres page.
    response = client.get('/genres')
    assert response.status_code == 200

    # check genres display
    assert b'Blues' in response.data
    assert b'Jazz' in response.data
    assert b'Rock' in response.data

    # Check we can successfully filter tracks by genre
    response_filter = client.get('/tracks?genre_id=10')
    assert response.status_code == 200

    assert b'Freeway' in response_filter.data
    assert b'Hrz' in response_filter.data
    assert b'AWOL' not in response_filter.data


def test_artists(client):
    # Check that we can retrieve the genres page.
    response = client.get('/artists')
    assert response.status_code == 200

    # check genres display
    assert b'Airway' in response.data
    assert b'Cheap Time' in response.data
    assert b'AWOL' in response.data

    # Check we can successfully filter tracks by artist
    response_filter = client.get('/tracks?artist_id=53')
    assert response.status_code == 200

    assert b'Side A' in response_filter.data
    assert b'Side A' in response_filter.data
    assert b'AWOL' not in response_filter.data