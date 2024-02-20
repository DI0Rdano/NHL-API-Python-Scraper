"""
Python based scraping functions for various NHL API endpoints.
Configured to the work with the new NHL API (as of late 2023).
Not intended to be comprehensive, created for personal use.

MIT Liscence

Follow @DI0Rdano on Twitter/X
"""

# Import libraries
import requests
from datetime import datetime
import json
import time

# Session object for making HTTP requests
session = requests.Session()

#####################################################################################################################################################
# JSON scraping functions for various NHL API endpoints #############################################################################################
#####################################################################################################################################################

def make_api_request(url, timeout=10, retries=3, input_validation=True):
    """
    Make a request to the API and handle retries and error conditions.

    Parameters:
    - url (str): The URL to make the API request to.
    - timeout (int): The timeout duration for the request in seconds. Default is 10.
    - retries (int): The number of retry attempts in case of failure. Default is 3.
    - input_validation (bool): Flag to enable/disable input validation. Default is True.

    Returns:
    - dict or None: The JSON response from the API or None in case of error.
    """
    # Input validation
    if input_validation:
        # Validate URL parameter
        if not isinstance(url, str):
            raise ValueError("(make_api_request) Invalid url, parameter must be a string.")

        # Validate timeout parameter
        if not isinstance(timeout, int):
            raise ValueError("(make_api_request) Invalid timeout, parameter must be an integer.")

        # Validate retries parameter
        if not isinstance(retries, int):
            raise ValueError("(make_api_request) Invalid retries, parameter must be an integer.")

    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if attempt < retries - 1:
                delay = (2 ** attempt) * 0.5  # Exponential backoff
                time.sleep(delay)
            else:
                return None
        except Exception as e:
            return None

def get_config(view=None):
    """
    Fetch data from the NHL API 'config' endpoint.

    Parameters:
    - view (str, optional): The part of the JSON to return. Default is None (returns everything).

    Returns:
    - dict: Configuration data as a JSON dictionary based on the specified view.
    - None: In case of an error.
    """

    # URL for the 'config' endpoint
    url = "https://api.nhle.com/stats/rest/en/config"

    # Make API request
    data = make_api_request(url)

    if data is None:
        return None

    # Filter the response based on the view parameter
    if view is not None:
        filtered_data = data.get(view)
        if filtered_data is None:
            raise ValueError("Invalid view parameter. Allowed values are playerReportData, goalieReportData, teamReportData, aggregatedColumns, individualColumns, and None.")
        return filtered_data

    return data

def get_countries(include_stateProvinces=True, sort="countryName", direction="ASC", input_validation=True):
    """
    Fetch data from the NHL API 'country' endpoint.

    Parameters:
    - include_stateProvinces (bool): Whether to include state provinces in the response. Default is True.
    - sort (str): Field to sort the countries by. Default is "countryName".
    - direction (str): Sort direction. Default is "ASC".
    - input_validation (bool): Flag to enable/disable input validation. Default is True.

    Returns:
    - dict: country data as a json dictionary.
    - None: In case of an error.
    """

    # Input validation
    if input_validation:
        # Validate include_stateProvinces parameter
        if not validate_boolean(include_stateProvinces):
            raise ValueError("(get_countries) Invalid include state provinces parameter. Valid options are TRUE and FALSE as booleans.")

        # Validate sort parameter
        if not validate_sort_field(sort, key="countries"):
            raise ValueError("(get_countries) Invalid sort field. Valid sorting fields include strings: id, country3Code, countryCode, countryName, hasPlayerStats, imageUrl, iocCode, isActive, nationalityName, olympicUrl, thumbnailUrl.")

        # Validate direction parameter
        if not validate_sort_direction(direction.upper()):
            raise ValueError("(get_countries) Invalid sort direction parameter.  Valid sorting options are ASC and DESC as strings.")

    # URL for the 'country' endpoint
    url = f"https://api.nhle.com/stats/rest/en/country?sort=%5B%7B%22property%22:%22{sort}%22,%22direction%22:%22{direction.upper()}%22%7D%5D"

    if include_stateProvinces:
        url += "&include=stateProvinces"

    # Make API request using the helper function
    data = make_api_request(url)

    if data is None:
        return None

    return data

def get_franchises(include_firstSeason=True, include_lastSeason=True, sort="fullName", direction="ASC", input_validation=True):
    """
    Fetch data from the NHL API 'franchise' endpoint.

    Parameters:
    - include_firstSeason (bool): Whether to include first season information. Default is True.
    - include_lastSeason (bool): Whether to include last season information. Default is True.
    - sort (str): Field to sort the franchises by. Default is "fullName". Valid values are "fullName", "teamCommonName", "teamPlaceName", and "id".
    - direction (str): Sort direction. Default is "ASC".
    - input_validation (bool): Flag to enable/disable input validation. Default is True.

    Returns:
    - dict: Franchise data as a JSON dictionary.
    - None: In case of an error.
    """

    # Input validation
    if input_validation:
        # Validate include_firstSeason parameter
        if not validate_boolean(include_firstSeason):
            raise ValueError("(get_franchises) Invalid include first season parameter. Valid options are TRUE and FALSE as booleans.")

        # Validate include_lastSeason parameter
        if not validate_boolean(include_lastSeason):
            raise ValueError("(get_franchises) Invalid include last season parameter. Valid options are TRUE and FALSE as booleans.")

        # Validate sort parameter
        if not validate_sort_field(sort, key="franchises"):
            raise ValueError("(get_franchises) Invalid sort field. Valid sorting fields include strings: fullName, teamCommonName, teamPlaceName, id.")

        # Validate direction parameter
        if not validate_sort_direction(direction.upper()):
            raise ValueError("(get_franchises) Invalid sort direction parameter.  Valid sorting options are ASC and DESC as strings.")

    # URL for the 'franchise' endpoint with sort and direction parameters
    url = f"https://api.nhle.com/stats/rest/en/franchise?sort=%5B%7B%22property%22:%22{sort}%22,%22direction%22:%22{direction.upper()}%22%7D%5D"

    # Include first season information if specified
    if include_firstSeason:
        url += "&include=firstSeason"
    
    # Include last season information if specified
    if include_lastSeason:
        url += "&include=lastSeason"

    # Make API request using the helper function
    data = make_api_request(url)

    if data is None:
        return None

    return data

