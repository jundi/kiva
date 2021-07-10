"""Start Flask application"""
import uuid
from flask import Flask, request, render_template, redirect, url_for
from kiva.tournament import Tournament


def create_app():
    """Create flask application."""
    app = Flask(__name__)

    tournaments = dict()

    @app.route('/create', methods=['POST', 'GET'])
    def _create():
        if request.method == 'GET':
            return render_template('create.html', url=url_for('_create'))

        teams = request.form['teams'].splitlines()
        identifier = uuid.uuid4().hex[:6]
        tournaments[identifier] = Tournament(teams)

        return redirect(f'/schedule/{identifier}')

    @app.route('/schedule/<identifier>', methods=['GET'])
    def _schedule(identifier):
        return render_template('schedule.html',
                               schedule=tournaments[identifier].schedule)

    return app


if __name__ == "__main__":
    create_app().run()
