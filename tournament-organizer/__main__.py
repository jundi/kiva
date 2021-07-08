"""Script that creates round-robin schedule."""
import argparse
import dataclasses
import pathlib
import random


# Order of matches in group for each possible size of group.
GROUP_MATCHES = {
    3: [
        [(0, 1), (0, 2), (1, 2)]
    ],
    4: [
        [(2, 3), (0, 2), (0, 3)],
        [(0, 1), (1, 3), (1, 2)]
    ],
    5: [
        [(2, 3), (0, 4), (0, 3), (0, 2), (1, 3)],
        [(0, 1), (1, 2), (1, 4), (3, 4), (2, 4)]
    ],
    6: [
        [(2, 3), (0, 4), (0, 3), (0, 2), (1, 3)],
        [(0, 1), (1, 2), (1, 4), (3, 4), (2, 4)],
        [(4, 5), (3, 5), (2, 5), (1, 5), (0, 5)]
    ],
}


@dataclasses.dataclass
class Match:
    """Match class."""
    team_a: str
    team_b: str
    round_: int
    field: int
    group: int


class Tournament():
    """Round robin schedule."""

    def __init__(self, teams, min_group_size=3):
        self.teams = teams
        self.min_group_size = min_group_size

    def draw(self):
        """Order teams randomly."""
        random.shuffle(self.teams)

    @property
    def num_of_groups(self):
        """Number of groups."""
        num_of_groups = 1

        while len(self.teams) >= num_of_groups*2 * self.min_group_size:
            num_of_groups *= 2

        return num_of_groups

    @property
    def groups(self):
        """Return list of groups. Each group contains list of teams."""
        n_of_teams = len(self.teams)

        groups = dict()
        team_index = 0
        for group_index in range(0, self.num_of_groups):
            if group_index < n_of_teams % self.num_of_groups:
                group_size = n_of_teams // self.num_of_groups + 1
            else:
                group_size = n_of_teams // self.num_of_groups

            groups[group_index] = self.teams[team_index:team_index+group_size]
            team_index += group_size

        return groups

    @property
    def matches(self):
        """Create list of matches."""

        matches = list()
        field_index = 0
        for group_index, group_teams in self.groups.items():
            for field in GROUP_MATCHES[len(group_teams)]:
                round_ = 0
                for match in field:
                    matches.append(
                        Match(group_teams[match[0]],
                              group_teams[match[1]],
                              round_,
                              field_index,
                              group_index)
                    )
                    round_ += 1
                field_index += 1

        return matches


def main():
    """Print round-robin schedule."""
    parser = argparse.ArgumentParser()
    parser.add_argument('teams',
                        help="Textfile that contains list of teams")
    args = parser.parse_args()

    # Read teams
    teams_file = pathlib.Path(args.teams)
    teams = teams_file.read_text().splitlines()

    # Create match schedule
    tournament = Tournament(teams)
    tournament.draw()

    # Print groups
    for group_index, teams in tournament.groups.items():
        print(f"\nGROUP {group_index+1}")
        for team in teams:
            print(team)

    # Print schedule
    for match in tournament.matches:
        if match.round_ == 0:
            print(f'\nGROUP {match.group+1}, FIELD {match.field+1}')
        print(f'{match.round_+1}: {match.team_a} - {match.team_b}')


if __name__ == "__main__":
    main()