def get_seasons(sort="id", direction="DESC", input_validation=True):
    """
    Fetch data from the NHL API 'season' endpoint.

    Parameters:
    - sort (str): Field to sort the seasons by. Default is "id". Valid values are "id" and other fields present in the NHL API response.
    - direction (str): Direction of sorting. Default is "DESC". Valid values are "ASC" (ascending) and "DESC" (descending).
    - input_validation (bool): Flag to enable/disable input validation. Default is True.

    Returns:
    - dict: Season data as a JSON dictionary.
    - None: In case of an error.
    """

    if input_validation:
        # Validate sort parameter
        if not validate_sort_field(sort, key="seasons"):
            raise ValueError("(get_seasons) Invalid sort field. Valid sorting fields include strings: id, allStarGameInUse, conferencesInUse, divisionsInUse, endDate, entryDraftInUse, formattedSeasonId, minimumPlayoffMinutesForGoalieStatsLeaders, minimumRegularGamesForGoalieStatsLeaders, nhlStanleyCupOwner, numberOfGames, olympicsParticipation, pointForOTLossInUse, preseasonStartdate, regularSeasonEndDate, rowInUse, seasonOrdinal, startDate, supplementalDraftInUse, tiesInUse, totalPlayoffGames, totalRegularSeasonGames, wildcardInUse.")

        # Validate direction parameter
        if not validate_sort_direction(direction.upper()):
            raise ValueError("(get_seasons) Invalid sort direction parameter.  Valid sorting options are ASC and DESC as strings.")

    # Construct URL
    url = f"https://api.nhle.com/stats/rest/en/season?sort=%5B%7B%22property%22:%22{sort}%22,%22direction%22:%22{direction.upper()}%22%7D%5D"

    # Make API request using the helper function
    data = make_api_request(url)

    if data is None:
        return None

    return data
    
def get_draftrounds(sort="draftYear", direction="DESC", input_validation=True):
    """
    Fetch data from the NHL API 'draft' endpoint.

    Parameters:
    - sort (str): Field to sort the draft rounds by. Default is "draftYear".
    - direction (str): Direction of sorting. Default is "DESC".
    - input_validation (bool): Flag to enable/disable input validation. Default is True.

    Returns:
    - dict: Draft round data as a json dictionary.
    - None: In case of an error.
    """
    
    if input_validation:
        # Validate sort parameter
        if not validate_sort_field(sort, key="draftrounds"):
            raise ValueError("(get_draftrounds) Invalid sort field. Valid sorting fields include strings: draftYear, id, rounds.")

        # Validate direction parameter
        if not validate_sort_direction(direction.upper()):
            raise ValueError("(get_draftrounds) Invalid sort direction parameter.  Valid sorting options are ASC and DESC as strings.")

    # URL for the 'draft' endpoint with sort and direction parameters
    url = f"https://api.nhle.com/stats/rest/en/draft?sort=%5B%7B%22property%22:%22{sort}%22,%22direction%22:%22{direction}%22%7D%5D"

    # Make API request using the helper function
    data = make_api_request(url)

    if data is None:
        return None

    return data

def get_roster(team_code, season, sort="lastName", direction="ASC", input_validation=True):
    """
    Fetch data from the NHL API 'team roster' endpoint.

    Parameters:
    - team_code (str): The abbreviated code of the team, (ex. "TOR").
    - season (str): The season in the format of "20232024".
    - sort (str): Field to sort the roster by. Default is "lastName".
    - direction (str): Direction of sorting. Default is "ASC".
    - input_validation (bool): Flag to enable/disable input validation. Default is True.

    Returns:
    - dict: Player roster data as a json dictionary.
    - None: In case of an error.
    """

    if input_validation:
        # Validate team_code parameter
        if not validate_team_code(team_code):
            raise ValueError("(get_roster) Invalid team code.")

        # Validate season parameter
        if not validate_season(season):
            raise ValueError("(get_roster) Invalid season.")

        # Validate sort parameter
        valid_sort_fields = ["draftYear", "id", "rounds"]
        if not validate_sort_field(sort, key="roster"):
            raise ValueError(f"(get_roster) Invalid sort field. Valid sorting fields include: {', '.join(valid_sort_fields)}.")

        # Validate direction parameter
        if not validate_sort_direction(direction.upper()):
            raise ValueError("(get_roster) Invalid sort direction parameter.  Valid sorting options are ASC and DESC as strings.")

    # Construct the URL for the 'roster' endpoint with sort and direction parameters
    base_url = "https://api-web.nhle.com/v1/roster/"
    url = f"{base_url}{team_code}/{season}?sort=%5B%7B%22property%22:%22{sort}%22,%22direction%22:%22{direction.upper()}%22%7D%5D"

    # Make API request using the helper function
    data = make_api_request(url)

    if data is None:
        return None

    return data
   
def get_roster_seasons(team_code, input_validation=True):
    """
    Fetch data from the NHL API 'team roster-season' endpoint.

    Parameters:
    - team_code (str): The abbreviated code of the team, (ex. "TOR").
    - input_validation (bool): Flag to enable/disable input validation. Default is True.

    Returns:
    - dict: Team roster seasons data as a json dictionary.
    - None: In case of an error.
    """

    if input_validation:
        # Validate team_code parameter
        if not validate_team_code(team_code):
            raise ValueError("(get_roster_season) Invalid team code.")

    # Construct the URL for the 'roster' endpoint with sort and direction parameters
    base_url = "https://api-web.nhle.com/v1/roster-season/"
    url = f"{base_url}{team_code}"

    # Make API request using the helper function
    data = make_api_request(url)

    if data is None:
        return None

    return data

def get_player_landing(player_id, view=None, input_validation=True):
    """
    Fetch data from the NHL API 'player/landing' endpoint.

    Parameters:
    - player_id (int): The ID of the player.
    - view (str): The part of the json to return. Default is None (to return everything).
    - input_validation (bool): Flag to enable/disable input validation. Default is True.

    Returns:
    - dict: Player landing data as a json dictionary.
    - None: In case of an error.
    """

    if input_validation:
        # Validate player_id
        if not validate_id(player_id):
            raise ValueError("Invalid player_id. It should be a positive integer or a string convertible to an integer.")

        # Convert player_id to integer if it's a string
        player_id = int(player_id)

    # Construct the URL for the 'player/landing' endpoint
    base_url = "https://api-web.nhle.com/v1/player/"
    url = f"{base_url}{player_id}/landing"

    # Make API request using the helper function
    data = make_api_request(url)

    if data is None:
        return None

    # Filter the response based on the view parameter
    if view is not None:
        filtered_data = data.get(view)
        if filtered_data is None:
            raise ValueError("Invalid view parameter. Allowed values are featuredStats, careerTotals, seasonTotals, last5Games, awards, currentTeamRoster, and None.")
        return filtered_data

    return data
    
