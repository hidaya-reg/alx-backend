#!/usr/bin/env python3
"""
Basic Flask app with user login and preferred locale support.
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

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user(user_id: Optional[int]) -> Optional[dict]:
    """
    Retrieve a user dictionary by user_id.
    """
    return users.get(user_id)


@app.before_request
def before_request() -> None:
    """
    Find a user and set it in the global object `g`.
    """
    user_id = request.args.get('login_as')
    if user_id:
        g.user = get_user(int(user_id))
    else:
        g.user = None


@babel.localeselector
def get_locale() -> str:
    """
    Determine the best match for the supported locales.
    The order of priority is:
    1. URL parameter
    2. User's preferred locale (if logged in)
    3. Accept-Language header from the request
    4. Default locale ('en')
    """
    # Check URL parameter
    locale = request.args.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale

    # Check user's preferred locale if logged in
    if g.user and g.user.get('locale') in app.config['LANGUAGES']:
        return g.user.get('locale')

    # Check request Accept-Language header
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index() -> str:
    """
    Render the index page.
    """
    return render_template('6-index.html')


if __name__ == '__main__':
    app.run(debug=True)
