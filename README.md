# QPFL Tools

![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/gansel51/qpfl_tools)
![GitHub repo file count](https://img.shields.io/github/directory-file-count/gansel51/qpfl_tools)
![GitHub issues](https://img.shields.io/github/issues-raw/gansel51/qpfl_tools)
![GitHub](https://img.shields.io/github/license/gansel51/qpfl_tools)

This repository holds tools to facilitate the running of an offline fantasy football league.

## Current Tools

-    Schedule Generator
-    Offline Scorer

## Usage

## How to Use

1. Clone the repository to your local machine. This can be done in the terminal with the command `git clone https://github.com/gansel51/qpfl_tools.git`
2. Run the tool you want to utilize by running the command `python <filename>.py`

### Schedule Generator

The schedule generator randomly generates a schedule for a 15 week season with 10 teams. Over the first 9 weeks of the season, each team plays each opponent once. After that, the schedule is random, but teams can only play another team a maximum of two times.

#### Rivalry Week

Week Five is rivalry week, as it is the last week with no byes. It is a predefined week where each team plays their rivals. That week counts as the time teams play their rival in the first 9 weeks.

#### Schedule Validator

The schedule validator confirms that teams only play an opponent a maximum of two times. Any times where the count is greater than three is indicative of a code failure.

### Offline Scorer

The offline scorer has three modes: player scoring, team scoring, and matchup scoring. Player scoring gives you the option to score one or more players without scoring a full team while team scoring is a full team and matchup scoring is two full teams.

If a player has already been scored, reply "scored" to the first prompt in scoring that player in order to pass through by inputting their score.

#### Quarterback

Quarterback will default to asking for passing yards, rushing yards, touchdowns, and turnovers. If your quarterback scored via receiving or two point conversions, indicate that your player scored in another way when prompted.

#### Running Back

Running back will default to asking for rushing yards, receiving yards, touchdowns, and turnovers. If your running back scored via passing or two point conversions, indicate that your player scored in another way when prompted.

#### Wide Receiver and Tight End

Wide Receiver and tight end will default to asking for receiving yards, touchdowns, and turnovers. If your wide receiver or tight end scored via passing or two point conversions, indicate that your player scored in another way when prompted.

#### Kicker

Kicker will ask for PATs made, PAT attempted, then field goals by yardage followed by misses.

#### Defense

Defense will ask for points allowed, turnovers, sacks, blocked punts or FGs, safeties, and TDs.

#### Head Coach

Defense will ask if your coach won and for the margin of victory or defeat.
