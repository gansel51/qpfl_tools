"""
QPFL Schedule Generator
"""

import random
import time


class ScheduleGenerator:
    """
    QPFL schedule geneation class. Run this class via the controller method.
    """

    def __init__(self):
        """
        Initialization for the class, including maximum times playing a specific opponent,
        a list of teams, and the schedule.
        """
        self.max_games_against_opponent = 2
        self.teams = [
            "Griffin",
            "Ryan",
            "Kaminska",
            "Reardon",
            "Stephen",
            "Tim/Spencer",
            "Joe Kuhl",
            "Joe Ward",
            "Bill",
            "Arnav",
        ]
        self.team_schedule = {
            "Griffin": [],
            "Ryan": [],
            "Kaminska": [],
            "Reardon": [],
            "Stephen": [],
            "Tim/Spencer": [],
            "Joe Kuhl": [],
            "Joe Ward": [],
            "Bill": [],
            "Arnav": [],
        }
        self.rivals = {
            "Griffin": "Ryan",
            "Ryan": "Griffin",
            "Reardon": "Kaminska",
            "Kaminska": "Reardon",
            "Bill": "Joe Kuhl",
            "Joe Kuhl": "Bill",
            "Arnav": "Stephen",
            "Stephen": "Arnav",
            "Tim/Spencer": "Joe Ward",
            "Joe Ward": "Tim/Spencer",
        }
        self.win_percentage_opponent = {
            "Griffin": None,
            "Ryan": None,
            "Kaminska": None,
            "Reardon": None,
            "Joe Kuhl": None,
            "Joe Ward": None,
            "Bill": None,
            "Arnav": None,
        }
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
        week_matchups = []
        available_teams = self.teams.copy()
        # if week == 5:
        #     rivalry_week = self._rivalry_week(week)
        #     return rivalry_week
        for team in self.teams:
            matchup_works = False
            infinite_loop_check = 0
            # Moves on if team already in a matchup for this week
            if team not in available_teams:
                continue
            while not matchup_works:
                week_schedule_accepted = True
                # loop check and week schedule check
                infinite_loop_check += 1
                # choose opponent and create/validate the matchup
                opponent = random.choice(available_teams)
                matchup = (team, opponent)
                matchup_works = self._validate_matchup(matchup, week)
                # if only two teams are left, this while can get stuck trying to create a matchup
                # this loop prevents that by breaking the while
                if infinite_loop_check > 100000:
                    week_schedule_accepted = False
                    break
            # adds matchup (if accepted) to week matchups and all matchups
            # removes teams in a matchup from available list
            if week_schedule_accepted:
                self.all_matchups.append(matchup)
                week_matchups.append((team, opponent))
                available_teams.remove(team)
                available_teams.remove(opponent)
                week_schedule_accepted = True if len(available_teams) == 0 else False
        # adds full week schedule to year schedule dictionary
        if week_schedule_accepted:
            self.schedule[f"Week {str(week)}"] = week_matchups
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
        # self.max_games_against_opponent = 1 if week < 10 else 2
        self.max_games_against_opponent = 2
        matchup_total = 0
        reversed_matchup = (matchup[1], matchup[0])
        # ensure teams don't play themselves and don't play more than max_games_against_opponent
        if matchup[0] != matchup[1]:
            if week < 5:
                for rival in self.rivals:
                    rival_match = (rival, self.rivals[rival])
                    if matchup == (rival_match or reversed_matchup):
                        return False
            matchup_total = self.all_matchups.count(matchup) + self.all_matchups.count(reversed_matchup)
            matchup_worked = True if matchup_total < self.max_games_against_opponent else False
            return matchup_worked
        else:
            return False

    def _rivalry_week(self, week: int):
        """
        Helper method to add rivalry week into the QPFL Season

        Args:
            week (int): Week of rivalry week

        Returns:
            bool: True if worked, False if Exception
        """
        try:
            week_matchups = []
            rivals = {
                "Griffin": "Ryan",
                "Reardon": "Kaminska",
                "Bill": "Joe Kuhl",
                "Arnav": "Stephen",
                "Tim/Spencer": "Joe Ward",
            }
            for key in rivals:
                # create rival matchup
                rival_matchup = (key, rivals[key])
                week_matchups.append(rival_matchup)
            for matchup in list(set(week_matchups)):
                self.all_matchups.append(matchup)
            self.schedule[f"Rivalry Week {str(week)}"] = week_matchups
            return True
        except Exception:
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
            with open("generated_schedule/schedule.txt", "w") as f:
                for key, value in schedule.items():
                    f.write("%s:%s\n\n" % (key, value))
            return True
        except Exception:
            return False

    def _calculate_strength_of_schedule(self):
        """
        Helper method to calculate the strength of schedule for each team.

        Returns:
            dict: Output dictionary keyed by team with their strength of schedule in a string sentence
        """
        # 2021 regular season scores
        team_win_percentages = {
            "Griffin": 0.6429,
            "Ryan": 0.5714,
            "Kaminska": 0.4286,
            "Reardon": 0.6429,
            "Joe Kuhl": 0.4286,
            "Joe Ward": 0.2857,
            "Bill": 0.4286,
            "Arnav": 0.5,
        }
        for matchup in self.all_matchups:
            # create team schedules
            self.team_schedule[matchup[0]].append(matchup[1])
            self.team_schedule[matchup[1]].append(matchup[0])
        for team in self.team_schedule:
            total_win_percentage = 0
            opponent_count = 0
            for opponent in self.team_schedule[team]:
                # confirm every opponent has a winning percentage to use
                if opponent not in ["Tim/Spencer", "Stephen"]:
                    opponent_count += 1
                    # average opponent winning percentages
                    total_win_percentage += team_win_percentages[opponent]
            team_adj_win_perc = total_win_percentage / opponent_count
            self.win_percentage_opponent[team] = team_adj_win_perc
            output_strength_of_schedule = {}
        # sort the strength of schedules
        for team in self.win_percentage_opponent:
            hardest_schedule = {
                key: rank
                for rank, key in enumerate(
                    sorted(self.win_percentage_opponent, key=self.win_percentage_opponent.get, reverse=True),
                    1,
                )
            }
            # create string output
            for team in hardest_schedule:
                if hardest_schedule[team] == 1:
                    string_ranking = ""
                elif hardest_schedule[team] == 2:
                    string_ranking = " 2nd"
                elif hardest_schedule[team] == 3:
                    string_ranking = " 3rd"
                else:
                    string_ranking = f" {hardest_schedule[team]}th"
                output_strength_of_schedule[
                    team
                ] = f"{team} has the{string_ranking} hardest schedule with an opponent winning percentage of {round(self.win_percentage_opponent[team], 3)}"
        # output strings to file
        with open("generated_schedule/strength_of_schedule.txt", "w") as f:
            for team in hardest_schedule:
                f.write("%s\n" % (output_strength_of_schedule[team]))
        return output_strength_of_schedule

    def _validate_output(self):
        """
        Double checks that each matchup only occurs maximum of one time

        Returns:
            bool: True if successful, False otherwise
        """
        matchups_list = []
        for matchup in self.all_matchups:
            if matchup[0] == matchup[1]:
                return False
            else:
                matchup_count = self.all_matchups.count(matchup) + self.all_matchups.count(reversed(matchup))
                matchups_list.append(f"{matchup} plays {matchup_count} times")
        matchups_list = list(set(matchups_list))
        with open("generated_schedule/validate_schedule.txt", "w") as f:
            for listed_matchup in sorted(matchups_list):
                f.write("%s\n" % (listed_matchup))
        return True

    def gen_schedule(self):
        """
        Controller method to run the class
        """
        current_week = 1
        counter = 0
        correct_schedule = False
        # generate schedule iterating by week
        while current_week < 17:
            if counter < 10 and current_week == 16:
                correct_schedule = True
                break
            correct_schedule = 0
            counter += 1
            print(f"Attempt {counter} for week {current_week}")
            indicator = self.generate_weekly_schedule(current_week)
            # only incremement the week if the schedule was accepted to ensure each week gets a schedule
            if indicator:
                print(f"Week {current_week} generated!")
                current_week += 1
                counter = 0
            if counter == 10:
                correct_schedule = False
                break
        # write the schedule to a txt file
        if not correct_schedule:
            self.schedule = {}
            self.all_matchups = []
        return correct_schedule

    def controller(self):
        start_time = time.time()
        correct_schedule = False
        count = 0
        while not correct_schedule:
            count += 1
            print(f"Schedule Attempt {count}")
            current_time = time.time()
            execution_time = round((current_time - start_time) / 60, 2)
            print(f"Total Execution Time: {execution_time} min")
            correct_schedule = self.gen_schedule()
        self._validate_output()
        self._output_schedule()
        self._calculate_strength_of_schedule()
        final_time = time.time() - start_time
        print(f"Executed with time {final_time}")


if __name__ == "__main__":
    SG = ScheduleGenerator()
    SG.controller()