def get_player_gamelog(player_id, season, game_type=2, view="gameLog", input_validation=True):
    """
    Fetch data from the NHL API player 'gamelog' endpoint.

    Parameters:
    - player_id (int): The ID of the player.
    - season (str): The season to return the gamelog from, (ex. '20232024').
    - game_type (int): The type of game (2 for regular season, 3 for playoffs). Default is 2.
    - view (str): The part of the json to return. Default is "gameLog". Allowed values are "gameLog", "playerStatsSeasons", and None (to return everything).
    - input_validation (bool): Flag to enable/disable input validation. Default is True.

    Returns:
    - dict: Player gamelog data as a json dictionary based on the specified view.
    - None: In case of an error.
    """

    if input_validation:
        # Validate player_id
        if not validate_id(player_id):
            raise ValueError("Invalid player_id. It should be a positive integer or a string convertible to an integer.")

        #Validate season
        if not validate_string(season):
            raise ValueError("Invalid season. It should be a string or convertible to a string.")

        # Convert player_id to integer if it's a string
        player_id = int(player_id)

    # Construct the URL for the 'gamelog' endpoint
    base_url = "https://api-web.nhle.com/v1/player/"
    url = f"{base_url}{player_id}/game-log/{season}/{game_type}"

    # Make API request using the helper function
    data = make_api_request(url)

    # Validate game_type
    if input_validation:
        valid_game_types = [game_type_data for game_type_data in data.get("playerStatsSeasons", []) if game_type_data["season"] == int(season)][0].get("gameTypes", [])
        if game_type not in valid_game_types:
            raise ValueError(f"Invalid game type for season {season}. Valid game types are: {', '.join(map(str, valid_game_types))}")
    
    # Filter the response based on the view parameter
    if view is not None:
        filtered_data = data.get(view)
        if filtered_data is None:
            raise ValueError("Invalid view parameter. Allowed values are 'gameLog', 'playerStatsSeasons', None.")
        return filtered_data

    return data

