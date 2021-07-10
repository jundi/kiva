"""Start Flask application"""
from flask import Flask, request, render_template, jsonify
from kiva.tournament import Tournament


def create_app():
    """Create flask application."""
    app = Flask(__name__)

    tournaments = []

    @app.route('/create', methods=['POST', 'GET'])
    def _create_tournament():
        if request.method == 'GET':
            return render_template('create.html')

        teams = request.form['teams'].splitlines()
        tournaments.append(Tournament(teams))
        return jsonify(teams)

    @app.route('/schedule/<int:tournament_id>', methods=['GET'])
    def _view_tournament_schedule(tournament_id):
        return render_template('view_schedule.html',
                               matches=tournaments[tournament_id].matches)

    return app


if __name__ == "__main__":
    create_app().run()
