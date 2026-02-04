"""Start Flask application"""
import json
import os
from pathlib import Path
import uuid
from flask import Flask, request, render_template, redirect, url_for, abort
import werkzeug
from kiva.tournament import Tournament


def create_app(instance_path=None):
    """Create flask application."""
    instance_path = instance_path or os.environ.get("KIVA_INSTANCE_PATH")
    if instance_path:
        app = Flask(__name__, instance_path=instance_path)
    else:
        app = Flask(__name__)

    # Flask provides instance_path for per-deployment data outside the code tree.
    storage_path = Path(app.instance_path) / "tournaments.json"

    def _serialize_tournament(tournament):
        return {
            "teams": tournament.teams,
            "locations": tournament.locations,
            "min_group_size": tournament.min_group_size,
        }

    def _load_tournaments():
        if not storage_path.exists():
            return {}

        with storage_path.open() as handle:
            data = json.load(handle)

        tournaments = {}
        for identifier, payload in data.items():
            tournaments[identifier] = Tournament(
                payload["teams"],
                locations=payload.get("locations"),
                min_group_size=payload.get("min_group_size", 3),
            )
        return tournaments

    def _save_tournaments(tournaments):
        storage_path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            identifier: _serialize_tournament(tournament)
            for identifier, tournament in tournaments.items()
        }
        with storage_path.open("w") as handle:
            json.dump(data, handle, indent=2, sort_keys=True)

    tournaments = _load_tournaments()

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
        _save_tournaments(tournaments)

        # Forward to groups
        return redirect(url_for('_groups', identifier=identifier))

    @app.route('/tournaments/', methods=['GET'])
    def _tournaments():
        return render_template('tournaments.html',
                               tournaments=tournaments)

    @app.route('/tournaments/<identifier>/draw', methods=['POST'])
    def _draw(identifier):

        tournaments[identifier].draw()
        _save_tournaments(tournaments)

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
