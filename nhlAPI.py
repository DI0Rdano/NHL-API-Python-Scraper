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
# Scraping functions for various NHL API endpoints ##################################################################################################
#####################################################################################################################################################

def get_config(view=None):
    """
    Fetch data from the NHL API 'config' endpoint.

    Parameters:
    - view (str, optional): The part of the JSON to return, use '.' as a delimiter for subfields. Default is None (returns everything).

    Returns:
    - dict: Configuration data as a JSON dictionary based on the specified view.
    - None: In case of an error.
    """

    # URL for the 'config' endpoint
    url = "https://api.nhle.com/stats/rest/en/config?"

    # Make API request
    data = make_api_request(url)

    if data is None:
        return None

    # Filter the response based on the view parameter
    if view is not None:
        # Split the view string by "." to handle nested fields
        fields = view.split(".")
        filtered_data = data
        for field in fields:
            # Check if the current field exists in the filtered data
            if isinstance(filtered_data, dict) and field in filtered_data:
                filtered_data = filtered_data[field]
            else:
                raise ValueError(f"Invalid view parameter. Field '{field}' not found or not a valid subfield.")
        return filtered_data

    return data

def get_countries(include_stateProvinces=True, sort="countryName", direction="ASC", filter=None, input_validation=True):
    """
    Fetch data from the NHL API 'country' endpoint.

    Parameters:
    - include_stateProvinces (bool): Whether to include state provinces in the response. Default is 'True'.
    - sort (str or list, optional): Field to sort the countries by. Default is 'countryName'.
    - direction (str or list): Sort direction ('ASC' for ascending, 'DESC' for descending). Default is 'ASC'.
    - filter (str or list, optional): The fields to include in the json response. Default is 'None' which returns all fields.
    - input_validation (bool): Flag to enable/disable input validation. Default is 'True'.

    Returns:
    - dict: country data as a json dictionary.
    - None: In case of an error.
    """

    # Input validation
    if input_validation:
        # Validate include_stateProvinces parameter
        if not validate_boolean(include_stateProvinces):
            raise ValueError(f"(get_countries) Invalid include state_provinces='{include_stateProvinces}'. Valid options are 'TRUE' and 'FALSE'.")

        # Validate sort parameter
        if sort is not None and not validate_field(sort, key="countries"):
            raise ValueError(f"(get_countries) Invalid sort='{sort}'. Valid fields include strings: 'id', 'country3Code', 'countryCode', 'countryName', 'hasPlayerStats', 'imageUrl', 'iocCode', 'isActive', 'nationalityName', 'olympicUrl', 'thumbnailUrl'.")

        # Validate direction parameter
        if not validate_sort_direction(direction):
            raise ValueError(f"(get_countries) Invalid sort direction='{direction}'. Valid sorting options are 'ASC' and 'DESC'.")

        # Validate filter parameter
        if filter is not None and not validate_field(filter, key="countries"):
            raise ValueError(f"(get_countries) Invalid filter='{filter}'. Valid fields include strings: 'id', 'country3Code', 'countryCode', 'countryName', 'hasPlayerStats', 'imageUrl', 'iocCode', 'isActive', 'nationalityName', 'olympicUrl', 'thumbnailUrl'.")


    # URL for the 'country' endpoint
    url = "https://api.nhle.com/stats/rest/en/country?"

    # Sorting parameters
    if sort is not None:
        # Construct the sort parameters
        sort_params = construct_sorting_params(sort, direction, input_validation)
        url += sort_params

    # Include state provinces
    if include_stateProvinces:
        if sort is not None:
            url += "&"
        url += "include=stateProvinces"

    # Filter parameters
    if filter:
        if sort is not None or include_stateProvinces:
            url += "&"
        if isinstance(filter, str):
            url += f"include={filter}"
        elif isinstance(filter, list):
            url += "&".join([f"include={f}" for f in filter])

    # Make API request
    data = make_api_request(url, input_validation=input_validation)

    if data is None:
        return None

    return data

def get_franchises(include_firstSeason=True, include_lastSeason=True, sort="fullName", direction="ASC", filter=None, input_validation=True):
    """
    Fetch data from the NHL API 'franchise' endpoint.

    Parameters:
    - include_firstSeason (bool): Whether to include first season information. Default is 'True'.
    - include_lastSeason (bool): Whether to include last season information. Default is 'True'.
    - sort (str or list, optional): Field to sort the franchises by. Default is 'fullName'. Valid values are 'fullName', 'teamCommonName', 'teamPlaceName', and 'id'.
    - direction (str or list): Sort direction. Default is 'ASC'.
    - filter (str or list, optional): The fields to include in the json response. Default is 'None' which returns all fields.
    - input_validation (bool): Flag to enable/disable input validation. Default is 'True'.

    Returns:
    - dict: Franchise data as a JSON dictionary.
    - None: In case of an error.
    """

    # Input validation
    if input_validation:
        # Validate include_firstSeason parameter
        if not validate_boolean(include_firstSeason):
            raise ValueError(f"(get_franchises) Invalid include_firstSeason='{include_firstSeason}'. Valid options are 'TRUE' and 'FALSE'.")

        # Validate include_lastSeason parameter
        if not validate_boolean(include_lastSeason):
            raise ValueError(f"(get_franchises) Invalid include_lastSeason={include_lastSeason}'. Valid options are 'TRUE' and 'FALSE'.")

        # Validate sort parameter
        if sort is not None and not validate_field(sort, key="franchises"):
            raise ValueError("(get_franchises) Invalid sort field. Valid sorting fields include strings: 'fullName', 'teamCommonName', 'teamPlaceName', 'id'.")
            
        # Validate direction parameter
        if not validate_sort_direction(direction):
            raise ValueError(f"(get_franchises) Invalid sort direction='{direction}'.  Valid sorting options are 'ASC' and 'DESC'.")

        # Validate filter parameter
        if filter is not None and not validate_field(filter, key="franchises"):
            raise ValueError(f"(get_franchises) Invalid filter='{filter}'. Valid fields include strings: 'fullName', 'teamCommonName', 'teamPlaceName', 'id'.")


    # URL for the 'franchise' endpoint
    url = f"https://api.nhle.com/stats/rest/en/franchise?"

    # Sorting parameters
    if sort is not None:
        # Construct the sort parameters
        sort_params = construct_sorting_params(sort, direction, input_validation)
        url += sort_params

    # Include first season
    if include_firstSeason:
        if sort is not None:
            url += "&"
        url += "include=firstSeason"

    
    # Include first season
    if include_lastSeason:
        if sort is not None or include_firstSeason is not None:
            url += "&"
        url += "include=lastSeason"

    # Filter parameters
    if filter:
        if sort is not None or include_firstSeason or include_lastSeason:
            url += "&"
        if isinstance(filter, str):
            url += f"include={filter}"
        elif isinstance(filter, list):
            url += "&".join([f"include={f}" for f in filter])

    # Make API request
    data = make_api_request(url, input_validation=input_validation)

    if data is None:
        return None

    return data

def get_seasons(sort="id", direction="DESC", filter=None, input_validation=True):
    """
    Fetch data from the NHL API 'season' endpoint.

    Parameters:
    - sort (str or list, optional): Field to sort the seasons by. Default is 'id'. Valid values are 'id' and other fields present in the NHL API response.
    - direction (str or list): Direction of sorting. Default is 'DESC'. Valid values are 'ASC' (ascending) and 'DESC' (descending).
    - filter (str or list, optional): The fields to include in the json response. Default is 'None' which returns all fields.
    - input_validation (bool): Flag to enable/disable input validation. Default is 'True'.

    Returns:
    - dict: Season data as a JSON dictionary.
    - None: In case of an error.
    """

    # Validate input parameters
    if input_validation:
        # Validate sort parameter
        if sort is not None and not validate_field(sort, key="seasons"):
            raise ValueError(f"(get_seasons) Invalid sort='{sort}'. Valid sorting fields include strings: 'id', 'allStarGameInUse', 'conferencesInUse', 'divisionsInUse', 'endDate', 'entryDraftInUse', 'formattedSeasonId', 'minimumPlayoffMinutesForGoalieStatsLeaders', 'minimumRegularGamesForGoalieStatsLeaders', 'nhlStanleyCupOwner', 'numberOfGames', 'olympicsParticipation', 'pointForOTLossInUse', 'preseasonStartdate', 'regularSeasonEndDate', 'rowInUse', 'seasonOrdinal', 'startDate', 'supplementalDraftInUse', 'tiesInUse', 'totalPlayoffGames', 'totalRegularSeasonGames', 'wildcardInUse'.")
        
        # Validate direction parameter
        if not validate_sort_direction(direction):
            raise ValueError(f"(get_seasons) Invalid sort direction='{direction}'.  Valid sorting options are 'ASC' and 'DESC'.")

        # Validate filter parameter
        if filter is not None and not validate_field(filter, key="seasons"):
            raise ValueError(f"(get_seasons) Invalid filter='{filter}'. Valid fields include strings: 'id', 'allStarGameInUse', 'conferencesInUse', 'divisionsInUse', 'endDate', 'entryDraftInUse', 'formattedSeasonId', 'minimumPlayoffMinutesForGoalieStatsLeaders', 'minimumRegularGamesForGoalieStatsLeaders', 'nhlStanleyCupOwner', 'numberOfGames', 'olympicsParticipation', 'pointForOTLossInUse', 'preseasonStartdate', 'regularSeasonEndDate', 'rowInUse', 'seasonOrdinal', 'startDate', 'supplementalDraftInUse', 'tiesInUse', 'totalPlayoffGames', 'totalRegularSeasonGames', 'wildcardInUse'.")

    # Construct URL
    url = f"https://api.nhle.com/stats/rest/en/season?"

    # Sorting parameters
    if sort is not None:
        # Construct the sort parameters
        sort_params = construct_sorting_params(sort, direction, input_validation)
        url += sort_params

    # Filter parameters
    if filter:
        if sort is not None:
            url += "&"
        if isinstance(filter, str):
            url += f"include={filter}"
        elif isinstance(filter, list):
            url += "&".join([f"include={f}" for f in filter])

    # Make API request
    data = make_api_request(url, input_validation=input_validation)

    if data is None:
        return None

    return data

