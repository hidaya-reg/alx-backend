#!/usr/bin/env python3
'''Task 7: Infer appropriate time zone
'''

from typing import Dict, Union
from flask import Flask, render_template, request, g
from flask_babel import Babel
import pytz


class Config:
    '''Configuration class for the Flask app and Babel'''

    DEBUG = True
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)

# Mock user database
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user() -> Union[Dict, None]:
    """Retrieves a user based on the `login_as` query parameter."""
    login_id = request.args.get('login_as')
    if login_id:
        return users.get(int(login_id))
    return None


@app.before_request
def before_request() -> None:
    """Sets a user object globally before each request."""
    g.user = get_user()


@babel.localeselector
def get_locale() -> str:
    """Determines the best match for the user's locale."""
    # Check for locale in URL parameters
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale
    # Check for locale from the user's settings
    if g.user and g.user.get('locale') in app.config["LANGUAGES"]:
        return g.user['locale']
    # Check for locale from the request headers
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone() -> str:
    """Determines the best match for the user's timezone."""
    # Check for timezone in URL parameters
    timezone = request.args.get('timezone', '').strip()
    # Use the user's timezone if available
    if not timezone and g.user:
        timezone = g.user.get('timezone', '')
    # Validate the timezone or fallback to default
    try:
        if timezone:
            return pytz.timezone(timezone).zone
    except pytz.exceptions.UnknownTimeZoneError:
        pass
    # Default to UTC if no valid timezone found
    return app.config['BABEL_DEFAULT_TIMEZONE']


@app.route('/')
def index() -> str:
    """Renders the homepage."""
    return render_template('7-index.html')


if __name__ == "__main__":
    app.run()
