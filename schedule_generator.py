"""
QPFL Schedule Generator
"""

import random


class ScheduleGenerator:
    """
    QPFL schedule geneation class. Run this class via the controller method.
    """

    def __init__(self):
        """
        Initialization for the class, including maximum times playing a specific opponent, a list of teams, and the schedule.
        """
        self.max_games_against_opponent = 2
        self.teams = [
            "Griffin",
            "Ryan",
            "Kaminska",
            "Connor",
            "Stephen",
            "Tim/Spencer",
            "Bocki",
            "Joe",
            "Bill",
            "Arnav",
        ]
        self.schedule = {}
        self.all_matchups = []

    def generate_weekly_schedule(self, week: int) -> bool:
        """
        Method to generate the schedule for a single week

        Args:
            week (int): The week of the season for which to generate a schedule

        Returns:
            week_schedule_accepted (bool): An indicator variable to show if an acceptable schedule was generated
        """
        matchups = []
        available_teams = self.teams.copy()
        for team in self.teams:
            matchup_works = False
            infinite_loop_check = 0
            # Moves on if team already in a matchup for this week
            if team not in available_teams:
                continue
            while not matchup_works:
                # loop check and week schedule check
                week_schedule_accepted = True
                infinite_loop_check += 1
                # choose opponent and create/validate the matchup
                opponent = random.choice(available_teams)
                matchup = (team, opponent)
                matchup_works = self._validate_matchup(matchup, week)
                # if only two teams are left, this while can get stuck trying to create a matchup
                # this loop prevents that by breaking the while
                if infinite_loop_check > 30:
                    week_schedule_accepted = False
                    break
            # adds matchup (if accepted) to week matchups and all matchups
            # removes teams in a matchup from available list
            if week_schedule_accepted:
                matchups.append((team, opponent))
                available_teams.remove(team)
                available_teams.remove(opponent)
                self.all_matchups.append(matchup)
        # adds full week schedule to year schedule dictionary
        if week_schedule_accepted:
            self.schedule[f"Week {str(week)}"] = matchups
        return week_schedule_accepted

    def _validate_matchup(self, matchup: tuple, week: int) -> bool:
        """
        Helper method to validate that a matchup is acceptable. Matchup is validated by confirming that a team isn't playing itself,
        has played every team once by week 10, and hasn't played this opponent twice

        Args:
            matchup (tuple): The current matchup (team, opponent)
            week (int): The current week

        Returns:
            bool: Returns a boolean on if the matchup should be accepted, True if yes otherwise False
        """
        # set number of times a team should play another - 1 until week 10 to ensure each team plays each other team
        self.max_games_against_opponent = 1 if week < 10 else 2
        # ensure teams don't play themselves and don't play more than max_games_against_opponent
        if matchup[0] != matchup[1]:
            return True if self.all_matchups.count(matchup) < self.max_games_against_opponent else False
        else:
            return False

    def _format_output(self) -> dict:
        """
        Helper method to generate a string version of each week's schedule for human readability

        Returns:
            dict: Dictionary of schedule keyed by week with values being a string of the week's matchups
        """
        output_dict = self.schedule.copy()
        for key in output_dict:
            string_of_week = " "
            for matchup in output_dict[key]:
                string_of_matchup = str(matchup[0]) + " versus " + str(matchup[1])
                string_of_week = string_of_week + string_of_matchup + ", "
            string_of_week = string_of_week.rstrip(", ")
            output_dict[key] = string_of_week
        return output_dict

    def _output_schedule(self) -> bool:
        """
        Helper method to output the schedule to a txt file.

        Returns:
            bool: True if schedule outputted successfully, otherwise False
        """
        schedule = self._format_output()
        try:
            with open("schedule.txt", "w") as f:
                for key, value in schedule.items():
                    f.write("%s:%s\n" % (key, value))
            return True
        except Exception:
            return False

    def controller(self):
        """
        Controller method to run the class
        """
        current_week = 1
        # generate schedule iterating by week
        while current_week < 16:
            indictator = self.generate_weekly_schedule(current_week)
            # only incremement the week if the schedule was accepted to ensure each week gets a schedule
            current_week += 1 if indictator else current_week
        # write the schedule to a txt file
        self._output_schedule()


if __name__ == "__main__":
    SG = ScheduleGenerator()
    SG.controller()