def get_draftrounds(sort="draftYear", direction="DESC", filter=None, input_validation=True):
    """
    Fetch data from the NHL API 'draft' endpoint.

    Parameters:
    - sort (str or list, optional): Field to sort the draft rounds by. Default is 'draftYear'.
    - direction (str or list): Direction of sorting. Default is 'DESC'.
    - filter (str or list, optional): The fields to include in the json response. Default is 'None' which returns all fields.
    - input_validation (bool): Flag to enable/disable input validation. Default is 'True'.

    Returns:
    - dict: Draft round data as a json dictionary.
    - None: In case of an error.
    """
    
    # Validate input parameters
    if input_validation:
        # Validate sort parameter
        if sort is not None and not validate_field(sort, key="draftrounds"):
            raise ValueError("(get_draftrounds) Invalid sort field. Valid sorting fields include strings: 'draftYear', 'id', 'rounds'.")

        # Validate direction parameter
        if not validate_sort_direction(direction):
            raise ValueError(f"(get_draftrounds) Invalid sort direction='{direction}'. Valid sorting options are 'ASC' and 'DESC'.")

        # Validate sort parameter
        if filter is not None and not validate_field(filter, key="draftrounds"):
            raise ValueError("(get_draftrounds) Invalid filter field. Valid fields include strings: 'draftYear', 'id', 'rounds'.")

    # URL for the 'draft' endpoint with sort and direction parameters
    url = f"https://api.nhle.com/stats/rest/en/draft?"

    # Sorting parameters
    if sort is not None:
        # Construct the sort parameters
        sort_params = construct_sorting_params(sort, direction, input_validation)
        url += sort_params
    
    # Filter parameters
    if filter:
        if sort is not None:
            url += "&"
        if isinstance(filter, str):
            url += f"include={filter}"
        elif isinstance(filter, list):
            url += "&".join([f"include={f}" for f in filter])

    # Make API request
    data = make_api_request(url, input_validation=input_validation)

    if data is None:
        return None

    return data

def get_players(player_limit=None, is_active=None, input_validation=True):
    """
    Fetch data from the NHL API 'players' endpoint.

    Parameters:
    - is_active (bool, optional): Whether the players are active (True to return active players, False to return incactive players). Default is 'None' which returns all players.
    - player_limit (int, optional): The max number of players to return.  Default is 'None'. There are approximately '2184' active players, and '19986' inactive players.
    - input_validation (bool): Flag to enable/disable input validation. Default is 'True'.

    Returns:
    - dict: Player data as a json dictionary.
    - None: In case of an error.
    """

    if input_validation:
        # Validate team_code parameter
        if is_active is not None and not validate_boolean(is_active):
            raise ValueError(f"(get_players) Invalid is_active='{is_active}'. Valid options are 'TRUE' and 'FALSE'.")

        # Validate season parameter
        if player_limit is not None and not validate_integer(player_limit):
            raise ValueError(f"(get_players) Invalid player_limit='{player_limit}'. Must be a positive integer.")

    # Adjust the player limit to the number of players
    if player_limit is None:
        if is_active is not None and is_active:
            limit = 2500
        elif is_active is not None and not is_active:
            limit = 22000
        else:
            limit = 25000 # all active and inactive players
    else:
        limit = player_limit

    # Construct the URL for the 'player' endpoint
    base_url = "https://search.d3.nhle.com/api/v1/search/player?culture=en-us"
    url = f"{base_url}&limit={limit}&q=%2A"

    # Check if player is active
    if is_active is not None:
        url += f"&active={is_active}"

    # Make API request
    data = make_api_request(url, input_validation=input_validation)

    if data is None:
        return None

    return data

def get_roster(team_code, season, input_validation=True):
    """
    Fetch data from the NHL API 'team roster' endpoint.

    Parameters:
    - team_code (str): The abbreviated code of the team, (ex. 'TOR').
    - season (str): The season in the format of '20232024'.
    - input_validation (bool): Flag to enable/disable input validation. Default is 'True'.

    Returns:
    - dict: Player roster data as a json dictionary.
    - None: In case of an error.
    """

    if input_validation:
        # Validate team_code parameter
        if not validate_team_code(team_code, return_fields=False):
            valid_team_codes = validate_team_code(team_code, return_fields=True)
            raise ValueError(f"(get_roster) Invalid team_code='{team_code}'. Valid team codes include: {valid_team_codes}")

        # Validate season parameter
        if not validate_season(season=season, team_code=team_code, return_fields=False):
            valid_seasons = get_roster_seasons(team_code=team_code, input_validation=input_validation)
            raise ValueError(f"(get_roster) Invalid season='{season}'. Valid seasons include: {valid_seasons}")

    # Construct the URL for the 'roster' endpoint with sort and direction parameters
    base_url = "https://api-web.nhle.com/v1/roster/"
    url = f"{base_url}{team_code}/{season}?"

    # Make API request
    data = make_api_request(url, input_validation=input_validation)

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
        if not validate_team_code(team_code, return_fields=False):
            valid_team_codes = validate_team_code(team_code, return_fields= True)
            raise ValueError(f"(get_roster_season) Invalid team_code='{team_code}'. Valid team codes include: {valid_team_codes}")

    # Construct the URL for the 'roster' endpoint with sort and direction parameters
    base_url = "https://api-web.nhle.com/v1/roster-season/"
    url = f"{base_url}{team_code}"

    # Make API request using the helper function
    data = make_api_request(url, input_validation=input_validation)

    if data is None:
        return None

    return data

def get_player_landing(player_id, view=None, input_validation=True):
    """
    Fetch data from the NHL API 'player/landing' endpoint.

    Parameters:
    - player_id (int): The ID of the player.
    - view (str): The part of the json to return, use '.' as a delimiter for subfields. Default is None (to return everything).
    - input_validation (bool): Flag to enable/disable input validation. Default is True.

    Returns:
    - dict: Player landing data as a json dictionary.
    - None: In case of an error.
    """

    if input_validation:
        # Validate player_id
        if not validate_players(player=player_id, key="playerId", return_fields=False):
            valid_player_ids = validate_players(player=player_id, key="playerId", return_fields=True)
            raise ValueError(f"Invalid player_id='{player_id}'. Valid fields include: {valid_player_ids}.")

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
        # Split the view string by "." to handle nested fields
        fields = view.split(".")
        filtered_data = data
        for field in fields:
            # Check if the current field exists in the filtered data
            if isinstance(filtered_data, dict) and field in filtered_data:
                filtered_data = filtered_data[field]
            else:
                raise ValueError(f"Invalid view parameter. Field '{field}' not found or not a valid subfield.")
        return filtered_data

    return data
   
def get_player_gamelog(player_id, season, game_type=2, view="gameLog", input_validation=True):
    """
    Fetch data from the NHL API player 'gamelog' endpoint.

    Parameters:
    - player_id (int): The ID of the player.
    - season (str): The season to return the gamelog from, (ex. '20232024').
    - game_type (int): The type of game (2 for regular season, 3 for playoffs). Default is 2.
    - view (str): The part of the json to return, use '.' as a delimiter for subfields. Default is None (to return everything).
    - input_validation (bool): Flag to enable/disable input validation. Default is True.

    Returns:
    - dict: Player gamelog data as a json dictionary based on the specified view.
    - None: In case of an error.
    """

    if input_validation:
        # Validate player_id
        if not validate_players(player=player_id, key="playerId", return_fields=False):
            valid_player_ids = validate_players(player=player_id, key="playerId", return_fields=True)
            raise ValueError(f"(get_player_gamelog) Invalid player_id='{player_id}'. Valid fields include: {valid_player_ids}.")

        #Validate season
        valid_player_seasons = validate_player_seasons(season=season, player_id=player_id, return_fields=True)
        #if not compare_list(field=season, json_list=valid_player_seasons, return_boolean=True): #TODO fix weird list comparison issues
        if not validate_season(season, return_fields=False):
            raise ValueError(f"(get_player_gamelog) Invalid season='{season}'. Valid seasons include: {valid_player_seasons}.")

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
        # Split the view string by "." to handle nested fields
        fields = view.split(".")
        filtered_data = data
        for field in fields:
            # Check if the current field exists in the filtered data
            if isinstance(filtered_data, dict) and field in filtered_data:
                filtered_data = filtered_data[field]
            else:
                raise ValueError(f"Invalid view parameter. Field '{field}' not found or not a valid subfield.")
        return filtered_data

    return data

