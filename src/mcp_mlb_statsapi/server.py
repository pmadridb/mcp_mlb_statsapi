from mcp.server.fastmcp import FastMCP
from pybaseball import playerid_lookup
import pandas as pd
import statsapi
from datetime import datetime

# Create an MCP server
mcp = FastMCP("mlb_statsapi_mcp")

def find_games_by_team_id(games_data, team_id):
    """
    Finds games in a list of game data where the given team is either the home or away team.

    Args:
        games_data: A list of dictionaries, where each dictionary represents a game
                    and contains keys like 'home_id' and 'away_id'.
        team_id: The id of the team to search for.

    Returns:
        A dictionary represents a game in which
        the specified team is playing (either as home or away team).
        Returns None if no games are found for the team.
    """
    for game in games_data:
        if game['home_id'] == team_id or game['away_id'] == team_id:
            return game
    return None
@mcp.tool()
def look_up_team(team_name):
    """
    Looks up an MLB team by name.

    Args:
        team_name (str): The name of the MLB team (e.g., "Los Angeles Dodgers").

    Returns:
        dict: A dictionary containing information about the team, such as its ID, name, abbreviation, and other relevant details.
    """
    teams = statsapi.lookup_team(team_name, activeStatus="Y")
    print(teams)
    return teams[0]

@mcp.tool()
def get_daily_results(date=None):
    """Fetch MLB game results for a given date (default is today)
       Args:
         date (str): The date for fetching game results.
       Returns:
         list: A list of dictionaries containing game details.
    """
    if date is None:
        date = datetime.today().strftime('%Y-%m-%d')  # Default to today

    schedule = statsapi.schedule(start_date=date, end_date=date)
    
    results = []
    for game in schedule:
        if game['status'] == "Final":
            result = {
                "date": game["game_date"],
                "home_team": game["home_name"],
                "home_score": game["home_score"],
                "away_team": game["away_name"],
                "away_score": game["away_score"],
                "winning_team": game["winning_team"],
                "losing_team": game["losing_team"],
                "MVP": game.get("winning_pitcher", "N/A")
            }
            results.append(result)

    return results

@mcp.tool()
def get_mlb_schedule(start_date=None, end_date=None, team_id=None):
    """
    Retrieves the MLB game schedule for a specified date range, optionally for a specific team.

    Args:
        start_date (str, optional): The start date for the schedule (YYYY-MM-DD). Defaults to today.
        end_date (str, optional): The end date for the schedule (YYYY-MM-DD). Defaults to today.
        team_id (int, optional): The ID of the team to get the schedule for. Defaults to None (all teams).

    Returns:
        list: A list of dictionaries, where each dictionary represents a game in the schedule.
              Each game dictionary contains details like game ID, date, time, home team, away team, etc.
    """
    if start_date is None:
        start_date = datetime.today().strftime('%Y-%m-%d')
    if end_date is None:
        end_date = datetime.today().strftime('%Y-%m-%d')
    if team_id is not None:
        return statsapi.schedule(team=team_id, start_date=start_date, end_date=end_date)
    
    return statsapi.schedule(start_date=start_date, end_date=end_date)

@mcp.tool()
def mlb_team_result(team_name, date=None):
    """
    Retrieves the results (scoring plays and highlights) for a specific MLB team's most recent game.

    Args:
        team_name (str): The name of the MLB team (e.g., "Los Angeles Dodgers").
        date (str, optional): The date for the schedule (YYYY-MM-DD). Defaults to today.
    Returns:
        dict or None: A dictionary containing the scoring plays and game highlights for the team's most recent game,
                      or None if no game is found for the team.
                      The dictionary has the following structure:
                      {
                          "scoring_plays": list,  # List of scoring plays
                          "game_highlights": list  # List of game highlights
                      }
    """
    teamInfo = look_up_team(team_name)
    games = get_mlb_schedule(start_date=date, end_date=date, team_id=teamInfo['id'])
    game = find_games_by_team_id(games, teamInfo['id'])

    if (game):
        gamePk = game['game_id']
        result = {
            "scoring_plays": statsapi.game_scoring_plays(gamePk),
            "game_highlights": statsapi.game_highlights(gamePk)
        }

        return result
    else:
        return None
    