#TODO fill out factCayenneExp, add in functionality for game range, improve input validation
def get_skaters_stats(season, report="summary", aggregate=True, min_gp=0, max_gp=None, sort_fields=["points", "goals", "assists", "playerId"], sort_direction=["DESC", "DESC", "DESC", "ASC"], game_type=2, start_season=None, end_season=None, franchise_id=None, opponent_franchise_id=None, position=None, skater_full_name=None, is_rookie=None, is_active=None, is_in_hall_of_fame=None, nationality_code=None, birth_state_province_code=None, home_or_road=None, game_result=None, draft_round=None, draft_year=None, shoots=None, skater_limit=100, sort=True, input_validation=True):
    """
    Fetch data from the NHL API skater 'skater' endpoint.

    Parameters:
    - season (str): The season to return the skaters stats from (e.g., '20232024').
    - report (str): The report type to return. Available report types are 'summary', 'bios', 'faceoffpercentages', 'faceoffwins', 'goalsForAgainst', etc.
    - aggregate (bool): Boolean option to aggregate skaters stats over multiple seasons or games. Default is 'True'.
    - min_gp (int): The minimum number of games played. Default is '0'.
    - max_gp (int): The maximum number of games played. Default is 'None'.
    - sort_fields (str or list): The sort field(s) for the query. Can be a single string or a list of strings.
    - sor_direction (str or list): The sort direction(s) for the query. Can be a single string or a list of strings.
    - game_type (int, optional): The type of game ('1' for pre-season, '2' for regular season, '3' for playoffs, '4' for all-star games). Default is '2'.
    - start_season (str, optional): The starting season of the range. Default is 'None'.
    - end_season (str, optional): The ending season of the range. Default is 'None'.
    - franchise_id (int, optional): The franchise identifier to return the skaters stats from. Default is 'None' which returns all franchises.
    - opponent_franchise_id (int, optional): The opponent franchise identifier to return the skaters stats from. Default is 'None' which returns all opponent franchises.
    - position (str or list, optional): The positions of the skaters. Default is 'None' which returns all positions.
    - skater_full_name (str, optional): The full name of the skater to filter. Default is 'None' which returns all skaters.
    - is_rookie (bool, optional): Whether the skaters are a rookie (True to return rookies, False to exclude rookies / return veterans). Default is 'None' which returns all skaters.
    - is_active (bool, optional): Whether the skaters are active (True to return active skaters, False to return incactive skaters). Default is 'None' which returns all skaters.
    - is_in_hall_of_fame (bool, optional): Wether the skaters are in the hall of fame. Default is 'None' which returns all skaters.
    - nationality_code (str, optional): The nationlity code of the skaters to return the stats from (e.g., 'CAN'). Default is 'None' which returns all nationalities.
    - birth_state_province_code (str, optional): The birth state province code of the skaters to return the stats from (e.g., 'ON'). Default is 'None' which returns all birth state provinces.
    - home_or_road (str, optional): The skaters stats from home or away games ('H' for home, 'R' for road/away).  Default is 'None' which returns all games.
    - game_result (str, optional): The skaters stats from games with the provided result ('W' for wins, 'L' for losses, and 'O' for overtime losses). Default is 'None' which returns all game results.
    - draft_round (int, optional): The draft round of the skaters to return the stats from. Default is 'None' which returns all rounds.
    - draft_year (str, optional): The draft year of the skaters to return the stats from (e.g., '2012'). Note: if no draft round is input, returns from first round, and only returns data for a single draft round.  Default is 'None' which returns all draft years.
    - shoots (str, optional): The handedness of the skaters to return the stats from ('L' for left, 'R' for right). Default is 'None' which returns all skaters.
    - skater_limit (int): The max number of skaters in one loop (loops to return all skaters regardless of limit).  Default is '100'.
    - sort (bool): Flag to enable/disable sorting. Default is 'True'.
    - input_validation (bool): Flag to enable/disable input validation. Default is 'True'.

    Returns:
    - list: List of dictionaries containing skater(s) season stats.
    - None: In case of an error.
    """
    if input_validation:
        # Validate the minimum games played parameter
        if not validate_min_gp(min_gp):
            raise ValueError("Invalid minimum games played. Must be a positive integer.")
        if max_gp is not None and not validate_min_gp(max_gp):
            raise ValueError("Invalid maximum games played. Must be a positive integer.")

        # Validate the aggregate seasons parameter
        if not validate_boolean(aggregate):
            raise ValueError("Invalid aggregate_seasons parameter. Must be a boolean.")

        # Validate the season parameter for player
        if not validate_season(season):
            raise ValueError("Invalid season.")

        # Validate the report parameter
        if not validate_sort_field(report, key="reports"):
            raise ValueError("Invalid report type.")

        # Validate the sort field parameter
        if not validate_sort_field(sort_fields, key="skaters_stats"):
            raise ValueError("Invalid sort_field.")

        # Validate the sort direction parameter
        if not validate_sort_direction(sort_direction):
            raise ValueError("Invalid sort_direction.")

        # Validate the game type parameter
        if game_type is not None and not (1 <= game_type <= 4):
            raise ValueError("Invalid game_type. Must be an integer from 1 to 4.")

        # Validate start_season and end_season if provided
        if start_season is not None and not validate_season(start_season):
            raise ValueError("Invalid start_season.")

        if end_season is not None and not validate_season(end_season):
            raise ValueError("Invalid end_season.")
        
        # Validate the franchise_id if provided
        if franchise_id is not None and not validate_integer(franchise_id):
            raise ValueError("Invalid franchise_id.  Must be an integer.")
        
        # Validate the franchise_id if provided
        if opponent_franchise_id is not None and not validate_integer(opponent_franchise_id):
            raise ValueError("Invalid opponent_franchise_id.  Must be an integer.")
        
        # Validate position if provided
        if position is not None:
            if isinstance(position, str):
                if position not in ["C", "L", "R", "D"]:
                    raise ValueError("Invalid position. Must be one of 'C', 'L', 'R', 'D'.")
            elif isinstance(position, list):
                if not all(pos in ["C", "L", "R", "D"] for pos in position):
                    raise ValueError("Invalid position list. Must contain only 'C', 'L', 'R', 'D'.")

        # Validate the skater_full_name if provided
        if skater_full_name is not None and not validate_string(skater_full_name):
            raise ValueError("Invalid skater_full_name. Must be a string.")

        # Validate is_rookie if provided
        if is_rookie is not None and not validate_boolean(is_rookie):
            raise ValueError("Invalid is_rookie parameter. Must be a boolean.")

        # Validate skater_limit
        if not validate_integer(skater_limit):
            raise ValueError("Invalid skater_limit. Must be an integer.")
        
        # Validate is_active
        if is_active is not None and not validate_boolean(is_active):
            raise ValueError("Invalid is_active. Must be a boolean.")
        
        # Validate is_in_hall_of_fame
        if is_active is not None and not validate_boolean(is_in_hall_of_fame):
            raise ValueError("Invalid is_in_hall_of_fame. Must be a boolean.")
        
        # Validate the skater_full_name if provided
        if nationality_code is not None and not validate_string(nationality_code):
            raise ValueError("Invalid nationality_code. Must be a string.")
        
        # Validate the skater_full_name if provided
        if birth_state_province_code is not None and not validate_string(birth_state_province_code):
            raise ValueError("Invalid birth_state_province_code. Must be a string.")
        
        # Validate the home_or_road if provided
        if home_or_road is not None and not validate_string(home_or_road):
            raise ValueError("Invalid home_or_road. Must be a string.")
        
        # Validate the home_or_road if provided
        if game_result is not None and not validate_string(game_result):
            raise ValueError("Invalid game_result. Must be a string.")
        
        if not validate_boolean(sort):
            raise ValueError("Invalid sort. Must be a boolean ('True' or 'False').")
        
        if not validate_boolean(input_validation):
            raise ValueError("Invalid input_validation. Must be a boolean ('True' or 'False').")
        
        if draft_round is not None and not validate_integer(draft_round):
            raise ValueError("Invalid draft_round. Must be an integer.")
        
        if draft_year is not None and not validate_string(draft_year):
            raise ValueError("Invalid draft_year. Must be a string.")
        
        if shoots is not None and not validate_string(shoots):
            raise ValueError("Invalid shoots. Must be a string ('L' or 'R').")

    # Construct the URL for the 'skater' endpoint
    base_url = "https://api.nhle.com/stats/rest/en/skater/" + report

    # Construct the cayenneExp
    if start_season is not None and end_season is not None:
        cayenneExp = f"seasonId<={end_season} and seasonId>={start_season}"
    else:
        cayenneExp = f"seasonId={season}"
    
    if game_type is not None:
        cayenneExp += f" and gameTypeId={game_type}"
    
    if franchise_id is not None:
        cayenneExp += f" and franchiseId={franchise_id}"

    if opponent_franchise_id is not None:
        cayenneExp += f" and opponentFranchiseId={opponent_franchise_id}"

    if position is not None:
        if isinstance(position, str):
            cayenneExp += f" and positionCode='{position}'"
        elif isinstance(position, list):
            position_exp = " or ".join([f"positionCode='{pos}'" for pos in position])
            cayenneExp += f" and ({position_exp})"

    if skater_full_name is not None:
        cayenneExp += f" and skaterFullName likeIgnoreCase '%{skater_full_name}%'"

    if is_rookie is not None:
        cayenneExp += f" and isRookie={'1' if is_rookie else '0'}"

    if is_active is not None:
        cayenneExp += f" and active={'1' if is_active else '0'}"

    if is_in_hall_of_fame is not None:
        cayenneExp += f" and isInHallOfFame={'1' if is_in_hall_of_fame else '0'}"

    if birth_state_province_code is not None:
        cayenneExp += f" and birthStateProvinceCode='{birth_state_province_code}'"
    
    if nationality_code is not None:
        cayenneExp += f" and nationalityCode='{nationality_code}'"

    if home_or_road is not None:
        cayenneExp += f" and homeRoad='{home_or_road}'"

    if game_result is not None:
        cayenneExp += f" and decision='{game_result}'"

    if draft_round is not None:
        cayenneExp += f" and draftRound={draft_round}"

    if draft_year is not None:
        cayenneExp += f" and draftYear='{draft_year}'"

    if shoots is not None:
        cayenneExp += f" and shootsCatches='{shoots}'"

    # Construct the factCayenneExp 
    factCayenneExp = f"gamesPlayed>={min_gp}"

    if max_gp is not None:
        factCayenneExp += f" and gamesPlayed<={max_gp}"

    # Construct the query parameters
    params = {
        "isAggregate": str(aggregate),
        "isGame": "false",
        "start": "0",
        "limit": str(skater_limit),
        "factCayenneExp": factCayenneExp,
        "cayenneExp": cayenneExp
    }

    if sort:
        # Convert sort and direction to lists if they are not already
        sort_fields = sort_fields if isinstance(sort_fields, list) else [sort_fields]
        sort_direction = sort_direction if isinstance(sort_direction, list) else [sort_direction]

        # Construct the sort parameters
        sort_params = [{"property": field, "direction": dir} for field, dir in zip(sort_fields, sort_direction)]
        sort_json = json.dumps(sort_params)
        params["sort"] = sort_json

    # Initialize an empty list to store the results
    all_skaters_data = []

    # Loop over multiple times to fetch all skaters
    while True:
        # Construct the complete URL
        url = f"{base_url}?{'&'.join([f'{key}={value}' for key, value in params.items()])}"

        # Make API request using the helper function
        data = make_api_request(url)

        if data is None:
            return None

        all_skaters_data.extend(data.get("data", []))

        # Check if there are more players to fetch
        if len(all_skaters_data) >= data.get("total", 0):
            break

        # Update the starting position for the next request
        params["start"] = str(len(all_skaters_data))

    return all_skaters_data

