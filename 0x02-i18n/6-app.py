#!/usr/bin/env python3
"""
Task 6: Use user locale
"""

from typing import Dict, Union
from flask import Flask, render_template, request, g
from flask_babel import Babel


class Config:
    """Configuration class for the Flask application and Babel."""
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


def get_user() -> Union[Dict, None]:
    """
    Retrieves the user information based on the 'login_as' parameter in the URL.

    Returns:
        dict or None: User data if found, otherwise None.
    """
    user_id = request.args.get('login_as')
    if user_id and user_id.isdigit():
        return users.get(int(user_id))
    return None


@app.before_request
def before_request() -> None:
    """
    Runs before every request to set the global user context.
    """
    g.user = get_user()


@babel.localeselector
def get_locale() -> str:
    """
    Determines the best locale to use for the current request.

    Returns:
        str: The locale that matches best, according to the URL, user settings, or headers.
    """
    # Check if locale is provided in URL parameters
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale
    
    # Check user preferences if a user is logged in
    if g.user and g.user['locale'] in app.config['LANGUAGES']:
        return g.user['locale']
    
    # Check if locale is provided in the request headers
    header_locale = request.headers.get('locale')
    if header_locale in app.config['LANGUAGES']:
        return header_locale
    
    # Fallback to best match based on Accept-Language header
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index() -> str:
    """
    Renders the homepage.

    Returns:
        str: Rendered HTML page.
    """
    return render_template("6-index.html")


if __name__ == "__main__":
    app.run(debug=True)