def get_skaters_stats(season=None, report="summary", aggregate=True, min_gp=0, max_gp=None, sort=["points", "goals", "assists", "playerId"], sort_direction=["DESC", "DESC", "DESC", "ASC"], game_type=2, start_season=None, end_season=None, is_game=False, start_date=None, end_date=None, franchise_id=None, opponent_franchise_id=None, position=None, skater_full_name=None, is_rookie=None, is_active=None, is_in_hall_of_fame=None, nationality_code=None, birth_state_province_code=None, home_or_road=None, game_result=None, draft_round=None, draft_year=None, shoots=None, property=None, comparator=None, value=None, skater_limit=100, input_validation=True):
    """
    Fetch data from the NHL API skater 'skater' endpoint.

    Parameters:
    - season (str, optional): The season to return the skaters stats from (e.g., '20232024').
    - report (str): The report type to return. Available report types are 'summary', 'bios', 'faceoffpercentages', 'faceoffwins', 'goalsForAgainst', 'realtime', 'penalties', 'penaltykill', 'penaltyShots', 'powerplay', 'puckPossessions', 'summaryshooting', 'percentages', 'scoringRates', 'scoringpergame', 'shootout', 'shottype', 'timeonice'.
    - aggregate (bool): Boolean option to aggregate skaters stats over multiple seasons or games. Default is 'True'.
    - min_gp (int): The minimum number of games played. Default is '0'.
    - max_gp (int, optional): The maximum number of games played. Default is 'None'.
    - sort (str or list, optional): The sort field(s) for the query. Can be a single string or a list of strings. 'None' returns skaters with no sorting.
    - sor_direction (str or list): The sort direction(s) for the query. Can be a single string or a list of strings.
    - game_type (int, optional): The type of game ('1' for pre-season, '2' for regular season, '3' for playoffs, '4' for all-star games). Default is '2'.
    - start_season (str, optional): The starting season of the range. Default is 'None'.
    - end_season (str, optional): The ending season of the range. Default is 'None'.
    - is_game (bool): The flag for providing a range of dates. Default is 'False'.
    - start_date(str, optional): The starting date of the range (YYYY-MM-DD). Default is 'None'.
    - end_date(str, optional): The ending date of the range (YYYY-MM-DD). Default is 'None'.
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
    - draft_round (str or int, optional): The draft round of the skaters to return the stats from. Default is 'None' which returns all rounds.
    - draft_year (str or int, optional): The draft year of the skaters to return the stats from (e.g., '2012'). Note: if no draft round is input, returns from first round, and only returns data for a single draft round.  Default is 'None' which returns all draft years.
    - shoots (str, optional): The handedness of the skaters to return the stats from ('L' for left, 'R' for right). Default is 'None' which returns all skaters.
    - property (str or list, optional): The property to filter by (note: works alongside a provided comparator and value). Default is 'None'.
    - comparator (str or list, optional): The comparator to filter by ('>=', '=', and '<=') (note: works alongside a provided comparator and value). Default is 'None'.
    - value (str or int or list, optional): The value to filter by (note: works alongside a provided comparator and value). Default is 'None'.
    - skater_limit (int): The max number of skaters in one loop (loops to return all skaters regardless of limit).  Default is '100'.
    - input_validation (bool): Flag to enable/disable input validation. Default is 'True'.

    Returns:
    - list: List of dictionaries containing skater(s) season stats.
    - None: In case of an error.
    """
    if input_validation:
        if season is None and start_season is None and end_season is None and start_date is None and end_date is None:
            raise ValueError("Provide either a season, a range of seasons, or a range of dates.")

        # Validate the minimum games played parameter
        if not validate_min_gp(min_gp):
            raise ValueError(f"Invalid min_gp='{min_gp}'. Must be a positive integer.")
        
        # Validate the maximum games played parameter
        if max_gp is not None and not validate_min_gp(max_gp):
            raise ValueError(f"Invalid max_gp='{max_gp}'. Must be a positive integer.")

        # Validate the aggregate seasons parameter
        if not validate_boolean(aggregate):
            raise ValueError(f"Invalid aggregate='{aggregate}'. Valid fields include: 'True', 'False'.")

        # Validate the season parameter for player
        if season is not None:
            if not validate_season(season=season, return_fields=False):
                valid_seasons = validate_season(season=season, return_fields=True)
                raise ValueError(f"Invalid season='{season}'. Valid seasons include: {valid_seasons}.")

        # Validate the report parameter
        if not validate_report(report=report, key="skaters"):
            valid_fields = validate_report(key="skaters", return_fields=True)
            raise ValueError(f"Invalid report='{report}'. Valid report types include: {valid_fields}.")
        
        # Validate the sort field parameter
        if sort is not None:
             valid_sort_fields = validate_fields(field=sort, report=report, key="skaters", is_game=is_game, return_fields=True)
             if not compare_list(field=sort, json_list=valid_sort_fields, return_boolean=True):
                raise ValueError(f"Invalid sort_field='{sort}'. Valid fields include: {valid_sort_fields}.")

        # Validate the sort direction parameter
        if sort_direction is not None and not validate_sort_direction(sort_direction):
            raise ValueError(f"Invalid sort_direction='{sort_direction}'. Valid fields are 'ASC', 'DESC'.")

        # Validate the game type parameter
        if game_type is not None and not validate_game_type(game_type):
            raise ValueError(f"Invalid game_type='{game_type}'. Valid fields are '1', '2', '3', '4'.")

        # Validate start_season and end_season if provided
        if start_season is not None:
            if not validate_season(season=start_season, return_fields=False):
                valid_seasons = validate_season(season=start_season, return_fields=True)
                raise ValueError(f"Invalid start_season='{start_season}'. Valid seasons include: {valid_seasons}")

        if end_season is not None:
            if not validate_season(season=end_season, return_fields=False):
                valid_seasons = validate_season(season=end_season, return_fields=True)
                raise ValueError(f"Invalid end_season='{end_season}'. Valid seasons include: {valid_seasons}")
        
        # Validate the franchise_id if provided
        if franchise_id is not None:
            if not validate_franchise_id(franchise_id, return_fields=False):
                valid_franchise_ids = validate_franchise_id(franchise_id, return_fields=True)
                raise ValueError(f"Invalid franchise_id='{franchise_id}'. Valid fields include: {valid_franchise_ids}.")
        
        # Validate the franchise_id if provided
        if opponent_franchise_id is not None:
            if not validate_franchise_id(opponent_franchise_id, return_fields=False):
                valid_opp_franchise_ids = validate_franchise_id(franchise_id, return_fields=True)
                raise ValueError(f"Invalid opponent_franchise_id='{opponent_franchise_id}'. Valid fields include: {valid_opp_franchise_ids}.")
        
        # Validate position if provided
        if position is not None and not validate_position(position):
            raise ValueError(f"Invalid position='{position}'. Valid fields include: 'C', 'L', 'R', 'D'.")

        # Validate the skater_full_name if provided
        if skater_full_name is not None:
            if not validate_players(player=skater_full_name, key="name", is_active=is_active, return_fields=False):
                valid_names = validate_players(player=skater_full_name, key="name", is_active=is_active, return_fields=True)
                raise ValueError(f"Invalid skater_full_name='{skater_full_name}'. Valid fields include: {valid_names}.")

        # Validate is_rookie if provided
        if is_rookie is not None and not validate_boolean(is_rookie):
            raise ValueError(f"Invalid is_rookie parameter='{is_rookie}'. Valid fields include: 'True', 'False'.")

        # Validate skater_limit
        if not validate_integer(skater_limit) or not int(skater_limit)>0:
            raise ValueError(f"Invalid skater_limit='{skater_limit}'. Must be a positive integer.")
        
        # Validate is_active if provided
        if is_active is not None and not validate_boolean(is_active):
            raise ValueError(f"Invalid is_active='{is_active}'. Valid fields include: 'True', 'False'.")
        
        # Validate is_in_hall_of_fame if provided
        if is_in_hall_of_fame is not None and not validate_boolean(is_in_hall_of_fame):
            raise ValueError(f"Invalid is_in_hall_of_fame='{is_in_hall_of_fame}'. Valid fields include: 'True', 'False'.")
        
        # Validate nationality_code if provided
        if nationality_code is not None:
            if not validate_countries(code=nationality_code, key="nationalityCode", return_fields=False):
                valid_nationality_codes = validate_countries(code=nationality_code, key="nationalityCode", return_fields=True)
                raise ValueError(f"Invalid nationality_code='{nationality_code}'. Valid fields include: {valid_nationality_codes}.")
        
        # Validate birth_state_province_code if provided
        if birth_state_province_code is not None:
            if not validate_countries(code=birth_state_province_code, key="birthStateProvinceCode", return_fields=False):
                valid_birth_state_province_codes = validate_countries(code=birth_state_province_code, key="birthStateProvinceCode", return_fields=True)
                raise ValueError(f"Invalid birth_state_province_code='{birth_state_province_code}'. Valid fields include: {valid_birth_state_province_codes}.")
        
        # Validate home_or_road if provided
        if home_or_road is not None and not validate_home_road(home_or_road):
            raise ValueError(f"Invalid home_or_road='{home_or_road}'. Valid fields include: 'H', 'R'.")
        
        # Validate game_result if provided
        if game_result is not None and not validate_game_result(game_result):
            raise ValueError(f"Invalid game_result='{game_result}'. Valid fields include: 'W', 'L', 'O'.")
        
        # Validate draft_round if provided
        if draft_round is not None:
            if not validate_draftrounds(draft_round=draft_round, key="rounds", return_fields=False):
                valid_draft_rounds = validate_draftrounds(draft_round=draft_round, key="rounds", return_fields=True)
                raise ValueError(f"Invalid draft_round='{draft_round}'. Valid fields include: {valid_draft_rounds}.")
        
        # Validate draft_year if provided
        if draft_year is not None:
            if not validate_draftrounds(draft_round=draft_year, key="draftYear", return_fields=False):
                valid_draft_years = validate_draftrounds(draft_round=draft_year, key="draftYear", return_fields=True)
                raise ValueError(f"Invalid draft_year='{draft_year}'. Valid fields include: {valid_draft_years}.")
        
        if shoots is not None and not validate_string(shoots):
            raise ValueError(f"Invalid shoots='{shoots}'. Valid fields include: 'L', 'R'.")

        # Validate start_date if provided
        if start_date is not None:
            formatted_start_date = format_date(start_date)
            if not formatted_start_date:
                raise ValueError(f"Invalid start_date='{start_date}'. Provide the date in 'YYYY-MM-DD' format.")
        
        # Validate end_date if provided
        if end_date is not None:
            formatted_end_date = format_date(end_date)
            if not formatted_end_date:
                raise ValueError(f"Invalid end_date='{end_date}'. Provide the date in 'YYYY-MM-DD' format.")
        
        # Validate is_game
        if not validate_boolean(is_game):
            raise ValueError(f"Invalid is_game='{is_game}'. Valid fields include: 'True', 'False'.")

    # Construct the URL for the 'skater' endpoint
    base_url = "https://api.nhle.com/stats/rest/en/skater/" + report

    # Construct the cayenneExp
    if start_season is not None and end_season is not None:
        cayenneExp = f"seasonId<={end_season} and seasonId>={start_season}"
    elif start_date is not None and end_date is not None:
        season = None
        is_game = True
        formatted_start_date = format_date(start_date)
        formatted_end_date = format_date(end_date)
        cayenneExp = f"gameDate<='{formatted_end_date}' and gameDate>='{formatted_start_date}'"
    elif season is not None:
        cayenneExp = f"seasonId={season}"

    if game_type is not None:
        cayenneExp += f" and gameTypeId={game_type}"
    
    if franchise_id is not None:
        cayenneExp += f" and franchiseId={int(franchise_id)}"

    if opponent_franchise_id is not None:
        cayenneExp += f" and opponentFranchiseId={int(opponent_franchise_id)}"

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
        cayenneExp += f" and homeRoad='{home_or_road.upper()}'"

    if game_result is not None:
        cayenneExp += f" and decision='{game_result.upper()}'"

    if draft_round is not None:
        cayenneExp += f" and draftRound={draft_round}"

    if draft_year is not None:
        cayenneExp += f" and draftYear='{draft_year}'"

    if shoots is not None:
        cayenneExp += f" and shootsCatches='{shoots.upper()}'"

    # Construct the factCayenneExp 
    factCayenneExp = f"gamesPlayed>={min_gp}"

    if max_gp is not None:
        factCayenneExp += f" and gamesPlayed<={max_gp}"
    
    if property is not None:
        # Convert to lists if they are not already
        property = property if isinstance(property, list) else [property]
        comparator = comparator if isinstance(comparator, list) else [comparator]
        value = value if isinstance(value, list) else [value]

        # Construct the factCayenneExp parameters
        for prop, comp, val in zip(property, comparator, value):
            factCayenneExp += f" and {prop}{comp}{val}"

    # Construct the query parameters
    params = {
        "isAggregate": str(aggregate),
        "isGame": str(is_game),
        "start": "0",
        "limit": str(skater_limit),
        "factCayenneExp": factCayenneExp,
        "cayenneExp": cayenneExp
    }

    if sort is not None:
        # Convert sort and direction to lists if they are not already
        sort = sort if isinstance(sort, list) else [sort]
        sort_direction = sort_direction if isinstance(sort_direction, list) else [sort_direction]

        # Construct the sort parameters
        sort_params = [{"property": field, "direction": dir} for field, dir in zip(sort, sort_direction)]
        sort_json = json.dumps(sort_params)
        params["sort"] = sort_json

    # Initialize an empty list to store the results
    all_skaters_data = []

    # Loop over multiple times to fetch all skaters
    while True:
        # Construct the complete URL
        url = f"{base_url}?{'&'.join([f'{key}={value}' for key, value in params.items()])}"

        # Make API request
        data = make_api_request(url, input_validation=input_validation)

        if data is None:
            return None

        all_skaters_data.extend(data.get("data", []))

        # Check if there are more players to fetch
        if len(all_skaters_data) >= data.get("total", 0):
            break

        # Update the starting position for the next request
        params["start"] = str(len(all_skaters_data))

    return all_skaters_data

