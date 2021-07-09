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
    location: str
    group: int


class Tournament():
    """Round robin schedule."""

    def __init__(self, teams, locations=None, min_group_size=3):
        """Init tournament."""
        self.teams = teams
        if locations:
            self.locations = locations
        else:
            self.locations = [f"Field {x+1}" for x in range(len(teams))]
        self.min_group_size = min_group_size

    def draw(self):
        """Order teams randomly."""
        random.shuffle(self.teams)

    @property
    def num_of_groups(self):
        """Return number of groups."""
        num_of_groups = 1

        while len(self.teams) >= num_of_groups*2 * self.min_group_size:
            num_of_groups *= 2

        return num_of_groups

    @property
    def groups(self):
        """Return list of groups. Each group contains list of teams."""
        n_of_teams = len(self.teams)

        groups = list()
        team_index = 0
        for group_index in range(0, self.num_of_groups):
            # Decide group size
            if group_index < n_of_teams % self.num_of_groups:
                group_size = n_of_teams // self.num_of_groups + 1
            else:
                group_size = n_of_teams // self.num_of_groups

            # Add group to list
            groups.append({
                'number': group_index+1,
                'teams': self.teams[team_index:team_index+group_size]
            })

            team_index += group_size

        return groups

    @property
    def matches(self):
        """Create list of matches."""
        matches = list()
        location_index = 0
        for group in self.groups:
            for field in GROUP_MATCHES[len(group['teams'])]:
                round_ = 1
                for match in field:
                    matches.append(
                        Match(group['teams'][match[0]],
                              group['teams'][match[1]],
                              round_,
                              self.locations[location_index],
                              group['number'])
                    )
                    round_ += 1
                location_index += 1

        return matches


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
    tournament = Tournament(teams, locations)
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
