"""Script that creates round-robin schedule."""
import dataclasses
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

    @property
    def schedule(self):
        """List of matches for each location."""
        schedule = list()
        for location in self.locations:
            matches = [match for match in self.matches
                       if match.location == location]
            # skip locations that do not have any matches
            if matches:
                schedule.append([match for match in self.matches
                                 if match.location == location])

        return schedule