#TODO test edge cases
def get_goalies_stats(season=None, report="summary", aggregate=True, min_gp=0, max_gp=None, sort=["points", "goals", "assists", "playerId"], sort_direction=["DESC", "DESC", "DESC", "ASC"], game_type=2, start_season=None, end_season=None, is_game=False, start_date=None, end_date=None, franchise_id=None, opponent_franchise_id=None, position=None, goalie_full_name=None, is_rookie=None, is_active=None, is_in_hall_of_fame=None, nationality_code=None, birth_state_province_code=None, home_or_road=None, game_result=None, draft_round=None, draft_year=None, catches=None, property=None, comparator=None, value=None, skater_limit=100, input_validation=True):
    """
    Fetch data from the NHL API 'goalie' endpoint.

    Parameters:
    - season (str, optional): The season to return the goalies stats from (e.g., '20232024').
    - report (str): The report type to return. Available report types are 'summary', 'bios', 'faceoffpercentages', 'faceoffwins', 'goalsForAgainst', 'realtime', 'penalties', 'penaltykill', 'penaltyShots', 'powerplay', 'puckPossessions', 'summaryshooting', 'percentages', 'scoringRates', 'scoringpergame', 'shootout', 'shottype', 'timeonice'.
    - aggregate (bool): Boolean option to aggregate goalies stats over multiple seasons or games. Default is 'True'.
    - min_gp (int): The minimum number of games played. Default is '0'.
    - max_gp (int, optional): The maximum number of games played. Default is 'None'.
    - sort (str or list, optional): The sort field(s) for the query. Can be a single string or a list of strings. 'None' returns goalies with no sorting.
    - sor_direction (str or list): The sort direction(s) for the query. Can be a single string or a list of strings.
    - game_type (int, optional): The type of game ('1' for pre-season, '2' for regular season, '3' for playoffs, '4' for all-star games). Default is '2'.
    - start_season (str, optional): The starting season of the range. Default is 'None'.
    - end_season (str, optional): The ending season of the range. Default is 'None'.
    - is_game (bool): The flag for providing a range of dates. Default is 'False'.
    - start_date(str, optional): The starting date of the range (YYYY-MM-DD). Default is 'None'.
    - end_date(str, optional): The ending date of the range (YYYY-MM-DD). Default is 'None'.
    - franchise_id (int, optional): The franchise identifier to return the goalies stats from. Default is 'None' which returns all franchises.
    - opponent_franchise_id (int, optional): The opponent franchise identifier to return the goalies stats from. Default is 'None' which returns all opponent franchises.
    - position (str or list, optional): The positions of the goalies. Default is 'None' which returns all positions.
    - goalie_full_name (str, optional): The full name of the goalie to filter. Default is 'None' which returns all goalies.
    - is_rookie (bool, optional): Whether the goalies are a rookie (True to return rookies, False to exclude rookies / return veterans). Default is 'None' which returns all goalies.
    - is_active (bool, optional): Whether the goalies are active (True to return active goalies, False to return incactive goalies). Default is 'None' which returns all goalies.
    - is_in_hall_of_fame (bool, optional): Wether the goalies are in the hall of fame. Default is 'None' which returns all goalies.
    - nationality_code (str, optional): The nationlity code of the goalies to return the stats from (e.g., 'CAN'). Default is 'None' which returns all nationalities.
    - birth_state_province_code (str, optional): The birth state province code of the goalies to return the stats from (e.g., 'ON'). Default is 'None' which returns all birth state provinces.
    - home_or_road (str, optional): The goalies stats from home or away games ('H' for home, 'R' for road/away).  Default is 'None' which returns all games.
    - game_result (str, optional): The goalies stats from games with the provided result ('W' for wins, 'L' for losses, and 'O' for overtime losses). Default is 'None' which returns all game results.
    - draft_round (str or int, optional): The draft round of the goalies to return the stats from. Default is 'None' which returns all rounds.
    - draft_year (str or int, optional): The draft year of the goalies to return the stats from (e.g., '2012'). Note: if no draft round is input, returns from first round, and only returns data for a single draft round.  Default is 'None' which returns all draft years.
    - catches (str, optional): The handedness of the goalies to return the stats from ('L' for left, 'R' for right). Default is 'None' which returns all goalies.
    - property (str or list, optional): The property to filter by (note: works alongside a provided comparator and value). Default is 'None'.
    - comparator (str or list, optional): The comparator to filter by ('>=', '=', and '<=') (note: works alongside a provided comparator and value). Default is 'None'.
    - value (str or int or list, optional): The value to filter by (note: works alongside a provided comparator and value). Default is 'None'.
    - skater_limit (int): The max number of goalies in one loop (loops to return all goalies regardless of limit).  Default is '100'.
    - input_validation (bool): Flag to enable/disable input validation. Default is 'True'.

    Returns:
    - list: List of dictionaries containing goalie(s) season stats.
    - None: In case of an error.
    """
    if input_validation:
        if season is None and start_season is None and end_season is None and start_date is None and end_date is None:
            raise ValueError("Provide either a season, a range of seasons, or a range of dates.")

        # Validate the minimum games played parameter
        if not validate_min_gp(min_gp):
            raise ValueError(f"Invalid min_gp='{min_gp}'. Must be a positive integer.")
        
        # Validate the maximum games played parameter
        if max_gp is not None and not validate_min_gp(max_gp):
            raise ValueError(f"Invalid max_gp='{max_gp}'. Must be a positive integer.")

        # Validate the aggregate seasons parameter
        if not validate_boolean(aggregate):
            raise ValueError(f"Invalid aggregate='{aggregate}'. Valid fields include: 'True', 'False'.")

        # Validate the season parameter for player
        if season is not None:
            if not validate_season(season=season, return_fields=False):
                valid_seasons = validate_season(season=season, return_fields=True)
                raise ValueError(f"Invalid season='{season}'. Valid seasons include: {valid_seasons}.")

        # Validate the report parameter
        if not validate_report(report=report, key="skaters"):
            valid_fields = validate_report(key="skaters", return_fields=True)
            raise ValueError(f"Invalid report='{report}'. Valid report types include: {valid_fields}.")
        
        # Validate the sort field parameter
        if sort is not None:
             valid_sort_fields = validate_fields(field=sort, report=report, key="skaters", is_game=is_game, return_fields=True)
             if not compare_list(field=sort, json_list=valid_sort_fields, return_boolean=True):
                raise ValueError(f"Invalid sort_field='{sort}'. Valid fields include: {valid_sort_fields}.")

        # Validate the sort direction parameter
        if sort_direction is not None and not validate_sort_direction(sort_direction):
            raise ValueError(f"Invalid sort_direction='{sort_direction}'. Valid fields are 'ASC', 'DESC'.")

        # Validate the game type parameter
        if game_type is not None and not validate_game_type(game_type):
            raise ValueError(f"Invalid game_type='{game_type}'. Valid fields are '1', '2', '3', '4'.")

        # Validate start_season and end_season if provided
        if start_season is not None:
            if not validate_season(season=start_season, return_fields=False):
                valid_seasons = validate_season(season=start_season, return_fields=True)
                raise ValueError(f"Invalid start_season='{start_season}'. Valid seasons include: {valid_seasons}")

        if end_season is not None:
            if not validate_season(season=end_season, return_fields=False):
                valid_seasons = validate_season(season=end_season, return_fields=True)
                raise ValueError(f"Invalid end_season='{end_season}'. Valid seasons include: {valid_seasons}")
        
        # Validate the franchise_id if provided
        if franchise_id is not None:
            if not validate_franchise_id(franchise_id, return_fields=False):
                valid_franchise_ids = validate_franchise_id(franchise_id, return_fields=True)
                raise ValueError(f"Invalid franchise_id='{franchise_id}'. Valid fields include: {valid_franchise_ids}.")
        
        # Validate the franchise_id if provided
        if opponent_franchise_id is not None:
            if not validate_franchise_id(opponent_franchise_id, return_fields=False):
                valid_opp_franchise_ids = validate_franchise_id(franchise_id, return_fields=True)
                raise ValueError(f"Invalid opponent_franchise_id='{opponent_franchise_id}'. Valid fields include: {valid_opp_franchise_ids}.")
        
        # Validate position if provided
        if position is not None and not validate_position(position):
            raise ValueError(f"Invalid position='{position}'. Valid fields include: 'C', 'L', 'R', 'D'.")

        # Validate the skater_full_name if provided
        if goalie_full_name is not None:
            if not validate_players(player=goalie_full_name, key="name", is_active=is_active, return_fields=False):
                valid_names = validate_players(player=goalie_full_name, key="name", is_active=is_active, return_fields=True)
                raise ValueError(f"Invalid skater_full_name='{goalie_full_name}'. Valid fields include: {valid_names}.")

        # Validate is_rookie if provided
        if is_rookie is not None and not validate_boolean(is_rookie):
            raise ValueError(f"Invalid is_rookie parameter='{is_rookie}'. Valid fields include: 'True', 'False'.")

        # Validate skater_limit
        if not validate_integer(skater_limit) or not int(skater_limit)>0:
            raise ValueError(f"Invalid skater_limit='{skater_limit}'. Must be a positive integer.")
        
        # Validate is_active if provided
        if is_active is not None and not validate_boolean(is_active):
            raise ValueError(f"Invalid is_active='{is_active}'. Valid fields include: 'True', 'False'.")
        
        # Validate is_in_hall_of_fame if provided
        if is_in_hall_of_fame is not None and not validate_boolean(is_in_hall_of_fame):
            raise ValueError(f"Invalid is_in_hall_of_fame='{is_in_hall_of_fame}'. Valid fields include: 'True', 'False'.")
        
        # Validate nationality_code if provided
        if nationality_code is not None:
            if not validate_countries(code=nationality_code, key="nationalityCode", return_fields=False):
                valid_nationality_codes = validate_countries(code=nationality_code, key="nationalityCode", return_fields=True)
                raise ValueError(f"Invalid nationality_code='{nationality_code}'. Valid fields include: {valid_nationality_codes}.")
        
        # Validate birth_state_province_code if provided
        if birth_state_province_code is not None:
            if not validate_countries(code=birth_state_province_code, key="birthStateProvinceCode", return_fields=False):
                valid_birth_state_province_codes = validate_countries(code=birth_state_province_code, key="birthStateProvinceCode", return_fields=True)
                raise ValueError(f"Invalid birth_state_province_code='{birth_state_province_code}'. Valid fields include: {valid_birth_state_province_codes}.")
        
        # Validate home_or_road if provided
        if home_or_road is not None and not validate_home_road(home_or_road):
            raise ValueError(f"Invalid home_or_road='{home_or_road}'. Valid fields include: 'H', 'R'.")
        
        # Validate game_result if provided
        if game_result is not None and not validate_game_result(game_result):
            raise ValueError(f"Invalid game_result='{game_result}'. Valid fields include: 'W', 'L', 'O'.")
        
        # Validate draft_round if provided
        if draft_round is not None:
            if not validate_draftrounds(draft_round=draft_round, key="rounds", return_fields=False):
                valid_draft_rounds = validate_draftrounds(draft_round=draft_round, key="rounds", return_fields=True)
                raise ValueError(f"Invalid draft_round='{draft_round}'. Valid fields include: {valid_draft_rounds}.")
        
        # Validate draft_year if provided
        if draft_year is not None:
            if not validate_draftrounds(draft_round=draft_year, key="draftYear", return_fields=False):
                valid_draft_years = validate_draftrounds(draft_round=draft_year, key="draftYear", return_fields=True)
                raise ValueError(f"Invalid draft_year='{draft_year}'. Valid fields include: {valid_draft_years}.")
        
        if catches is not None and not validate_string(catches):
            raise ValueError(f"Invalid shoots='{catches}'. Valid fields include: 'L', 'R'.")

        # Validate start_date if provided
        if start_date is not None:
            formatted_start_date = format_date(start_date)
            if not formatted_start_date:
                raise ValueError(f"Invalid start_date='{start_date}'. Provide the date in 'YYYY-MM-DD' format.")
        
        # Validate end_date if provided
        if end_date is not None:
            formatted_end_date = format_date(end_date)
            if not formatted_end_date:
                raise ValueError(f"Invalid end_date='{end_date}'. Provide the date in 'YYYY-MM-DD' format.")
        
        # Validate is_game
        if not validate_boolean(is_game):
            raise ValueError(f"Invalid is_game='{is_game}'. Valid fields include: 'True', 'False'.")

    # Construct the URL for the 'skater' endpoint
    base_url = "https://api.nhle.com/stats/rest/en/skater/" + report

    # Construct the cayenneExp
    if start_season is not None and end_season is not None:
        cayenneExp = f"seasonId<={end_season} and seasonId>={start_season}"
    elif start_date is not None and end_date is not None:
        season = None
        is_game = True
        formatted_start_date = format_date(start_date)
        formatted_end_date = format_date(end_date)
        cayenneExp = f"gameDate<='{formatted_end_date}' and gameDate>='{formatted_start_date}'"
    elif season is not None:
        cayenneExp = f"seasonId={season}"

    if game_type is not None:
        cayenneExp += f" and gameTypeId={game_type}"
    
    if franchise_id is not None:
        cayenneExp += f" and franchiseId={int(franchise_id)}"

    if opponent_franchise_id is not None:
        cayenneExp += f" and opponentFranchiseId={int(opponent_franchise_id)}"

    if position is not None:
        if isinstance(position, str):
            cayenneExp += f" and positionCode='{position}'"
        elif isinstance(position, list):
            position_exp = " or ".join([f"positionCode='{pos}'" for pos in position])
            cayenneExp += f" and ({position_exp})"

    if goalie_full_name is not None:
        cayenneExp += f" and skaterFullName likeIgnoreCase '%{goalie_full_name}%'"

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
        cayenneExp += f" and homeRoad='{home_or_road.upper()}'"

    if game_result is not None:
        cayenneExp += f" and decision='{game_result.upper()}'"

    if draft_round is not None:
        cayenneExp += f" and draftRound={draft_round}"

    if draft_year is not None:
        cayenneExp += f" and draftYear='{draft_year}'"

    if catches is not None:
        cayenneExp += f" and shootsCatches='{catches.upper()}'"

    # Construct the factCayenneExp 
    factCayenneExp = f"gamesPlayed>={min_gp}"

    if max_gp is not None:
        factCayenneExp += f" and gamesPlayed<={max_gp}"
    
    if property is not None:
        # Convert to lists if they are not already
        property = property if isinstance(property, list) else [property]
        comparator = comparator if isinstance(comparator, list) else [comparator]
        value = value if isinstance(value, list) else [value]

        # Construct the factCayenneExp parameters
        for prop, comp, val in zip(property, comparator, value):
            factCayenneExp += f" and {prop}{comp}{val}"

    # Construct the query parameters
    params = {
        "isAggregate": str(aggregate),
        "isGame": str(is_game),
        "start": "0",
        "limit": str(skater_limit),
        "factCayenneExp": factCayenneExp,
        "cayenneExp": cayenneExp
    }

    if sort is not None:
        # Convert sort and direction to lists if they are not already
        sort = sort if isinstance(sort, list) else [sort]
        sort_direction = sort_direction if isinstance(sort_direction, list) else [sort_direction]

        # Construct the sort parameters
        sort_params = [{"property": field, "direction": dir} for field, dir in zip(sort, sort_direction)]
        sort_json = json.dumps(sort_params)
        params["sort"] = sort_json

    # Initialize an empty list to store the results
    all_goalies_data = []

    # Loop over multiple times to fetch all goalies
    while True:
        # Construct the complete URL
        url = f"{base_url}?{'&'.join([f'{key}={value}' for key, value in params.items()])}"

        # Make API request
        data = make_api_request(url, input_validation=input_validation)

        if data is None:
            return None

        all_goalies_data.extend(data.get("data", []))

        # Check if there are more goalies to fetch
        if len(all_goalies_data) >= data.get("total", 0):
            break

        # Update the starting position for the next request
        params["start"] = str(len(all_goalies_data))

    return all_goalies_data