@mcp.tool()
def player_id_lookup(last_name: str = None, first_name: str = None, fuzzy: bool = False) -> pd.DataFrame:
    """
    Look up player IDs based on last name, first name, and fuzzy matching.

    Args:
        last_name (str, optional): The last name of the player. Defaults to None.
        first_name (str, optional): The first name of the player. Defaults to None.
        fuzzy (bool, optional): Whether to use fuzzy matching for the lookup. Defaults to False.

    Returns:
        pd.DataFrame: A DataFrame containing the player information based on the provided criteria.
    """
    if last_name is not None and first_name is not None:
        data = playerid_lookup(last_name, first_name, fuzzy=False)
    elif last_name is not None and first_name is None:
        data = playerid_lookup(last_name, fuzzy=True)
    elif last_name is None and first_name is not None:
        data = playerid_lookup(first_name, fuzzy=True)
    else:
        return None

    return data

@mcp.tool()
def get_player_info(lookup_value) -> dict:
    """
    Retrieve player information based on the lookup value.

    Args:
        lookup_value (str): The lookup value.

    Returns:
        dict: A dictionary containing the player's information, including name, team, position, and other relevant details.
    """
    try:
        player_info = statsapi.lookup_player(lookup_value)
        return player_info
    except Exception as e:
        print(f"Error retrieving player information: {e}")
        return None

@mcp.tool()
def get_game_highlights(game_id) -> list:
    """
    Retrieve game highlights based on the provided game ID.

    Args:
        game_id (str): The ID of the game for which to retrieve highlights.

    Returns:
        list: A list of highlights for the specified game, including descriptions and media links.
    """
    try:
        highlights = statsapi.game_highlights(game_id)
        return highlights
    except Exception as e:
        print(f"Error retrieving game highlights: {e}")
        return None


@mcp.tool()
def game_pace(season):
    """
    MCP wrapper for statsapi.game_pace.

    For full parameter details see the upstream `statsapi.game_pace` function.
    This wrapper forwards the `season` argument to `statsapi.game_pace`.

    Returns:
        The result from `statsapi.game_pace` for the specified season, which includes pace metrics for MLB games in that season.
        Example:
            2008 Game Pace Stats
            hitsPer9Inn: 18.26
            runsPer9Inn: 9.38
            pitchesPer9Inn: 297.72
            plateAppearancesPer9Inn: 77.89
            hitsPerGame: 18.11
            runsPerGame: 9.3
            inningsPlayedPerGame: 8.96
            pitchesPerGame: 295.36
            pitchersPerGame: 7.83
            plateAppearancesPerGame: 77.28
            totalGameTime: 7086:06:00
            totalInningsPlayed: 21748.0
            totalHits: 43972
            totalRuns: 22585
            totalPlateAppearances: 187630
            totalPitchers: 19012
            totalPitches: 717131
            totalGames: 2428
            total9InnGames: 2428
            totalExtraInnGames: 208
            timePerGame: 02:55:07
            timePerPitch: 00:00:36
            timePerHit: 00:09:40
            timePerRun: 00:18:50
            timePerPlateAppearance: 00:02:16
            timePer9Inn: 02:56:30
            timePer77PlateAppearances: 02:54:29
            totalExtraInnTime: 775:10:00
            timePer7InnGameWithoutExtraInn: 00:00:00
            total9InnGamesCompletedEarly: 3
            total9InnGamesWithoutExtraInn: 2217
            total9InnGamesScheduled: 2428
            hitsPerRun: 1.947
            pitchesPerPitcher: 37.72
            total7InnGames: 3
            total9InnGames: 2217
            totalExtraInnGames: 208
            timePer7InnGame: 01:54:40
            timePer9InnGame: 02:50:38
            timePerExtraInnGame: 03:43:36
    """
    try:
        return statsapi.game_pace(season)
    except Exception as e:
        print(f"Error calling statsapi.game_pace: {e}")
        return None