def get_schedule_calendar(date="now", input_validation=True):
    """
    Fetches schedule calendar data from the NHL API for a specific date.

    Parameters:
    - date (str, optional): The date for which to fetch the schedule calendar data (in 'YYYY-MM-DD' format). Default is "now".
    - input_validation (bool): Flag to enable/disable input validation. Default is True.

    Returns:
    - dict: Schedule calendar data as a JSON dictionary.
    - None: If there is an error fetching the data.
    """
    if date != "now" and input_validation:
        # Validate date parameter and format if valid
        formatted_date = format_date(date)
        if not formatted_date:
            raise ValueError("Invalid date format. Please provide the date in 'YYYY-MM-DD' format.")
    else:
        formatted_date = date

    # Construct the base URL for the schedule calendar endpoint
    base_url = "https://api-web.nhle.com/v1/schedule-calendar/"

    if formatted_date == "now":
        url = f"{base_url}now"
    else:
        # Construct the complete URL for the API request
        url = f"{base_url}{formatted_date}"

    try:
        # Make a request to the NHL API to fetch schedule calendar data
        roster_data = make_api_request(url)
        return roster_data
    except Exception as e:
        # Raise a ValueError if there's an issue with the request
        raise ValueError(f"Error fetching data: {e}")

def get_schedule(date="now", input_validation=True):
    """
    Fetches schedule data from the NHL API for a specific date.

    Parameters:
    - date (str, optional): The date for which to fetch the schedule data (in 'YYYY-MM-DD' format). Default is "now".
    - input_validation (bool): Flag to enable/disable input validation. Default is True.

    Returns:
    - dict: Schedule data as a JSON dictionary.
    - None: If there is an error fetching the data.
    """

    if date != "now" and input_validation:
        # Validate date parameter and format if valid
        formatted_date = format_date(date)
        if not formatted_date:
            raise ValueError("Invalid date format. Please provide the date in 'YYYY-MM-DD' format.")
    else:
        formatted_date = date

    base_url = "https://api-web.nhle.com/v1/schedule/"
    if formatted_date == "now":
        url = f"{base_url}now"
    else:
        url = f"{base_url}{formatted_date}"

    try:
        roster_data = make_api_request(url)
        return roster_data
    except Exception as e:
        raise ValueError(f"Error fetching data: {e}")

def get_nhl_standings(date="now", input_validation=True):
    """
    Fetches NHL standings data for a specific date or today's date.

    Parameters:
    - date (str, optional): The date for which to fetch the standings data (in 'YYYY-MM-DD' format). Default is "now".
    - input_validation (bool): Flag to enable/disable input validation. Default is True.

    Returns:
    - dict: Standings data as a JSON dictionary.
    - None: If there is an error fetching the data.
    """
    if date != "now" and input_validation:
        # Validate date parameter and format if valid
        formatted_date = format_date(date)
        if not formatted_date:
            raise ValueError("Invalid date format. Please provide the date in 'YYYY-MM-DD' format.")
    else:
        formatted_date = date

    base_url = "https://api-web.nhle.com/v1/standings/"
    if formatted_date == "now":
        url = f"{base_url}now"
    else:
        url = f"{base_url}{formatted_date}"

    try:
        standings_data = make_api_request(url)
        return standings_data
    except Exception as e:
        raise ValueError(f"Error fetching standings data: {e}")

def get_standings_seasons(): #TODO add sorting and views
    """
    Fetch data from the NHL API 'standings-season' endpoint.

    Returns:
    - dict: NHL standings available seasons data as a json dictionary.
    - None: In case of an error.
    """

    # Construct the URL for the 'roster' endpoint with sort and direction parameters
    url = "https://api-web.nhle.com/v1/standings-season"

    # Make API request using the helper function
    data = make_api_request(url)

    if data is None:
        return None

    return data

def get_scores(date="now", input_validation=True):
    """
    Fetches NHL scores data for a specific date or today's date.

    Parameters:
    - date (str, optional): The date for which to fetch the scores data (in 'YYYY-MM-DD' format). Default is "now".
    - input_validation (bool): Flag to enable/disable input validation. Default is True.

    Returns:
    - dict: Scores data as a JSON dictionary.
    - None: If there is an error fetching the data.
    """
    if date != "now" and input_validation:
        # Validate date parameter and format if valid
        formatted_date = format_date(date)
        if not formatted_date:
            raise ValueError("Invalid date format. Please provide the date in 'YYYY-MM-DD' format.")
    else:
        formatted_date = date

    base_url = "https://api-web.nhle.com/v1/score/"
    if formatted_date == "now":
        url = f"{base_url}now"
    else:
        url = f"{base_url}{formatted_date}"

    try:
        scores_data = make_api_request(url)
        return scores_data
    except Exception as e:
        raise ValueError(f"Error fetching scores data: {e}")

