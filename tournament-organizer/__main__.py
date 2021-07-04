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

        groups = [[] for group in range(0, n_of_groups)]
        teams = copy.copy(self.teams)
        while teams:
            for group in range(0, n_of_groups):
                groups[group] += [teams.pop()]
                if not teams:
                    break

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
