"""
QPFL Schedule Generator
"""

import random
import logging
import os
import shutil


class ScheduleGenerator:
    """
    QPFL schedule geneation class. Run this class via the controller method.
    """

    def __init__(self):
        """
        Initialization for the class, including a list of teams, rivals, and the schedule.
        """
        self.logger = logging.getLogger(name="schedule_logger")
        self.logger.info("ScheduleGenerator class initialized")
        self.teams = [
            "Griffin",
            "Ryan",
            "Kaminska",
            "Connor",
            "Stephen",
            "Tim/Spencer",
            "Joe Kuhl",
            "Joe Ward",
            "Bill",
            "Arnav",
        ]
        self.rivals = {
            "Griffin": "Ryan",
            "Ryan": "Griffin",
            "Connor": "Kaminska",
            "Kaminska": "Connor",
            "Bill": "Joe Kuhl",
            "Joe Kuhl": "Bill",
            "Arnav": "Stephen",
            "Stephen": "Arnav",
            "Tim/Spencer": "Joe Ward",
            "Joe Ward": "Tim/Spencer",
        }
        self.schedule = {}
        self.all_matchups = []
        self.previous_week = []
        # counts matchup numbers
        self.griffin = {
            "Griffin": 0,
            "Ryan": 0,
            "Kaminska": 0,
            "Connor": 0,
            "Stephen": 0,
            "Tim/Spencer": 0,
            "Joe Kuhl": 0,
            "Joe Ward": 0,
            "Bill": 0,
            "Arnav": 0,
        }
        self.ryan = {
            "Griffin": 0,
            "Ryan": 0,
            "Kaminska": 0,
            "Connor": 0,
            "Stephen": 0,
            "Tim/Spencer": 0,
            "Joe Kuhl": 0,
            "Joe Ward": 0,
            "Bill": 0,
            "Arnav": 0,
        }
        self.kaminska = {
            "Griffin": 0,
            "Ryan": 0,
            "Kaminska": 0,
            "Connor": 0,
            "Stephen": 0,
            "Tim/Spencer": 0,
            "Joe Kuhl": 0,
            "Joe Ward": 0,
            "Bill": 0,
            "Arnav": 0,
        }
        self.connor = {
            "Griffin": 0,
            "Ryan": 0,
            "Kaminska": 0,
            "Connor": 0,
            "Stephen": 0,
            "Tim/Spencer": 0,
            "Joe Kuhl": 0,
            "Joe Ward": 0,
            "Bill": 0,
            "Arnav": 0,
        }
        self.stephen = {
            "Griffin": 0,
            "Ryan": 0,
            "Kaminska": 0,
            "Connor": 0,
            "Stephen": 0,
            "Tim/Spencer": 0,
            "Joe Kuhl": 0,
            "Joe Ward": 0,
            "Bill": 0,
            "Arnav": 0,
        }
        self.tim_spencer = {
            "Griffin": 0,
            "Ryan": 0,
            "Kaminska": 0,
            "Connor": 0,
            "Stephen": 0,
            "Tim/Spencer": 0,
            "Joe Kuhl": 0,
            "Joe Ward": 0,
            "Bill": 0,
            "Arnav": 0,
        }
        self.joek = {
            "Griffin": 0,
            "Ryan": 0,
            "Kaminska": 0,
            "Connor": 0,
            "Stephen": 0,
            "Tim/Spencer": 0,
            "Joe Kuhl": 0,
            "Joe Ward": 0,
            "Bill": 0,
            "Arnav": 0,
        }
        self.joew = {
            "Griffin": 0,
            "Ryan": 0,
            "Kaminska": 0,
            "Connor": 0,
            "Stephen": 0,
            "Tim/Spencer": 0,
            "Joe Kuhl": 0,
            "Joe Ward": 0,
            "Bill": 0,
            "Arnav": 0,
        }
        self.bill = {
            "Griffin": 0,
            "Ryan": 0,
            "Kaminska": 0,
            "Connor": 0,
            "Stephen": 0,
            "Tim/Spencer": 0,
            "Joe Kuhl": 0,
            "Joe Ward": 0,
            "Bill": 0,
            "Arnav": 0,
        }
        self.arnav = {
            "Griffin": 0,
            "Ryan": 0,
            "Kaminska": 0,
            "Connor": 0,
            "Stephen": 0,
            "Tim/Spencer": 0,
            "Joe Kuhl": 0,
            "Joe Ward": 0,
            "Bill": 0,
            "Arnav": 0,
        }

    def _return_correct_team_dict(self, team: str) -> dict:
        """
        Helper method to return the correct team's dictionary

        Args:
            team (string): the name of the team for which to return the dictionary

        Returns:
            dict: dictionary of the team's schedule counts
        """
        self.logger.info("Accessing correct team dictionary")
        try:
            if team == "Griffin":
                return self.griffin
            elif team == "Ryan":
                return self.ryan
            elif team == "Kaminska":
                return self.kaminska
            elif team == "Connor":
                return self.connor
            elif team == "Stephen":
                return self.stephen
            elif team == "Tim/Spencer":
                return self.tim_spencer
            elif team == "Joe Kuhl":
                return self.joek
            elif team == "Joe Ward":
                return self.joew
            elif team == "Bill":
                return self.bill
            elif team == "Arnav":
                return self.arnav
        except Exception as e:
            self.logger.error(e)
            raise e

    def _update_correct_team_dict(self, home: str, away: str) -> bool:
        """
        Helper method to update the count of matchups against a specific opponent

        Args:
            home (str): first team in matchup
            away (str): second team in matchup
        """
        self.logger.info("Updating correct team dictionary...")
        try:
            if home == "Griffin":
                self.griffin[away] += 1
            elif home == "Ryan":
                self.ryan[away] += 1
            elif home == "Kaminska":
                self.kaminska[away] += 1
            elif home == "Connor":
                self.connor[away] += 1
            elif home == "Stephen":
                self.stephen[away] += 1
            elif home == "Tim/Spencer":
                self.tim_spencer[away] += 1
            elif home == "Joe Kuhl":
                self.joek[away] += 1
            elif home == "Joe Ward":
                self.joew[away] += 1
            elif home == "Bill":
                self.bill[away] += 1
            elif home == "Arnav":
                self.arnav[away] += 1
            self.logger.info("Updated correct team dictionary successfully")
        except Exception as e:
            self.logger.error(e)
            raise e

    def generate_weekly_schedule(self, week: int) -> bool:
        """
        Method to generate the schedule for a single week

        Args:
            week (int): The week of the season for which to generate a schedule

        Returns:
            week_schedule_accepted (bool): An indicator variable to show if an acceptable schedule was generated
        """
        self.logger.warning(f"Starting schedule generation for week {week}")
        week_matchups = []
        available_teams = self.teams.copy()
        if week == 5:
            rivalry_week = self._rivalry_week(week)
            return rivalry_week
        for team in self.teams:
            matchup_works = False
            infinite_loop_check = 0
            # Moves on if team already in a matchup for this week
            if team not in available_teams:
                continue
            while not matchup_works:
                # loop check and week schedule check
                infinite_loop_check += 1
                # choose opponent and create/validate the matchup
                opponent = random.choice(available_teams)
                matchup = (team, opponent)
                self.logger.info(f"Testing matchup {matchup}")
                matchup_works = self._validate_matchup(matchup, week)
                self.logger.info(f"Matchup {matchup} {matchup_works}")
                # if only two teams are left, this while can get stuck trying to create a matchup
                # this loop prevents that by breaking the while
                if infinite_loop_check > 10000:
                    return False
            # adds matchup (if accepted) to week matchups and all matchups
            # removes teams in a matchup from available list
            week_matchups.append((team, opponent))
            available_teams.remove(team)
            available_teams.remove(opponent)
        if len(week_matchups) == 5:
            self.logger.info("Week schedule accepted")
            self.schedule[f"Week {str(week)}"] = week_matchups
            for matchup in week_matchups:
                home = matchup[0]
                away = matchup[1]
                self._update_correct_team_dict(home=home, away=away)
                self._update_correct_team_dict(home=away, away=home)
                self.all_matchups.append(matchup)
            self.logger.info("Setting previous week variable equal to this week.")
            self.previous_week = week_matchups
            return True
        else:
            return False

    def _validate_matchup(self, matchup: tuple, week: int) -> bool:
        """
        Helper method to validate that a matchup is acceptable. Matchup is validated by confirming that a team isn't
        playing itself, has played every team once by week 10, and hasn't played this opponent twice

        Args:
            matchup (tuple): The current matchup (team, opponent)
            week (int): The current week

        Returns:
            bool: Returns a boolean on if the matchup should be accepted, True if yes otherwise False
        """
        self.logger.info("Validating the matchup")
        # set number of times a team should play another to 1 until week 10 to ensure each team plays
        # each other team to start the season
        max_games_against_opponent = 1 if week <= 9 else 2

        home = matchup[0]
        away = matchup[1]

        if matchup in self.previous_week:
            self.logger.info("Matchup failed because matchup occurred the previous week")
            return False

        # confirm team isn't playing itself or its rival before rivalry week
        if home != away:
            home_dict = self._return_correct_team_dict(team=home)
            away_dict = self._return_correct_team_dict(team=away)
            if week < 5:
                if self.rivals[home] == away:
                    self.logger.info("Matchup failed because rivals played before week 5")
                    return False
                elif self.rivals[away] == home:
                    self.logger.info("Matchup failed because rivals played before week 5")
                    return False
            matchup_total_home_away = home_dict[away]
            matchup_total_away_home = away_dict[home]
            if matchup_total_away_home == matchup_total_home_away:
                if matchup_total_away_home < max_games_against_opponent:
                    self.logger.info("Matchup validation successful")
                    return True
                else:
                    self.logger.info("Matchup failed because teams play each other more than twice")
                    return False
                self.logger.info(f"Matchup {matchup} has count: {matchup_total_away_home}")
            else:
                self.logger.error(
                    f"{home}/{away} matchup count: {home}: {matchup_total_home_away}, {away}: {matchup_total_away_home}"
                )
                raise AssertionError("Home team dict and away team dict do not match.")
        else:
            self.logger.info("Matchup failed because team is playing itself")
            return False

    def _rivalry_week(self, week: int):
        """
        Helper method to add rivalry week into the QPFL Season

        Args:
            week (int): Week of rivalry week
        """
        try:
            self.logger.info("Creating rivalry week matchups")
            week_matchups = []
            rivals = {
                "Griffin": "Ryan",
                "Connor": "Kaminska",
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
                self._update_correct_team_dict(home=matchup[0], away=matchup[1])
                self._update_correct_team_dict(home=matchup[1], away=matchup[0])
            self.schedule[f"Rivalry Week {str(week)}"] = week_matchups
            self.logger.info("Rivalry week matchups created successfully!")
            return True
        except Exception as e:
            self.logger.error(e)
            raise e

    def _format_output(self) -> dict:
        """
        Helper method to generate a string version of each week's schedule for human readability

        Returns:
            dict: Dictionary of schedule keyed by week with values being a string of the week's matchups
        """
        try:
            self.logger.info("Formatting output")
            output_dict = self.schedule.copy()
            for key in output_dict:
                string_of_week = " "
                for matchup in output_dict[key]:
                    string_of_matchup = str(matchup[0]) + " versus " + str(matchup[1])
                    string_of_week = string_of_week + string_of_matchup + ", "
                string_of_week = string_of_week.rstrip(", ")
                output_dict[key] = string_of_week
            self.logger.info("Formatted output successfully!")
            return output_dict
        except Exception as e:
            self.logger.error(e)
            raise e

    def _output_schedule(self) -> bool:
        """
        Helper method to output the schedule to a txt file.
        """
        schedule = self._format_output()
        self.logger.info("Outputting schedule")
        try:
            with open("schedule.txt", "w") as f:
                for key, value in schedule.items():
                    f.write("%s:%s\n\n" % (key, value))
            self.logger.info("Schedule outputted successfully!")
        except Exception as e:
            self.logger.error(e)
            raise e

    def _validate_output(self):
        """
        Double checks that each matchup only occurs maximum of one time

        Args:
            None
        """
        self.logger.info("Validating output")
        try:
            matchups_list = []
            for matchup in self.all_matchups:
                home = matchup[0]
                away = matchup[1]
                home_dict = self._return_correct_team_dict(team=home)
                matchup_count_home = home_dict[away]
                matchup_count = self.all_matchups.count(matchup) + self.all_matchups.count(matchup[::-1])
                if not matchup_count == matchup_count_home:
                    self.logger.warning(
                        f"Matchup {matchup} counts: home: {matchup_count_home} counter: {matchup_count}"
                    )
                matchups_list.append(f"{matchup} plays {matchup_count} times")
            matchups_list = list(set(matchups_list))
            self.logger.info("Creating validation doc")
            with open("validate_schedule.txt", "w") as f:
                for listed_matchup in sorted(matchups_list):
                    f.write("%s\n" % (listed_matchup))
            self.logger.info("Validation doc created successfully!")
        except Exception as e:
            self.logger.error(e)
            raise e

    def _output_team_schedules(self):
        """
        Helper method to output team schedules

        Args:
            None
        """
        self.logger.info("Creating team schedules")
        team_schedule = {}
        with open("schedule.txt", "r") as file:
            lines = file.readlines()

            week = 0
            matchups = []

            for line in lines:
                line = line.strip()

                if line.startswith("Week"):
                    week = int(line.split(":")[0].split()[1])
                    matchups = line.split(":")[1].strip().split(",")

                elif line.startswith("Rivalry Week"):
                    week = "Rivalry"
                    matchups = line.split(":")[1].strip().split(",")

                for matchup in matchups:
                    teams = matchup.split("versus")
                    team1 = teams[0].strip()
                    team2 = teams[1].strip()

                    if team1 not in team_schedule:
                        team_schedule[team1] = []
                    if team2 not in team_schedule:
                        team_schedule[team2] = []

                    team_schedule[team1].append((week, team2))
                    team_schedule[team2].append((week, team1))

                # clear matchup list to prevent duplication
                matchups = []

        self.logger.info("Outputting team schedules to file")
        # output team schedules into a file
        with open("team_schedules.txt", "w") as f:
            for team, schedule in team_schedule.items():
                f.write(f"Schedule for {team}:\n")
                for matchup in schedule:
                    week, opponent = matchup
                    if week == "Rivalry":
                        weekly_match = f"Rivalry Week: versus {opponent}"
                    else:
                        weekly_match = f"Week {week}: versus {opponent}"
                    f.write(f"{weekly_match}\n")
                f.write("\n")

    def _move_files_to_schedule_folder(self):
        """
        Helper method to move schedule files into a schedule folder

        Args:
            None
        """
        self.logger.info("Moving created txt files into schedule folder.")
        # Create the "schedule" folder if it doesn't exist
        if not os.path.exists("schedule"):
            os.makedirs("schedule")

        # List of files to be moved
        files_to_move = ["schedule.txt", "team_schedules.txt", "validate_schedule.txt"]

        # Move each file to the "schedule" folder
        for file_name in files_to_move:
            source_path = file_name
            destination_path = os.path.join("schedule", file_name)
            shutil.move(source_path, destination_path)
        self.logger.info("Files moved successfully to the 'schedule' folder.")

    def controller(self):
        """
        Controller method to run the class
        """
        self.logger.info("Controller beginning schedule generation.")
        current_week = 1
        count_attempts = 1
        # generate schedule iterating by week
        while current_week < 16:
            count_attempts += 1
            indicator = self.generate_weekly_schedule(current_week)
            # only incremement the week if the schedule was accepted to ensure each week gets a schedule
            if indicator:
                count_attempts = 1
                current_week += 1
            if count_attempts > 15:
                return False
        # write the schedule to a txt file
        self._validate_output()
        self._output_schedule()
        self._output_team_schedules()
        self._move_files_to_schedule_folder()
        return True


if __name__ == "__main__":
    number_of_tries = 60
    count = 1
    logger = logging.getLogger("controller_logs")
    while count <= number_of_tries:
        logger.warning(f"Starting attempt number {count} of {number_of_tries}")
        SG = ScheduleGenerator()
        success = SG.controller()
        if success:
            break
        else:
            count += 1
    if success:
        logger.warning("Schedule generated successfully!")
    else:
        logger.warning(f"Schedule validation failed after {number_of_tries} attempts")