#TODO test edge cases
def get_teams_stats(season=None, report="summary", aggregate=True, min_gp=0, max_gp=None, sort=["points", "wins", "franchiseId"], sort_direction=["DESC", "DESC", "ASC"], game_type=2, start_season=None, end_season=None, is_game=False, start_date=None, end_date=None, franchise_id=None, opponent_franchise_id=None, home_or_road=None, game_result=None, property=None, comparator=None, value=None, team_limit=50, input_validation=True):
    """
    Fetch data from the NHL API skater 'team' endpoint.

    Parameters:
    - season (str, optional): The season to return the tams stats from (e.g., '20232024').
    - report (str): The report type to return. Available report types are 'summary', 'bios', 'faceoffpercentages', 'faceoffwins', 'goalsForAgainst', 'realtime', 'penalties', 'penaltykill', 'penaltyShots', 'powerplay', 'puckPossessions', 'summaryshooting', 'percentages', 'scoringRates', 'scoringpergame', 'shootout', 'shottype', 'timeonice'.
    - aggregate (bool): Boolean option to aggregate teams stats over multiple seasons or games. Default is 'True'.
    - min_gp (int): The minimum number of games played. Default is '0'.
    - max_gp (int, optional): The maximum number of games played. Default is 'None'.
    - sort (str or list, optional): The sort field(s) for the query. Can be a single string or a list of strings. 'None' returns teams with no sorting.
    - sort_direction (str or list): The sort direction(s) for the query. Can be a single string or a list of strings.
    - game_type (int, optional): The type of game ('1' for pre-season, '2' for regular season, '3' for playoffs, '4' for all-star games). Default is '2'.
    - start_season (str, optional): The starting season of the range. Default is 'None'.
    - end_season (str, optional): The ending season of the range. Default is 'None'.
    - is_game (bool): The flag for providing a range of dates. Default is 'False'.
    - start_date(str, optional): The starting date of the range (YYYY-MM-DD). Default is 'None'.
    - end_date(str, optional): The ending date of the range (YYYY-MM-DD). Default is 'None'.
    - franchise_id (int, optional): The franchise identifier to return the teams stats from. Default is 'None' which returns all franchises.
    - opponent_franchise_id (int, optional): The opponent franchise identifier to return the teams stats from. Default is 'None' which returns all opponent franchises.
    - home_or_road (str, optional): The teams stats from home or away games ('H' for home, 'R' for road/away).  Default is 'None' which returns all games.
    - game_result (str, optional): The teams stats from games with the provided result ('W' for wins, 'L' for losses, and 'O' for overtime losses). Default is 'None' which returns all game results.
    - property (str or list, optional): The property to filter by (note: works alongside a provided comparator and value). Default is 'None'.
    - comparator (str or list, optional): The comparator to filter by ('>=', '=', and '<=') (note: works alongside a provided comparator and value). Default is 'None'.
    - value (str or int or list, optional): The value to filter by (note: works alongside a provided comparator and value). Default is 'None'.
    - team_limit (int): The max number of teams in one loop (loops to return all teams regardless of limit).  Default is '50'.
    - input_validation (bool): Flag to enable/disable input validation. Default is 'True'.

    Returns:
    - list: List of dictionaries containing skater(s) season stats.
    - None: In case of an error.
    """
    if input_validation:
        if season is None and start_season is None and end_season is None and start_date is None and end_date is None:
            raise ValueError("Provide either a season, a range of seasons, or a range of dates.")

        # Validate the minimum games played parameter
        if not validate_min_gp(min_gp):
            raise ValueError(f"Invalid min_gp='{min_gp}'. Must be a positive integer.")
        
        # Validate the maximum games played parameter
        if max_gp is not None and not validate_min_gp(max_gp):
            raise ValueError(f"Invalid max_gp='{max_gp}'. Must be a positive integer.")

        # Validate the aggregate seasons parameter
        if not validate_boolean(aggregate):
            raise ValueError(f"Invalid aggregate='{aggregate}'. Valid fields include: 'True', 'False'.")

        # Validate the season parameter for player
        if season is not None:
            if not validate_season(season=season, return_fields=False):
                valid_seasons = validate_season(season=season, return_fields=True)
                raise ValueError(f"Invalid season='{season}'. Valid seasons include: {valid_seasons}.")

        # Validate the report parameter
        if not validate_report(report=report, key="teams"):
            valid_fields = validate_report(key="teams", return_fields=True)
            raise ValueError(f"Invalid report='{report}'. Valid report types include: {valid_fields}.")
        
        # Validate the sort field parameter
        if sort is not None:
             valid_sort_fields = validate_fields(field=sort, report=report, key="teams", is_game=is_game, return_fields=True)
             if not compare_list(field=sort, json_list=valid_sort_fields, return_boolean=True):
                raise ValueError(f"Invalid sort_field='{sort}'. Valid fields include: {valid_sort_fields}.")

        # Validate the sort direction parameter
        if sort_direction is not None and not validate_sort_direction(sort_direction):
            raise ValueError(f"Invalid sort_direction='{sort_direction}'. Valid fields are 'ASC', 'DESC'.")

        # Validate the game type parameter
        if game_type is not None and not validate_game_type(game_type):
            raise ValueError(f"Invalid game_type='{game_type}'. Valid fields are '1', '2', '3', '4'.")

        # Validate start_season and end_season if provided
        if start_season is not None:
            if not validate_season(season=start_season, return_fields=False):
                valid_seasons = validate_season(season=start_season, return_fields=True)
                raise ValueError(f"Invalid start_season='{start_season}'. Valid seasons include: {valid_seasons}")

        if end_season is not None:
            if not validate_season(season=end_season, return_fields=False):
                valid_seasons = validate_season(season=end_season, return_fields=True)
                raise ValueError(f"Invalid end_season='{end_season}'. Valid seasons include: {valid_seasons}")
        
        # Validate the franchise_id if provided
        if franchise_id is not None:
            if not validate_franchise_id(franchise_id, return_fields=False):
                valid_franchise_ids = validate_franchise_id(franchise_id, return_fields=True)
                raise ValueError(f"Invalid franchise_id='{franchise_id}'. Valid fields include: {valid_franchise_ids}.")
        
        # Validate the franchise_id if provided
        if opponent_franchise_id is not None:
            if not validate_franchise_id(opponent_franchise_id, return_fields=False):
                valid_opp_franchise_ids = validate_franchise_id(franchise_id, return_fields=True)
                raise ValueError(f"Invalid opponent_franchise_id='{opponent_franchise_id}'. Valid fields include: {valid_opp_franchise_ids}.")

        # Validate team_limit
        if not validate_integer(team_limit) or not int(team_limit)>0:
            raise ValueError(f"Invalid team_limit='{team_limit}'. Must be a positive integer.")

        # Validate home_or_road if provided
        if home_or_road is not None and not validate_home_road(home_or_road):
            raise ValueError(f"Invalid home_or_road='{home_or_road}'. Valid fields include: 'H', 'R'.")
        
        # Validate game_result if provided
        if game_result is not None and not validate_game_result(game_result):
            raise ValueError(f"Invalid game_result='{game_result}'. Valid fields include: 'W', 'L', 'O'.")
        
        # Validate start_date if provided
        if start_date is not None:
            formatted_start_date = format_date(start_date)
            if not formatted_start_date:
                raise ValueError(f"Invalid start_date='{start_date}'. Provide the date in 'YYYY-MM-DD' format.")
        
        # Validate end_date if provided
        if end_date is not None:
            formatted_end_date = format_date(end_date)
            if not formatted_end_date:
                raise ValueError(f"Invalid end_date='{end_date}'. Provide the date in 'YYYY-MM-DD' format.")
        
        # Validate is_game
        if not validate_boolean(is_game):
            raise ValueError(f"Invalid is_game='{is_game}'. Valid fields include: 'True', 'False'.")

    # Construct the URL for the 'skater' endpoint
    base_url = "https://api.nhle.com/stats/rest/en/team/" + report

    # Construct the cayenneExp
    if start_season is not None and end_season is not None:
        cayenneExp = f"seasonId<={end_season} and seasonId>={start_season}"
    elif start_date is not None and end_date is not None:
        season = None
        is_game = True
        cayenneExp = f"gameDate<='{end_date}' and gameDate>='{start_date}'"
    elif season is not None:
        cayenneExp = f"seasonId={season} and seasonId={season}"

    if game_type is not None:
        cayenneExp += f" and gameTypeId={game_type}"
    
    if franchise_id is not None:
        cayenneExp += f" and franchiseId={franchise_id}"

    if opponent_franchise_id is not None:
        cayenneExp += f" and opponentFranchiseId={opponent_franchise_id}"

    if home_or_road is not None:
        cayenneExp += f" and homeRoad='{home_or_road}'"

    if game_result is not None:
        cayenneExp += f" and decision='{game_result}'"

    # Construct the factCayenneExp 
    factCayenneExp = f"gamesPlayed>={min_gp}"

    if max_gp is not None:
        factCayenneExp += f" and gamesPlayed<={max_gp}"
    
    if property is not None:
        # Convert to lists if they are not already
        property = property if isinstance(property, list) else [property]
        comparator = comparator if isinstance(comparator, list) else [comparator]
        value = value if isinstance(value, list) else [value]

        # Construct the factCayenneExp parameters
        for prop, comp, val in zip(property, comparator, value):
            factCayenneExp += f" and {prop}{comp}{val}"

    # Construct the query parameters
    params = {
        "isAggregate": str(aggregate),
        "isGame": str(is_game),
        "start": "0",
        "limit": str(team_limit),
        "factCayenneExp": factCayenneExp,
        "cayenneExp": cayenneExp
    }

    if sort is not None:
        # Convert sort and direction to lists if they are not already
        sort = sort if isinstance(sort, list) else [sort]
        sort_direction = sort_direction if isinstance(sort_direction, list) else [sort_direction]

        # Construct the sort parameters
        sort_params = [{"property": field, "direction": dir} for field, dir in zip(sort, sort_direction)]
        sort_json = json.dumps(sort_params)
        params["sort"] = sort_json

    # Initialize an empty list to store the results
    all_teams_data = []

    # Loop over multiple times to fetch all teams
    while True:
        # Construct the complete URL
        url = f"{base_url}?{'&'.join([f'{key}={value}' for key, value in params.items()])}"

        # Make API request
        data = make_api_request(url)

        if data is None:
            return None

        all_teams_data.extend(data.get("data", []))

        # Check if there are more teams to fetch
        if len(all_teams_data) >= data.get("total", 0):
            break

        # Update the starting position for the next request
        params["start"] = str(len(all_teams_data))

    return all_teams_data

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
        roster_data = make_api_request(url, input_validation=input_validation)
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
        roster_data = make_api_request(url, input_validation=input_validation)
        return roster_data
    except Exception as e:
        raise ValueError(f"Error fetching data: {e}")

