from flask import Blueprint, render_template

import music.adapters.repository as repo
import music.tracks.services as services

home_blueprint = Blueprint(
    'home_bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():

    # return random tracks to display on the homepage
    return render_template(
        'home/home.html',
        home_tracks=services.get_home(repo.repo_instance),
    )
