"""Start Flask application"""
import uuid
from flask import Flask, request, render_template, redirect, url_for, abort
import werkzeug
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

        # Remove empty teams
        teams = [team for team in teams if team]

        if len(teams) < 3:
            abort(400, "At least three teams is rquired.")

        # Create new tournament
        identifier = uuid.uuid4().hex[:6]
        tournaments[identifier] = Tournament(teams)

        # Forward to groups
        return redirect(url_for('_groups', identifier=identifier))

    @app.route('/tournaments/', methods=['GET'])
    def _tournaments():
        return render_template('tournaments.html',
                               tournaments=tournaments)

    @app.route('/tournaments/<identifier>/draw', methods=['POST'])
    def _draw(identifier):

        tournaments[identifier].draw()

        # Forward to groups
        return redirect(url_for('_groups', identifier=identifier))

    @app.route('/tournaments/<identifier>/groups', methods=['GET'])
    def _groups(identifier):
        return render_template('groups.html',
                               groups=tournaments[identifier].groups,
                               identifier=identifier)

    @app.route('/tournaments/<identifier>/schedule', methods=['GET'])
    def _schedule(identifier):
        return render_template('schedule.html',
                               schedule=tournaments[identifier].schedule,
                               identifier=identifier)

    @app.errorhandler(werkzeug.exceptions.HTTPException)
    def _handle_exception(exception):
        """Return nice error page."""
        return render_template('error.html',
                               code=exception.code,
                               name=exception.name,
                               description=exception.description)

    return app


if __name__ == "__main__":
    create_app().run()