def get_playbyplay(game_id, view=None, input_validation=True):
    """
    Fetch data from the NHL API player 'play-by-play' endpoint.

    Parameters:
    - game_id (int): The ID of the game.
    - view (str, optional): The part of the JSON to return. Default is None (returns everything).
                            Allowed values are "plays", "rosterSpots", "homeTeam", "awayTeam" to return specific parts of the JSON.
    - input_validation (bool): Flag to enable/disable input validation. Default is True.

    Returns:
    - dict: Play by play data as a JSON dictionary.
    - None: In case of an error.
    """
    if input_validation:
        # Validate game_id
        if not validate_id(game_id):
            raise ValueError("Invalid game_id. It should be a positive integer or a string convertible to an integer.")

        # Convert game_id to integer if it's a string
        game_id = int(game_id)

    # Construct the URL for the 'play-by-play' endpoint
    base_url = "https://api-web.nhle.com/v1/gamecenter/"
    url = f"{base_url}{game_id}/play-by-play"

    try:
        # Make API request using the helper function
        data = make_api_request(url)

        if data is None:
            return None

        # Filter the response based on the view parameter
        if view is not None:
            filtered_data = data.get(view)
            if filtered_data is None:
                raise ValueError("Invalid view parameter. Allowed values are plays, rosterSpots, homeTeam, awayTeam, and None.")
            return filtered_data

        return data

    except ValueError as e:
        # Raise a ValueError if there's an issue with the validation
        raise ValueError(str(e))
    
def get_boxscore(game_id, view=None, input_validation=True):
    """
    Fetch data from the NHL API player 'boxscore' endpoint.

    Parameters:
    - game_id (int): The ID of the game.
    - view (str, optional): The part of the JSON to return. Default is None (returns everything).
                            Allowed values are "boxscore", "homeTeam", "awayTeam" to return specific parts of the JSON.
    - input_validation (bool): Flag to enable/disable input validation. Default is True.

    Returns:
    - dict: Boxscore data as a JSON dictionary.
    - None: In case of an error.
    """
    if input_validation:
        # Validate game_id
        if not validate_id(game_id):
            raise ValueError("Invalid game_id. It should be a positive integer or a string convertible to an integer.")

        # Convert game_id to integer if it's a string
        game_id = int(game_id)

    # Construct the URL for the 'play-by-play' endpoint
    base_url = "https://api-web.nhle.com/v1/gamecenter/"
    url = f"{base_url}{game_id}/boxscore"

    try:
        # Make API request using the helper function
        data = make_api_request(url)

        if data is None:
            return None

        # Filter the response based on the view parameter
        if view is not None:
            filtered_data = data.get(view)
            if filtered_data is None:
                raise ValueError("Invalid view parameter. Allowed values are boxscore, awayTeam, homeTeam, and None.")
            return filtered_data

        return data

    except ValueError as e:
        # Raise a ValueError if there's an issue with the validation
        raise ValueError(str(e))

def get_shifts(game_id, sort=None, direction=None, input_validation=True):
    """
    Fetch data from the NHL API player 'shiftcharts' endpoint.

    Parameters:
    - game_id (int): The ID of the game.
    - sort (str, optional): The field to sort the data by. Default is None.
    - direction (str, optional): The sorting direction. Default is None.
    - input_validation (bool): Flag to enable/disable input validation. Default is True.

    Returns:
    - dict: Shift data as a JSON dictionary.
    - None: In case of an error.
    """

    if input_validation:
        # Validate game_id
        if not validate_id(game_id):
            raise ValueError("Invalid game_id. It should be a positive integer or a string convertible to an integer.")

        # Validate sort field
        if sort is not None and not validate_sort_field(sort, key="shifts"):
            raise ValueError("Invalid sort field.")

        # Validate sort direction
        if direction is not None and not validate_sort_direction(direction):
            raise ValueError("Invalid sort direction.")

    # Construct the URL for the 'shiftcharts' endpoint with optional sorting
    base_url = "https://api.nhle.com/stats/rest/en/shiftcharts"
    if sort is not None and direction is not None:
        sort_param = f"%5B%7B%22property%22%3A%22{sort}%22%2C%22direction%22%3A%22{direction}%22%7D%5D"
        url = f"{base_url}?sort={sort_param}&cayenneExp=gameId%3E={game_id}"
    else:
        url = f"{base_url}?cayenneExp=gameId%3E={game_id}"

    try:
        # Make API request using the helper function
        data = make_api_request(url)

        if data is None:
            return None

        return data

    except ValueError as e:
        # Raise a ValueError if there's an issue with the validation
        raise ValueError(str(e))

def get_team_information():
    """
    Combine data from 'franchises', 'nhl_standings_today', and 'nhl_schedule_calendar' endpoints.

    Returns:
    - dict: Team information combining data from 'franchises', 'nhl_standings_today', and 'nhl_schedule_calendar'.
    """

    # Get data from endpoints
    franchises_data = get_franchises()
    nhl_standings_data = get_nhl_standings()
    nhl_schedule_calendar = get_schedule_calendar()

    # Check if any of the required data is missing
    if None in (franchises_data, nhl_standings_data, nhl_schedule_calendar):
        return None

    # Convert franchises data into a set for faster lookup
    franchises_set = {franchise.get("fullName") for franchise in franchises_data.get("data", [])}

    # Initialize dictionary to store team information
    team_info = {}

    # Process data from 'nhl_standings_today' endpoint
    for team_standings in nhl_standings_data.get("standings", []):
        team_name = team_standings.get("teamName", {}).get("default")

        # Check if team name exists in franchises data
        if team_name in franchises_set:
            # Find the corresponding franchise information using team name
            franchise_info = next((franchise for franchise in franchises_data.get("data", []) if franchise.get("fullName") == team_name), None)

            # If franchise info exists, add it to the team_info dictionary
            if franchise_info:
                team_info[team_name] = {
                    "teamName": franchise_info.get("fullName"),
                    "teamCommonName": franchise_info.get("teamCommonName"),
                    "teamPlaceName": franchise_info.get("teamPlaceName"),
                    "teamAbbrev": team_standings.get("teamAbbrev", {}).get("default"),
                    "conferenceAbbrev": team_standings.get("conferenceAbbrev"),
                    "conferenceName": team_standings.get("conferenceName"),
                    "divisionAbbrev": team_standings.get("divisionAbbrev"),
                    "divisionName": team_standings.get("divisionName"),
                    "franchiseId": franchise_info.get("id"),
                    "firstSeasonId": franchise_info.get("firstSeason", {}).get("id"),
                    "lastSeasonId": franchise_info.get("lastSeason", {}).get("id") if franchise_info.get("lastSeason") else None,
                    "teamLogoLight": team_standings.get("teamLogo"),
                }

    # Process data from 'nhl_schedule_calendar' endpoint
    for team_schedule in nhl_schedule_calendar.get("teams", []):
        team_name = team_schedule.get("name", {}).get("default")

        # Check if team name exists in franchises data
        if team_name in franchises_set:
            # Find the corresponding franchise information using team name
            franchise_info = next((franchise for franchise in franchises_data.get("data", []) if franchise.get("fullName") == team_name), None)

            # If franchise info exists, update team_info with additional data
            if franchise_info:
                if team_name in team_info:
                    team_info[team_name]["teamLogoDark"] = team_schedule.get("darkLogo")
                    team_info[team_name]["teamId"] = team_schedule.get("id")

    return team_info

