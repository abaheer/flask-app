from flask import Blueprint, request, render_template, redirect, url_for, session
from datetime import date
import music.adapters.repository as repo
import music.tracks.services as services

from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

from music.auth.auth import login_required

# Configure Blueprint.
tracks_blueprint = Blueprint('tracks_bp', __name__)


@tracks_blueprint.route('/tracks', methods=['GET'])
def display_tracks():
    # Generate the webpage to display the tracks.

    tracks_per_page = 15
    cursor = request.args.get('cursor')
    album_id = request.args.get('album_id')
    artist_id = request.args.get('artist_id')
    genre_id = request.args.get('genre_id')

    if cursor is None:
        # No cursor query parameter, so initialise cursor to start at the beginning.
        cursor = 0
    else:
        # Convert cursor from string to int.
        cursor = int(cursor)

    next_track = None
    prev_track = None

    if cursor > 0:
        # There are preceding articles, so generate URLs for the 'previous' and 'first' navigation buttons.
        prev_track = url_for('tracks_bp.display_tracks', cursor=cursor - tracks_per_page,
                             album_id=album_id, artist_id=artist_id, genre_id=genre_id)

    # generate a list of all eligible tracks
    all_tracks = services.all_tracks(repo.repo_instance, cursor, album_id, artist_id, genre_id)

    if cursor + tracks_per_page < len(all_tracks):
        # There are further articles, so generate URLs for the 'next' and 'last' navigation buttons.
        next_track = url_for('tracks_bp.display_tracks', cursor=cursor + tracks_per_page,
                             album_id=album_id, artist_id=artist_id, genre_id=genre_id)

    return render_template(
        'tracks/tracks.html',
        list_of_tracks=services.get_tracks(repo.repo_instance, cursor, album_id, artist_id, genre_id),
        prev_track=prev_track,
        next_track=next_track
    )


@tracks_blueprint.route('/albums', methods=['GET'])
def display_albums():
    # Generate the webpage to display the albums.

    albums_per_page = 15
    cursor = request.args.get('cursor')

    if cursor is None:
        # No cursor query parameter, so initialise cursor to start at the beginning.
        cursor = 0
    else:
        # Convert cursor from string to int.
        cursor = int(cursor)

    next_album = None
    prev_album = None

    if cursor > 0:
        # There are preceding articles, so generate URLs for the 'previous' and 'first' navigation buttons.
        prev_album = url_for('tracks_bp.display_albums', cursor=cursor - albums_per_page)

    all_albums = services.all_albums(repo.repo_instance)

    if cursor + albums_per_page < len(all_albums):
        # There are further articles, so generate URLs for the 'next' and 'last' navigation buttons.
        next_album = url_for('tracks_bp.display_albums', cursor=cursor + albums_per_page)

    return render_template(
        'tracks/albums.html',
        list_of_albums=services.get_albums(repo.repo_instance, cursor),
        prev_album=prev_album,
        next_album=next_album
    )


@tracks_blueprint.route('/artists', methods=['GET'])
def display_artists():
    # Generate the webpage to display the artists.

    items_per_page = 14
    cursor = request.args.get('cursor')

    if cursor is None:
        # No cursor query parameter, so initialise cursor to start at the beginning.
        cursor = 0
    else:
        # Convert cursor from string to int.
        cursor = int(cursor)

    next_artists = None
    prev_artists = None

    if cursor > 0:
        # There are preceding articles, so generate URLs for the 'previous' and 'first' navigation buttons.
        prev_artists = url_for('tracks_bp.display_artists', cursor=cursor - items_per_page)

    all_artists = services.all_artists(repo.repo_instance)

    if cursor + items_per_page < len(all_artists):
        # There are further articles, so generate URLs for the 'next' and 'last' navigation buttons.
        next_artists = url_for('tracks_bp.display_artists', cursor=cursor + items_per_page)

    return render_template(
        'tracks/artists.html',
        list_of_artists=services.get_artists(repo.repo_instance, cursor),
        prev_artists=prev_artists,
        next_artists=next_artists
    )


@tracks_blueprint.route('/genres', methods=['GET'])
def display_genres():
    # Generate the webpage to display the genres.

    items_per_page = 14
    cursor = request.args.get('cursor')

    if cursor is None:
        # No cursor query parameter, so initialise cursor to start at the beginning.
        cursor = 0
    else:
        # Convert cursor from string to int.
        cursor = int(cursor)

    next_genres = None
    prev_genres = None

    if cursor > 0:
        # There are preceding articles, so generate URLs for the 'previous' and 'first' navigation buttons.
        prev_genres = url_for('tracks_bp.display_genres', cursor=cursor - items_per_page)

    all_genres = services.all_genres(repo.repo_instance)

    if cursor + items_per_page < len(all_genres):
        # There are further articles, so generate URLs for the 'next' and 'last' navigation buttons.
        next_genres = url_for('tracks_bp.display_genres', cursor=cursor + items_per_page)

    return render_template(
        'tracks/genres.html',
        list_of_genres=services.get_genres(repo.repo_instance, cursor),
        prev_genres=prev_genres,
        next_genres=next_genres
    )


# @tracks_blueprint.route('/comment', methods=['GET', 'POST'])
# @login_required
# def comment_on_track():
#     # Obtain the user name of the currently logged in user.
#     user_name = session['user_name']
#
#     # Create form. The form maintains state, e.g. when this method is called with a HTTP GET request and populates
#     # the form with an article id, when subsequently called with a HTTP POST request, the article id remains in the
#     # form.
#     form = CommentForm()
#
#     if form.validate_on_submit():
#         # Successful POST, i.e. the comment text has passed data validation.
#         # Extract the article id, representing the commented article, from the form.
#         track_id = int(form.track_id.data)
#
#         # Use the service layer to store the new comment.
#         services.add_comment(track_id, form.comment.data, user_name, repo.repo_instance)
#
#         # Retrieve the article in dict form.
#         track = services.get_track(track_id, repo.repo_instance)
#
#         # Cause the web browser to display the page of all articles that have the same date as the commented article,
#         # and display all comments, including the new comment.
#         return redirect(url_for('tracks_bp.tracks', view_comments_for=track_id))
#
#     if request.method == 'GET':
#         # Request is a HTTP GET to display the form.
#         # Extract the article id, representing the article to comment, from a query parameter of the GET request.
#         track_id = int(request.args.get('track'))
#
#         # Store the article id in the form.
#         form.track_id.data = track_id
#     else:
#         # Request is a HTTP POST where form validation has failed.
#         # Extract the article id of the article being commented from the form.
#         track_id = int(form.track_id.data)
#
#     # For a GET or an unsuccessful POST, retrieve the article to comment in dict form, and return a Web page that allows
#     # the user to enter a comment. The generated Web page includes a form object.
#     track = services.get_track(track_id, repo.repo_instance)
#     return render_template(
#         'tracks/comment_on_track.html',
#         title='Edit article',
#         track=track,
#         form=form,
#         handler_url=url_for('tracks_bp.comment_on_track'),
#     )
#
# class CommentForm(FlaskForm):
#     comment = TextAreaField('Comment', [
#         DataRequired(),
#         Length(min=4, message='Your comment is too short'),
#         ProfanityFree(message='Your comment must not contain profanity')])
#     track_id = HiddenField("track id")
#     submit = SubmitField('Submit')