"""Script that creates round-robin schedule."""
import argparse
import pathlib

import kiva.tournament


def main():
    """Print round-robin schedule."""
    parser = argparse.ArgumentParser()
    parser.add_argument('teams',
                        help="Textfile that contains list of teams")
    parser.add_argument('--locations',
                        help="Textfile that contains locations for matches")
    parser.add_argument('--draw',
                        help="Teams in random order",
                        action="store_true")
    args = parser.parse_args()

    # Read teams
    teams_file = pathlib.Path(args.teams)
    teams = teams_file.read_text().splitlines()

    # Read locations
    if args.locations:
        locations = pathlib.Path(args.locations).read_text().splitlines()
    else:
        locations = None

    # Create match schedule
    tournament = kiva.tournament.Tournament(teams, locations)
    if args.draw:
        tournament.draw()
        draw_file_index = 0
        while True:
            draw_file = pathlib.Path(
                args.teams + '.draw' + str(draw_file_index)
            )
            if not draw_file.exists():
                break
            draw_file_index += 1
        draw_file.write_text("\n".join(tournament.teams))
        print(f"Teams saved to {draw_file}")

    # Print groups
    for group in tournament.groups:
        print(f"\nGROUP {group['number']}")
        for team in group['teams']:
            print(team)

    # Print schedule
    for match in tournament.matches:
        if match.round_ == 1:
            print(f'\nGROUP {match.group}, {match.location}')
        print(f'{match.round_}: {match.team_a} - {match.team_b}')


if __name__ == "__main__":
    main()
