#!/usr/bin/env python3
"""
Basic Flask app with user login simulation and localization
"""

from flask import Flask, render_template, request, g
from flask_babel import Babel, _
from typing import Optional


class Config:
    """
    Configuration for Flask-Babel.
    """

    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)

# Mock user data
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user() -> Optional[dict]:
    """
    Returns a user dictionary if the user ID is found, None otherwise.
    """
    try:
        user_id = int(request.args.get('login_as'))
        return users.get(user_id)
    except (TypeError, ValueError):
        return None


@app.before_request
def before_request() -> None:
    """
    Find the user if any, and set it as a global variable in flask.g.
    """
    g.user = get_user()


@babel.localeselector
def get_locale() -> str:
    """
    Select locale based on URL parameter or Accept-Language header.
    """
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale
    if g.user and g.user.get('locale') in app.config['LANGUAGES']:
        return g.user['locale']
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index() -> str:
    """
    Render the index page.
    """
    return render_template('5-index.html')


if __name__ == '__main__':
    app.run(debug=True)
