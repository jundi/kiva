"""Script that creates round-robin schedule."""
import argparse
import copy
import pathlib
import random


class Schdedule():
    """Round robin schedule."""

    def __init__(self, teams):
        self.teams = teams

    def draw(self):
        """Order teams randomly."""
        random.shuffle(self.teams)

    def groups(self):
        """Return list of groups. Each group contains list of teams."""
        n_of_teams = len(self.teams)
        n_of_groups = n_of_teams // 3

        groups = list()
        team_index = 0
        for group_index in range(0, n_of_groups):
            if group_index < n_of_teams % n_of_groups:
                group_size = n_of_teams // n_of_groups + 1
            else:
                group_size = n_of_teams // n_of_groups

            groups.append(self.teams[team_index:team_index+group_size])
            team_index += group_size

        return groups


def main():
    """Print round-robin schedule."""
    parser = argparse.ArgumentParser()
    parser.add_argument('teams',
                        help="Textfile that contains list of teams")
    args = parser.parse_args()

    # Read teams
    teams_file = pathlib.Path(args.teams)
    teams = teams_file.read_text().splitlines()

    # Print groups
    schedule = Schdedule(teams)
    schedule.draw()
    print(schedule.groups())


if __name__ == "__main__":
    main()