def get_standings(date="now", input_validation=True):
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

def get_standings_seasons():
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
    - view (str): The part of the json to return, use '.' as a delimiter for subfields. Default is None (to return everything).
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
            # Split the view string by "." to handle nested fields
            fields = view.split(".")
            filtered_data = data
            for field in fields:
                # Check if the current field exists in the filtered data
                if isinstance(filtered_data, dict) and field in filtered_data:
                    filtered_data = filtered_data[field]
                else:
                    raise ValueError(f"Invalid view parameter. Field '{field}' not found or not a valid subfield.")
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
    - view (str): The part of the json to return, use '.' as a delimiter for subfields. Default is None (to return everything).
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
            # Split the view string by "." to handle nested fields
            fields = view.split(".")
            filtered_data = data
            for field in fields:
                # Check if the current field exists in the filtered data
                if isinstance(filtered_data, dict) and field in filtered_data:
                    filtered_data = filtered_data[field]
                else:
                    raise ValueError(f"Invalid view parameter. Field '{field}' not found or not a valid subfield.")
            return filtered_data

        return data

    except ValueError as e:
        # Raise a ValueError if there's an issue with the validation
        raise ValueError(str(e))

def get_shifts(game_id, sort=None, direction=None, view=None, input_validation=True):
    """
    Fetch data from the NHL API player 'shiftcharts' endpoint.

    Parameters:
    - game_id (int): The ID of the game.
    - sort (str, optional): The field to sort the data by. Default is None.
    - direction (str, optional): The sorting direction. Default is None.
    - view (str): The part of the json to return, use '.' as a delimiter for subfields. Default is None (to return everything).
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
        if sort is not None and not validate_field(sort, key="shifts"):
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

        # Filter the response based on the view parameter
        if view is not None:
            # Split the view string by "." to handle nested fields
            fields = view.split(".")
            filtered_data = data
            for field in fields:
                # Check if the current field exists in the filtered data
                if isinstance(filtered_data, dict) and field in filtered_data:
                    filtered_data = filtered_data[field]
                else:
                    raise ValueError(f"Invalid view parameter. Field '{field}' not found or not a valid subfield.")
            return filtered_data

        return data

    except ValueError as e:
        # Raise a ValueError if there's an issue with the validation
        raise ValueError(str(e))

def get_team_information(is_active=None):
    """
    Combine data from 'franchises', 'standings', and 'schedule_calendar' endpoints.

    Parameters:
    - is_active (bool, optional): Flag to specify if only active teams should be considered. Default is None.

    Returns:
    - dict: Team information combining data from 'franchises', 'standings', and 'schedule_calendar'.
    """

    # Get data from endpoints
    franchises_data = get_franchises()
    nhl_standings_data = get_standings()
    nhl_schedule_calendar = get_schedule_calendar()

    # Check if any of the required data is missing
    if None in (franchises_data, nhl_standings_data, nhl_schedule_calendar):
        return None

    # Convert franchises data into a set for faster lookup
    franchises_set = {franchise.get("fullName") for franchise in franchises_data.get("data", [])}

    # Convert active team names from nhl_standings_data into a set
    active_teams_set = {team_standings.get("teamName", {}).get("default") for team_standings in nhl_standings_data.get("standings", [])}

    # Get inactive teams
    inactive_teams = franchises_set - active_teams_set

    # Initialize dictionary to store team information
    team_info = {}

    # Active teams
    if is_active is True or (is_active is None):
        for team_name in active_teams_set:
            franchise_info = next((franchise for franchise in franchises_data.get("data", []) if franchise.get("fullName") == team_name), None)
            team_standings = next((standings_team for standings_team in nhl_standings_data.get("standings", []) if standings_team.get("teamName", {}).get("default") == team_name), None)
            team_info[team_name] = {
                "teamName": franchise_info.get("fullName"),
                "teamCommonName": franchise_info.get("teamCommonName"),
                "teamPlaceName": franchise_info.get("teamPlaceName"),
                "teamAbbrev": team_standings.get("teamAbbrev", {}).get("default") if team_standings else None,
                "conferenceAbbrev": team_standings.get("conferenceAbbrev") if team_standings else None,
                "conferenceName": team_standings.get("conferenceName") if team_standings else None,
                "divisionAbbrev": team_standings.get("divisionAbbrev") if team_standings else None,
                "divisionName": team_standings.get("divisionName") if team_standings else None,
                "franchiseId": franchise_info.get("id"),
                "firstSeasonId": franchise_info.get("firstSeason", {}).get("id"),
                "lastSeasonId": franchise_info.get("lastSeason", {}).get("id") if franchise_info.get("lastSeason") else None,
                "teamLogoLight": team_standings.get("teamLogo") if team_standings else None,
            }

    # Inactive teams
    if is_active is False or (is_active is None):
        for team_name in inactive_teams:
            franchise_info = next((franchise for franchise in franchises_data.get("data", []) if franchise.get("fullName") == team_name), None)
            team_info[team_name] = {
                "teamName": franchise_info.get("fullName"),
                "teamCommonName": franchise_info.get("teamCommonName"),
                "teamPlaceName": franchise_info.get("teamPlaceName"),
                "teamAbbrev": None,
                "franchiseId": franchise_info.get("id"),
                "firstSeasonId": franchise_info.get("firstSeason", {}).get("id"),
                "lastSeasonId": franchise_info.get("lastSeason", {}).get("id") if franchise_info.get("lastSeason") else None,
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

def get_club_schedule(team_code, period="month", date="now", view=None, input_validation=True):
    """
    Fetches schedule data from the NHL API for a specific date.

    Parameters:
    - date (str, optional): The date for which to fetch the schedule data (in 'YYYY-MM-DD' format). Default is "now".
    - period (str, optional): The period to fetch the schedule data for ('month' or 'week'). Default is 'month'.
    - team_code (str): The abbreviated code of the team, (ex. "TOR").
    - view (str): The part of the json to return, use '.' as a delimiter for subfields. Default is None (to return everything).
    - input_validation (bool): Flag to enable/disable input validation. Default is True.

    Returns:
    - dict: Schedule data as a JSON dictionary.
    - None: If there is an error fetching the data.
    """

    if input_validation:
        # Validate team_code parameter
        if not validate_team_code(team_code):
            raise ValueError("(get_club_schedule) Invalid team code.")
        
        # Validate the period parameter
        if period.lower() != "month" and period.lower() != "week":
            raise ValueError("(get_club_schedule) Invalid period. Valid periods are 'month' and 'week'.")

    if date != "now" and input_validation:
        # Validate date parameter and format if valid
        if period.lower() == "month":
            formatted_date = format_month(date)
            if not formatted_date:
                raise ValueError("(get_club_schedule) Invalid date format. Please provide the date in 'YYYY-MM-DD' format.")
        if period.lower() == "week":
            formatted_date = format_date(date)
            if not formatted_date:
                raise ValueError("(get_club_schedule) Invalid date format. Please provide the date in 'YYYY-MM-DD' format.")
    else:
        formatted_date = date

    base_url = "https://api-web.nhle.com/v1/club-schedule/"
    if formatted_date == "now":
        url = f"{base_url}{team_code}/{period.lower()}/now"
    else:
        url = f"{base_url}{team_code}/{period.lower()}/{formatted_date}"

    try:
        roster_data = make_api_request(url)

        # Filter the response based on the view parameter
        if view is not None:
            # Split the view string by "." to handle nested fields
            fields = view.split(".")
            filtered_data = roster_data
            for field in fields:
                # Check if the current field exists in the filtered data
                if isinstance(filtered_data, dict) and field in filtered_data:
                    filtered_data = filtered_data[field]
                else:
                    raise ValueError(f"Invalid view parameter. Field '{field}' not found or not a valid subfield.")
            return filtered_data

        return roster_data
    except Exception as e:
        raise ValueError(f"Error fetching data: {e}")

#TODO get club stats https://api-web.nhle.com/v1/club-stats/TOR/20222023/2
#TODO https://api.nhle.com/stats/rest/en/leaders/skaters/points?cayenneExp=season=20232024%20and%20gameType=2%20and%20player.positionCode%20=%20%27D%27
#TODO https://assets.nhle.com/mugs/nhl/20232024/TOR/8477479.png
#TODO https://assets.nhle.com/mugs/actionshots/1296x729/8477479.jpg
#TODO https://api-web.nhle.com/v1/player-spotlight
#TODO https://api.nhle.com/stats/rest/en/players
#TODO https://api.nhle.com/stats/rest/en/glossary?sort=fullName
#TODO https://api-web.nhle.com/v1/draft/rankings/now (now and year)
#TODO https://api-web.nhle.com/v1/draft/rankings/2024/1 (1 to 4)
#TODO https://records.nhl.com/site/api/record-category
#TODO https://records.nhl.com/site/api/nhl/menu?cayenneExp=parent=null&include=children&include=children.children
#TODO https://records.nhl.com/site/api/component-season
#TODO https://records.nhl.com/site/api/franchise?include=teams.id&include=teams.active&include=teams.triCode&include=teams.placeName&include=teams.commonName&include=teams.fullName&include=teams.logos&include=teams.conference.name&include=teams.division.name&include=teams.franchiseTeam.firstSeason.id&include=teams.franchiseTeam.lastSeason.id&sort=[{%22property%22:%22teamPlaceName%22},{%22property%22:%22teamCommonName%22}]

#####################################################################################################################################################
# Helper functions for the various NHL API scraper functions ########################################################################################
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

def construct_sorting_params(sort, direction, input_validation=True):
    """
    Construct sorting parameters for the API URL.

    Parameters:
    - sort (str or list): Field(s) to sort by.
    - direction (str or list): Sort direction(s) ('ASC' or 'DESC').
    - input_validation (bool): Flag to enable/disable input validation for sort and direction. Default is True.

    Returns:
    - str: Sorting parameters as an f-string.
    """
    if input_validation:
        # Validate input types
        if not isinstance(sort, (str, list)):
            raise ValueError("Invalid input type for sort parameter. Must be a string or a list.")
        if not isinstance(direction, (str, list)):
            raise ValueError("Invalid input type for direction parameter. Must be a string or a list.")

    # Convert sort and direction to lists if they are not already
    sort = sort if isinstance(sort, list) else [sort]
    direction = direction if isinstance(direction, list) else [direction]

    # Construct the sort parameters
    sort_params = [{"property": field, "direction": dir} for field, dir in zip(sort, direction)]
    sort_json = json.dumps(sort_params)

    return f"sort={sort_json}"

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

def compare_list(field, json_list, return_boolean=False):
    """
    Compare the provided field(s) against a given JSON list.

    Parameters:
    - field (str or list): The field or list of fields to compare.
    - json_list (list): The JSON list to compare against.
    - return_boolean (bool): If True, return True if all fields are in the JSON list,
                      otherwise return a dictionary of comparison results. Default is False.

    Returns:
    - bool or dict: If boolean is True, returns True if all fields are present in the JSON list,
                    False otherwise.
                    If boolean is False, returns a dictionary containing comparison results
                    for each provided field. Keys are the provided fields, and values are True
                    if the field is present in the JSON list, False otherwise.
    """
    # Convert field to a list if it's a single string
    if not isinstance(field, list):
        field = [field]

    # Check if all provided fields are in the JSON list
    if return_boolean:
        return all(f in json_list for f in field)
    else:
        # Initialize the comparison results dictionary
        compare_results = {}

        # Check if each provided field is in the JSON list
        for f in field:
            compare_results[f] = f in json_list

        return compare_results

#####################################################################################################################################################
# Input validation for the various NHL API functions ################################################################################################
#####################################################################################################################################################

def validate_team_code(team_code, team_info=None, return_fields=False):
    """
    Validate the team code.

    Parameters:
    - team_code (str): The team code to validate.
    - team_info (dict): JSON dictionary containing team information [response from team_information()].
    - return_fields (bool): If True, returns a list of team codes. If False, returns True if the team code is valid, False otherwise.

    Returns:
    - bool or list: If return_fields is False, returns True if the team code is valid, False otherwise.
                    If return_fields is True, returns a list of team codes.
    """
    # If team_info is not provided, call team_information function to retrieve team_info
    if team_info is None:
        team_info = get_team_information()

    # Check if return_fields is True
    if return_fields:
        team_abbrevs = [team_data.get("teamAbbrev") for team_data in team_info.values()]
        # Remove None values
        team_abbrevs = [abbrev for abbrev in team_abbrevs if abbrev is not None]
        # Sort alphabetically
        team_abbrevs.sort()
        return team_abbrevs

    # Check if team_code is found in any teamAbbrev field in team_info
    for team_data in team_info.values():
        if team_data.get("teamAbbrev") == team_code:
            return True

    return False

#TODO make it get the team fields instead of manually creating a dictionary
def validate_field(sort_field, key=None):
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
        "cofig": ["playerReportData", "goalieReportData", "teamReportData", "aggregatedColumns", "individualColumns"],
        "countries": ["id", "country3Code", "countryCode", "countryName", "hasPlayerStats", "imageUrl", "iocCode", "isActive", "nationalityName", "olympicUrl", "thumbnailUrl"], 
        "franchises": ["fullName", "teamCommonName", "teamPlaceName", "id"], 
        "seasons": ["id", "allStarGameInUse", "conferencesInUse", "divisionsInUse", "endDate", "entryDraftInUse", "formattedSeasonId", "minimumPlayoffMinutesForGoalieStatsLeaders", "minimumRegularGamesForGoalieStatsLeaders", "nhlStanleyCupOwner", "numberOfGames", "olympicsParticipation", "pointForOTLossInUse", "preseasonStartdate", "regularSeasonEndDate", "rowInUse", "seasonOrdinal", "startDate", "supplementalDraftInUse", "tiesInUse", "totalPlayoffGames", "totalRegularSeasonGames", "wildcardInUse"],
        "draftrounds": ["draftYear", "id", "rounds"],
        "roster": ["lastName", "firstName", "id", "firstName", "lastName", "sweaterNumber", "positionCode", "shootsCatches", "heightInInches", "heighInCentimeters", "weightInPounds", "weightInKilograms", "birthDate", "birthCity", "birthCountry", "birthStateProvince"], # need to add the rest of the fields, also for players_stats
        "skaters_stats": ["points", "evPoints", "goals", "evGoals", "otGoals", "gameWinningGoals", "assists", "playerId", "gamesPlayed", "faceoffWinPct", "penaltyMinutes"],
        "shifts": [None, "id"], #add the rest
        "skater_reports": ["summary", "bios", "faceoffpercentages", "faceoffwins", "goalsForAgainst", "realtime", "penalties", "penaltykill", "penaltyShots", "powerplay", "puckPossessions", "summaryshooting", "percentages", "scoringRates", "scoringpergame", "shootout", "shottype", "timeonice"] 
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

def validate_season(season, seasons_info=None, team_info=None, team_code=None, return_fields=False):
    """
    Validate the season.

    Parameters:
    - season (str): The season to validate.
    - seasons_info (dict, optional): Dictionary containing information about available seasons. Default is None.
    - team_info (dict, optional): Dictionary containing team information. Default is None.
    - team_code (str, optional): The team code. Default is None.
    - return_fields (bool): If True, returns all available seasons. Default is False.

    Returns:
    - bool or list: If return_fields is False, returns True if the season is valid within the available seasons
                    and can be converted to a string, False otherwise.
                    If return_fields is True, returns a list of all available seasons.
    """
    if seasons_info is None:
        # Call get_seasons function to retrieve seasons_info
        seasons_info = get_seasons()

    if seasons_info is None:
        return False  # Unable to retrieve seasons info
    
    if team_info is None:
        # Call get_team_information function to retrieve team_information
        team_info = get_team_information()

    if team_info is None:
        return False  # Unable to retrieve team info

    # Check if the season is within the available seasons
    available_seasons = [str(season_data.get("id")) for season_data in seasons_info.get("data", [])]

    # Additional check if the provided season is within the available seasons
    if str(season) not in available_seasons:
        return False
    
    # Convert season to string for comparison
    try:
        season_str = str(season)
    except ValueError:
        return False  # Cannot convert to string

    # Check if team_info is provided and team_code is not None
    if team_info and team_code is not None:
        # Check if team_code is found in any teamAbbrev field in team_info
        for team_data in team_info.values():
            if team_data.get("teamAbbrev") == team_info.get(team_code, {}).get("teamAbbrev"):
                # Get the first and last season IDs from the team information
                first_season_id = team_info.get(team_code, {}).get("firstSeasonId")
                last_season_id = team_info.get(team_code, {}).get("lastSeasonId")

                # Check if the season is earlier than the first season
                if first_season_id and season_str < str(first_season_id):
                    return False

                # Check if the season is later than the last season
                if last_season_id and season_str > str(last_season_id):
                    return False

                # If the team is found and the season is within its range, return True
                return True
        
        # If the team is not found in team_info, return False
        return False

    # If return_fields is True, return available seasons
    if return_fields:
        return available_seasons

    # Otherwise, the season is valid
    return True

def validate_draftrounds(draft_round, key='rounds', draft_info=None, return_fields=False):
    """
    Validate the draft round or year.

    Parameters:
    - draft_round (str): The round or year to validate.
    - key (str): The key to specify whether to validate 'rounds' or 'draftYear'. Default is 'rounds'.
    - draft_info (dict, optional): Dictionary containing information about available draft rounds and years. Default is None.
    - return_fields (bool): If True, returns all available rounds or years. Default is False.

    Returns:
    - bool or list: If return_fields is False, returns True if the round or year is within the available data, False otherwise.
                    If return_fields is True, returns a list of all available rounds or years.
    """
    if draft_info is None:
        # Call get_draft_info function to retrieve draft rounds and years
        draft_info = get_draftrounds()

    if draft_info is None:
        return False  # Unable to retrieve draft information
    
    # Determine the list of available rounds or years based on the key
    available_data = [str(info.get(key)) for info in draft_info.get("data", [])]
    
    # Filter the available data to unique values
    unique_data = list(set(available_data))
    
    # Sort the unique data in ascending order
    sorted_data = sorted(unique_data, key=lambda x: int(x))
    
    if return_fields:
        return sorted_data
    
    return str(draft_round) in sorted_data

def validate_players(player, key='playerId', players=None, is_active=None, return_fields=False):
    """
    Validate the player name or id based on the key.

    Parameters:
    - player (str): The name or id to validate.
    - key (str): The key to specify whether to validate 'playerId' or 'name'. Default is 'player_id'.
    - players (list, optional): List containing information about available players. Default is None.
    - is_active (bool, optional): Whether the players are active. Default is 'None' which returns all players.
    - return_fields (bool): If True, returns all available fields. Default is False.

    Returns:
    - bool or list: If return_fields is False, returns True if the field is within the available data, False otherwise.
                    If return_fields is True, returns a list of all available rounds or years.
    """
    if players is None:
        # Call get_draft_info function to retrieve players
        players = get_players()

    if players is None:
        return False  # Unable to retrieve player information
    
    # Determine the list of available players
    available_data = [info.get(key) for info in players]
    
    if key == 'name':
        sorted_data = sorted(available_data)  # Sort alphabetically
    else:
        # Convert to strings if not already, and then sort numerically
        available_data = [str(item) for item in available_data]
        sorted_data = sorted(available_data, key=lambda x: int(x))

    if return_fields:
        return sorted_data
    
    return str(player) in sorted_data

def validate_franchise_id(franchise_id, franchises=None, return_fields=False):
    """
    Validate the franchise id.

    Parameters:
    - franchise_id (str or int): The id to validate.
    - franchises (dict, optional): Dictionary containing information about available franchises. Default is None.
    - return_fields (bool): If True, returns all available franchise id's. Default is False.

    Returns:
    - bool or list: If return_fields is False, returns True if the franchise_id is within the available franchise IDs, False otherwise.
                    If return_fields is True, returns a list of all available franchise IDs.
    """
    if franchises is None:
        # Call get_franchises function to retrieve franchises
        franchises = get_franchises()

    if franchises is None:
        return False  # Unable to retrieve franchises
    
    # Check if the franchise_id is within the available franchise IDs
    available_franchises_id = [str(franchise.get("id")) for franchise in franchises.get("data", [])]
    
    if return_fields:
        return available_franchises_id
    
    return str(franchise_id) in available_franchises_id

def validate_countries(code, key="nationalityCode", return_fields=False, countries=None):
    """
    Validate the nationality code or birth state province code.

    Parameters:
    - code (str): The code to validate.
    - key (str): The key to validate against, either "nationalityCode" or "birthStateProvinceCode". Default is "nationalityCode".
    - return_fields (bool): If True, returns all available codes. Default is False.
    - countries (dict, optional): Dictionary containing information about available countries. Default is None.

    Returns:
    - bool or list: If return_fields is False, returns True if the code is within the available codes, False otherwise.
                    If return_fields is True, returns a list of all available codes.
    """
    if countries is None:
        # Call get_countries function to retrieve countries
        if key == "birthStateProvinceCode":
            countries = get_countries(include_stateProvinces=True)
        else:
            countries = get_countries()

    if countries is None:
        return False  # Unable to retrieve countries

    if key == "nationalityCode":
        # Check if the code is within the available nationality codes
        available_codes = [str(countries.get("id")) for countries in countries.get("data", [])]
    elif key == "birthStateProvinceCode":
        # Check if the code is within the available birth state province codes
        available_codes = []
        for country in countries.get("data", []):
            state_provinces = country.get("stateProvinces", [])
            for state_province in state_provinces:
                available_codes.append(str(state_province.get("id")))

    if return_fields:
        return available_codes

    return str(code) in available_codes

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

def validate_game_type(game_type):
    """
    Validate an integer input and ensure it is between 1 and 4.

    Parameters:
    - game_type (any): The input value to validate.

    Returns:
    - bool: True if the input is valid, False otherwise.
    """
    try:
        # Attempt to convert the input to an integer
        int_value = int(game_type)
        # Check if the integer is between 1 and 4.
        if (1 <= int_value <= 4):
            return True
    except ValueError:
        return False

def validate_position(position):
    """
    Validate input is 'C', 'L', 'R', or 'D'.

    Parameters:
    - position (str or list): The input value to validate.

    Returns:
    - bool: True if the input is valid, False otherwise.
    """
    try:
        # Check if the input is valid
        if isinstance(position, str):
            if position not in ["C", "L", "R", "D"]:
                return False
            else:
                return True
        elif isinstance(position, list):
            if not all(pos in ["C", "L", "R", "D"] for pos in position):
                return False
            else:
                return True
    except ValueError:
        return False
    
def validate_home_road(home_road):
    """
    Validate input is 'H', or 'R'.

    Parameters:
    - home_road (str): The input value to validate.

    Returns:
    - bool: True if the input is valid, False otherwise.
    """
    try:
        # Check if the input is valid
        if home_road.upper() not in ["H", "R"]:
            return False
        else:
            return True
    except ValueError:
        return False
    
def validate_shoots(shoots):
    """
    Validate input is 'L', or 'R'.

    Parameters:
    - shoots (str): The input value to validate.

    Returns:
    - bool: True if the input is valid, False otherwise.
    """
    try:
        # Check if the input is valid
        if shoots.upper() not in ["L", "R"]:
            return False
        else:
            return True
    except ValueError:
        return False
    
def validate_game_result(game_result):
    """
    Validate input is 'W', 'L', or 'O'.

    Parameters:
    - game_result (str): The input value to validate.

    Returns:
    - bool: True if the input is valid, False otherwise.
    """
    try:
        # Check if the input is valid
        if game_result.upper() not in ["W", "L", "O"]:
            return False
        else:
            return True
    except ValueError:
        return False

def validate_report(report=None, key=None, config_data=None, view=None, return_fields=False):
    """
    Validate if the provided report is within the available fields of the get_config response.
    Note: Must provide a report if return_fields is False.

    Parameters:
    - report (str or None): The report type to validate. Default is None.
    - key (str, optional): The type of report, which determines the view parameter for get_config. Default is None.
    - config_data (dict or None): The configuration data fetched from get_config. If None, fetches the configuration data.
    - view (str, optional): The part of the JSON to retrieve keys from. Default is None.
    - return_fields (bool): If True, returns the available fields instead of a boolean indicating whether the report is valid. Default is False.

    Returns:
    - bool or list: If return_fields is False (default), returns True if the report is valid, False otherwise.
                    If return_fields is True, returns the list of available fields.
    """
    # Define key mapping dictionary
    key_mapping = {
        "skaters": "playerReportData",
        "goalies": "goalieReportData",
        "teams": "teamReportData",
        "aggregated": "aggregatedColumns",
        "individual": "individualColumns",
    }

    # Determine the view parameter based on the key
    if key is not None:
        config_view = key_mapping.get(key)
    else:
        config_view = view

    # Fetch available fields from get_config response if config_data is not provided
    if config_data is None:
        config_data = get_config(config_view)

    # If config_data is not a dictionary, return False or available fields based on return_fields value
    if not isinstance(config_data, dict):
        return config_data if return_fields else False

    # Parse view parameter to get the keys
    if view:
        keys = view.split(".")
        for key in keys:
            config_data = config_data.get(key)
            if not isinstance(config_data, dict):
                return config_data if return_fields else False

    # Get available fields
    available_fields = list(config_data.keys())

    if return_fields:
        return available_fields
    else:
        # If report is None and return_fields is False, return False
        if report is None:
            return False
        # Check if the provided report is in the available fields
        return report in available_fields

#TODO fix list comparison issues (bypass by returning_fields and using compare_lists)
def validate_fields(field=None, report=None, key=None, is_game=None, config_data=None, config_display="displayItems", view=None, return_fields=True):
    """
    Validate if the provided field is within the available fields of the get_config response.
    Note: Must provide a field if return_fields is False.

    Parameters:
    - field (str, optional): The field to validate. Default is 'None'.
    - report (str, optional): The report type, which determines the view parameter for get_config. Default is 'None'.
    - key (str, optional): The key for the type of report, which determines the view parameter for get_config. Default is 'None'.
    - is_game (bool, optional): The flag for providing a range of dates. Default is 'None'.
    - config_data (dict, optional): The configuration data fetched from get_config. If 'None', fetches the configuration data.
    - config_display (str, optional): The subfields to display. Valid fields include 'displayItems', 'resultFilters', 'sortKeys'. Default is 'displayItems'.
    - view (str, optional): The part of the JSON to retrieve keys from. Default is 'None'.
    - return_fields (bool): If True, returns the available fields instead of a boolean indicating whether the field is valid. Default is 'True'. Note: issues with 'False' currently.

    Returns:
    - bool or list: If return_fields is False (default), returns True if the field is valid, False otherwise.
                    If return_fields is True, returns the list of available fields.
    """
    # Define key mapping dictionary
    key_mapping = {
        "skaters": "playerReportData",
        "goalies": "goalieReportData",
        "teams": "teamReportData",
        "aggregated": "aggregatedColumns",
        "individual": "individualColumns",
    }

    # Determine the view parameter based on the key and field
    if key is not None:
        config_view = key_mapping.get(key)
    elif report is not None:
        config_view = key_mapping.get(report)
    else:
        config_view = view

    if report is not None:
        # Append the field to the config_view with a "." delimiter
        if config_view:
            config_view += "." + report

        if is_game is not None:
            # Append the field to the config_view with a "." delimiter
            if config_view:
                if is_game:
                    config_view += "." + "game"
                else:
                    config_view += "." + "season"

                if config_display is not None:
                    config_view += "." + config_display

    # Fetch available fields from get_config response if config_data is not provided
    if config_data is None:
        config_data = get_config(config_view)

    # If config_data is not a dictionary, return False or available fields based on return_fields value
    if not isinstance(config_data, dict):
        return config_data if return_fields else False

    # Get available fields
    available_fields = list(config_data.keys())

    if return_fields:
        return available_fields
    else:
        # Check if all provided fields are in the available fields
        return True #compare_list(field=field, json_list=available_fields, return_boolean=True) #TODO fix list comparison issues
    
#TODO fix list comparison issues (bypass by returning_fields and using compare_lists)
def validate_player_seasons(season, player_id, return_fields=False):
    """
    Validate the season parameter for a specific player_id.

    Parameters:
    - player_id (int): The ID of the player.
    - season (str): The season to validate (e.g., '20202021').
    - return_fields (bool): If True, returns the list of unique NHL seasons for the player. If False, returns True if the season is valid for the player, False otherwise.

    Returns:
    - bool or list: If return_fields is False, returns True if the season is valid for the player, False otherwise.
                    If return_fields is True, returns a list of unique NHL seasons for the player.
    """
    # Fetch player landing data to get a list of all seasons for the player
    player_landing_data = get_player_landing(player_id, view="seasonTotals")
    if player_landing_data is None:
        # Unable to fetch player landing data, return False or an empty list depending on return_fields
        return [] if return_fields else False

    # Extract NHL seasons from player landing data and filter to unique values
    nhl_seasons = set(season_data.get("season") for season_data in player_landing_data if season_data.get("leagueAbbrev") == "NHL")

    # Check if return_fields is True
    if return_fields:
        return list(nhl_seasons)

    # Check if the provided season is within the list of NHL seasons for the player
    if season in nhl_seasons:
        return True

    return False

#TODO use get_club_stats_season to validate seasons for club_stats
