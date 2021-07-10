"""Start Flask application"""
from flask import Flask, request, render_template, jsonify
from kiva.tournament import Tournament


def create_app():
    """Create flask application."""
    app = Flask(__name__)

    tournaments = []

    @app.route('/create', methods=['POST', 'GET'])
    def _create():
        if request.method == 'GET':
            return render_template('create.html')

        teams = request.form['teams'].splitlines()
        tournaments.append(Tournament(teams))
        return jsonify(teams)

    @app.route('/schedule/<int:tournament_id>', methods=['GET'])
    def _schedule(tournament_id):
        return render_template('schedule.html',
                               schedule=tournaments[tournament_id].schedule)

    return app


if __name__ == "__main__":
    create_app().run()