def get_club_stats_seasons(team_code, input_validation=True):
    """
    Fetch data from the NHL API 'team roster' endpoint.

    Parameters:
    - team_code (str): The abbreviated code of the team, (ex. "TOR").
    - input_validation (bool): Flag to enable/disable input validation. Default is True.

    Returns:
    - dict: Player roster data as a json dictionary.
    - None: In case of an error.
    """

    if input_validation:
        # Validate team_code parameter
        if not validate_team_code(team_code):
            raise ValueError("(get_club_stats_season) Invalid team code.")

    # Construct the URL for the 'roster' endpoint with sort and direction parameters
    base_url = "https://api-web.nhle.com/v1/club-stats-season/"
    url = f"{base_url}{team_code}"

    # Make API request using the helper function
    data = make_api_request(url)

    if data is None:
        return None

    return data

def get_club_schedule_week(team_code, date="now", input_validation=True):
    """
    Fetches schedule data from the NHL API for a specific date.

    Parameters:
    - date (str, optional): The date for which to fetch the schedule data (in 'YYYY-MM-DD' format). Default is "now".
    - team_code (str): The abbreviated code of the team, (ex. "TOR").
    - input_validation (bool): Flag to enable/disable input validation. Default is True.

    Returns:
    - dict: Schedule data as a JSON dictionary.
    - None: If there is an error fetching the data.
    """

    if input_validation:
        # Validate team_code parameter
        if not validate_team_code(team_code):
            raise ValueError("(get_roster_season) Invalid team code.")

    if date != "now" and input_validation:
        # Validate date parameter and format if valid
        formatted_date = format_date(date)
        if not formatted_date:
            raise ValueError("Invalid date format. Please provide the date in 'YYYY-MM-DD' format.")
    else:
        formatted_date = date

    base_url = "https://api-web.nhle.com/v1/club-schedule/"
    if formatted_date == "now":
        url = f"{base_url}{team_code}/week/now"
    else:
        url = f"{base_url}{team_code}/week/{formatted_date}"

    try:
        roster_data = make_api_request(url)
        return roster_data
    except Exception as e:
        raise ValueError(f"Error fetching data: {e}")

def get_club_schedule_month(team_code, date="now", input_validation=True):
    """
    Fetches schedule data from the NHL API for a specific date.

    Parameters:
    - date (str, optional): The date for which to fetch the schedule data (in 'YYYY-MM-DD' format). Default is "now".
    - team_code (str): The abbreviated code of the team, (ex. "TOR").
    - input_validation (bool): Flag to enable/disable input validation. Default is True.

    Returns:
    - dict: Schedule data as a JSON dictionary.
    - None: If there is an error fetching the data.
    """

    if input_validation:
        # Validate team_code parameter
        if not validate_team_code(team_code):
            raise ValueError("(get_roster_season) Invalid team code.")

    if date != "now" and input_validation:
        # Validate date parameter and format if valid
        formatted_date = format_month(date)
        if not formatted_date:
            raise ValueError("Invalid date format. Please provide the date in 'YYYY-MM-DD' format.")
    else:
        formatted_date = date

    base_url = "https://api-web.nhle.com/v1/club-schedule/"
    if formatted_date == "now":
        url = f"{base_url}{team_code}/month/now"
    else:
        url = f"{base_url}{team_code}/month/{formatted_date}"

    try:
        roster_data = make_api_request(url)
        return roster_data
    except Exception as e:
        raise ValueError(f"Error fetching data: {e}")

#TODO get club stats



#####################################################################################################################################################
# Input validation for the various NHL API functions #########################################################################################
#####################################################################################################################################################

def validate_team_code(team_code, team_info=None):
    """
    Validate the team code.

    Parameters:
    - team_code (str): The team code to validate.
    - team_info (dict): JSON dictionary containing team information [response from team_information()].

    Returns:
    - bool: True if the team code is valid, False otherwise.
    """
    
    # If team_info is not provided, call team_information function to retrieve team_info
    if team_info is None:
        team_info = get_team_information()

    # Check if team_code is found in any teamAbbrev field in team_info
    for team_data in team_info.values():
        if team_data.get("teamAbbrev") == team_code:
            return True

    return False

def validate_sort_field(sort_field, key=None):
    """
    Validate the sort field based on the specified key.

    Parameters:
    - sort_field (str or list): The sort field(s) to validate. Can be a single string or a list of strings.
    - key (str, optional): The key indicating which set of valid sort fields to use.

    Returns:
    - bool: True if the sort field(s) is valid, False otherwise.
    """
    # Define valid sort fields based on the key
    valid_sort_fields = {
        "countries": ["id", "country3Code", "countryCode", "countryName", "hasPlayerStats", "imageUrl", "iocCode", "isActive", "nationalityName", "olympicUrl", "thumbnailUrl"], 
        "franchises": ["fullName", "teamCommonName", "teamPlaceName", "id"], 
        "seasons": ["id", "allStarGameInUse", "conferencesInUse", "divisionsInUse", "endDate", "entryDraftInUse", "formattedSeasonId", "minimumPlayoffMinutesForGoalieStatsLeaders", "minimumRegularGamesForGoalieStatsLeaders", "nhlStanleyCupOwner", "numberOfGames", "olympicsParticipation", "pointForOTLossInUse", "preseasonStartdate", "regularSeasonEndDate", "rowInUse", "seasonOrdinal", "startDate", "supplementalDraftInUse", "tiesInUse", "totalPlayoffGames", "totalRegularSeasonGames", "wildcardInUse"],
        "draftrounds": ["draftYear", "id", "rounds"],
        "roster": ["lastName", "firstName"], # need to add the rest of the fields, also for players_stats
        "skaters_stats": ["points", "evPoints", "goals", "evGoals", "otGoals", "gameWinningGoals", "assists", "playerId", "gamesPlayed", "faceoffWinPct", "penaltyMinutes"],
        "shifts": [None, "id"], #add the rest
        "reports": ["summary", "bios", "faceoffpercentages", "faceoffwins", "goalsForAgainst"] #need to add the rest
        # Add more keys and valid sort fields as needed
    }

    # Get the valid sort fields based on the key
    valid_fields = valid_sort_fields.get(key, [])

    # If sort_field is a list, check each element
    if isinstance(sort_field, list):
        return all(field in valid_fields for field in sort_field)
    # If sort_field is a single string, check it directly
    elif isinstance(sort_field, str):
        return sort_field in valid_fields
    else:
        return False

def validate_sort_direction(direction):
    """
    Validate the sorting direction.

    Parameters:
    - direction (str or list): The sorting direction(s) to validate. Can be a single string or a list of strings.

    Returns:
    - bool: True if the sorting direction(s) is valid, False otherwise.
    """
    valid_directions = ["ASC", "DESC"]

    # If direction is a list, check each element
    if isinstance(direction, list):
        return all(dir_str in valid_directions for dir_str in direction)
    # If direction is a single string, check it directly
    elif isinstance(direction, str):
        return direction in valid_directions
    else:
        return False

def validate_season(season, seasons_info=None, team_info=None, team_code=None):
    """
    Validate the season.

    Parameters:
    - season (str): The season to validate.
    - seasons_info (dict, optional): Dictionary containing information about available seasons. Default is None.
    - team_info (dict, optional): Dictionary containing team information. Default is None.
    - team_code (str, optional): The team code. Default is None.

    Returns:
    - bool: True if the season is valid within the available seasons and can be converted to a string, False otherwise.
    """
    if seasons_info is None:
        # Call get_seasons function to retrieve seasons_info
        seasons_info = get_seasons()

    if seasons_info is None:
        return False  # Unable to retrieve seasons info

    # Check if the season is within the available seasons
    available_seasons = [str(season_data.get("id")) for season_data in seasons_info.get("data", [])]
    if str(season) not in available_seasons:
        return False
    
    # Convert season to string for comparison
    try:
        season_str = str(season)
    except ValueError:
        return False  # Cannot convert to string

    # If team_info is not provided but team_code is, call team_information function to retrieve team_info
    if team_info is None and team_code:
        team_info = get_team_information()

    # If team_info is provided, check if the season is within the team's range
    if team_info and team_code:
        # If no team information is available, return False
        if team_code not in team_info:
            return False
        
        # Get the first and last season IDs from the team information
        first_season_id = team_info[team_code].get("firstSeasonId")
        last_season_id = team_info[team_code].get("lastSeasonId")
        
        # Check if the season is earlier than the first season
        if first_season_id and season_str < str(first_season_id):
            return False

        # Check if the season is later than the last season
        if last_season_id and season_str > str(last_season_id):
            return False

    # Otherwise, the season is valid
    return True

def validate_string(string):
    """
    Validate a string input.

    Parameters:
    - input_value (any): The input value to validate.

    Returns:
    - bool: True if the input can be converted to a non-empty string, False otherwise.
    """
    try:
        # Attempt to convert the input to a string
        str(string)
        # Check if the resulting string is non-empty
        return isinstance(string, str) and string.strip() != ""
    except:
        return False

def validate_boolean(boolean):
    """
    Validate a boolean input.

    Parameters:
    - input_value (bool): The input value to validate.

    Returns:
    - bool: True if the input is a boolean, False otherwise.
    """
    return isinstance(boolean, bool)

def validate_integer(integer):
    """
    Validate an integer input.

    Parameters:
    - input_value (any): The input value to validate.

    Returns:
    - bool: True if the input can be converted to an integer, False otherwise.
    """
    try:
        # Attempt to convert the input to an integer
        int(integer)
        return True
    except ValueError:
        return False

def validate_min_gp(min_gp):
    """
    Validate an integer input and ensure it is greater than zero.

    Parameters:
    - integer (any): The input value to validate.

    Returns:
    - bool: True if the input can be converted to a positive integer, False otherwise.
    """
    try:
        # Attempt to convert the input to an integer
        int_value = int(min_gp)
        # Check if the integer is greater than zero
        return int_value >= 0
    except ValueError:
        return False

def validate_id(id):
    """
    Validate an integer input and ensure it is greater than zero.

    Parameters:
    - integer (any): The input value to validate.

    Returns:
    - bool: True if the input can be converted to a positive integer, False otherwise.
    """
    try:
        # Attempt to convert the input to an integer
        int_value = int(id)
        # Check if the integer is greater than zero
        return int_value > 0
    except ValueError:
        return False

def format_date(date_string):
    try:
        # Parse the input date string
        parsed_date = datetime.strptime(date_string, "%Y-%m-%d")
        # Format the date as "YYYY-MM-DD"
        formatted_date = parsed_date.strftime("%Y-%m-%d")
        return formatted_date
    except ValueError:
        # Handle invalid date string
        raise ValueError("Error: Invalid date format")
    
def format_month(date_string):
    try:
        # Parse the input date string
        parsed_date = datetime.strptime(date_string, "%Y-%m-%d")
        # Format the date as "YYYY-MM"
        formatted_date = parsed_date.strftime("%Y-%m")
        return formatted_date
    except ValueError:
        # Handle invalid date string
        raise ValueError("Error: Invalid date format")
    
#TODO fix list comparison issues
def validate_player_seasons(season, player_id):
    """
    Validate the season parameter for a specific player_id.

    Parameters:
    - player_id (int): The ID of the player.
    - season (str): The season to validate (e.g., '20202021').

    Returns:
    - bool: True if the season is valid for the player, False otherwise.
    """
    # Fetch player landing data to get a list of all seasons for the player
    player_landing_data = get_player_landing(player_id, view="seasonTotals")
    if player_landing_data is None:
        # Unable to fetch player landing data, return False
        return False

    # Extract NHL seasons from player landing data
    nhl_seasons = [season_data.get("season") for season_data in player_landing_data if season_data.get("leagueAbbrev") == "NHL"]

    # Check if the provided season is within the list of NHL seasons for the player
    if season in nhl_seasons:
        return True

    return False

#TODO use get_config to validate skater_stats fields
#TODO use get_club_stats_season to validate seasons for club_stats
#TODO use get_roster_seasons to valdate season in get_roster
#TODO validate get_skaters_stats parameters
