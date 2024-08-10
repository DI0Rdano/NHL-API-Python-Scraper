"""
Supporting functions for the NHL API Python Scraper [https://github.com/DI0Rdano/NHL-API-Python-Scraper/blob/main/nhlAPIscraper.py].
Documentation for scraper methods on github [https://github.com/DI0Rdano/NHL-API-Python-Scraper/blob/main/scraperDocumentation.md].
Follow @DI0Rdano on Twitter/X [https://x.com/DI0Rdano].
"""

import json
import time
import requests
from datetime import datetime
from typing import Union, Any

def make_api_request(url: str, timeout: int = 10, retries: int = 3, backoff: float = 0.1, validation: bool = False, return_json: bool = True) -> dict:
    """
    Make a request to the API and handle retries and error conditions.

    Parameters:
    - `url` (str): The URL to make the API request to.

    Additional Parameters:
    - `timeout` (int): The timeout duration for the request in seconds. Default is '10'.
    - `retries` (int): The number of retry attempts in case of failure. Default is '3'.
    - `backoff` (float): The delay before the next retry attempt in seconds. Default is '0.1'.
    - `validation` (bool): Flag to enable/disable input validation. Default is 'False'.
    - `return_json` (bool): Flag to determine whether to return JSON or raw text. Default is 'True'.

    Returns:
    - `json` (dict | None): The JSON response from the API or none in case of error.
    """
    session = requests.Session()

    if validation:
        if not isinstance(url, str):
            raise ValueError(f"Invalid url='{url}', parameter must be a string.")

        if not isinstance(timeout, int) or not timeout > 0:
            raise ValueError(f"Invalid timeout='{timeout}', parameter must be a positive integer.")

        if not isinstance(retries, int) or not retries > 0:
            raise ValueError(f"Invalid retries='{retries}', parameter must be a positive integer.")

    for attempt in range(retries):
        try:
            response = session.get(url, timeout=timeout)
            response.raise_for_status()
            
            if not response.content:
                return None
                
            if return_json:
                return response.json()
            else:
                return response.text
        
        except requests.exceptions.RequestException as e:
            if attempt < retries - 1:
                delay = (2 ** attempt) * backoff 
                time.sleep(delay) 
            else:
                return None
            
    return None

def filter_view(data: dict, view: str, validation: bool = False) -> dict:
    """
    Filter the JSON data based on the specified view.

    Parameters:
    - `data` (dict): JSON data to filter.
    - `view` (str): The part of the JSON to return, use '.' as a delimiter for subfields.

    Additional Parameters:
    - `validation` (bool | None): Flag to enable/disable input validation. Default is 'False'.

    Returns:
    - `json` (dict): Filtered data based on the specified view.
    """

    if not view:
        return data

    for field in view.split("."): # Split the view string by "." to handle nested fields
        if validation and field not in data: 
            raise ValueError(f"Invalid view='{view}'. Field '{field}' not found. Valid fields at this level include: {', '.join(data.keys())}.")
        elif not validation and field not in data:
            return None
        data = data[field]
    return data

def get_nested_value(data: dict, key: str) -> Any:
    """
    Get a value from a nested dictionary using a dot-delimited key.

    Parameters:
    - `data` (dict): The dictionary to search.
    - `key` (str): The dot-delimited key string.

    Returns:
    - The value if found, else None.
    """
    keys = key.split(".")
    for k in keys:
        data = data.get(k, {})
    return data if data else None

def filter_json_data(data: dict, filters: dict, exclude: bool = False) -> dict:
    """
    Filter data based on the provided filters.

    Parameters:
    - `data` (dict): The JSON data to filter.
    - `filters` (dict): Dictionary containing filter parameters and their corresponding values.

    Additional Parameters
    - `exclude` (bool): Flag to indicate whether to exclude data based on the filters. Default is `False`.

    Returns:
    - `json` (dict): Filtered data based on the provided filters.
    """
    #TODO add validation and modify to work with multiple inclusions/exclusions {"param1": val1, "param2": val2}

    if not filters:
        return data

    filtered_data = [
        item for item in data
        if exclude ^ all(
            (get_nested_value(item, key) == value if value is not None else get_nested_value(item, key) is None) or
            (isinstance(value, list) and get_nested_value(item, key) in value)
            for key, value in filters.items()
        )
    ]

    return filtered_data

def construct_sorting_params(sort: Union[str, list], direction: Union[str, list], validation: bool = False) -> str:
    """
    Construct sorting parameters for the API URL.

    Parameters:
    - `sort` (str | list): Field(s) to sort by.
    - `direction` (str | list): Sort direction(s) ('ASC' or 'DESC').
    - `validation` (bool): Flag to enable/disable input validation for sort and direction. Default is True.

    Returns:
    - `str`: Sorting parameters as an f-string.
    """
    if validation:
        if not isinstance(sort, (str, list)):
            raise ValueError("Invalid input type for sort parameter. Must be a string or a list of strings.")
        if not isinstance(direction, (str, list)):
            raise ValueError("Invalid input type for direction parameter. Must be a string or a list of strings.")

    sort = sort if isinstance(sort, list) else [sort]
    direction = direction if isinstance(direction, list) else [direction]

    valid_directions = {'ASC', 'DESC'}
    for dir in direction:
        if validation and dir not in valid_directions:
            raise ValueError(f"Invalid sort direction: {dir}. Must be 'ASC' or 'DESC'.")
    #TODO update sorting validation

    sort_params = [{"property": field, "direction": dir} for field, dir in zip(sort, direction)]
    sort_json = json.dumps(sort_params)

    return f"sort={sort_json}"

def construct_cayenne_exp(start_season: str = None, end_season: str = None, start_date: str = None, end_date: str = None, season: str = None, default_kwargs: dict = None) -> str:
    """
    Construct the cayenneExp for the get_stats function.

    Parameters:
    - `start_season` (str): Starting season.
    - `end_season` (str): Ending season.
    - `start_date` (str): Starting date (YYYY-MM-DD).
    - `end_date` (str): Ending date (YYYY-MM-DD).
    - `season` (str): Specific season.
    - `default_kwargs` (dict): Additional keyword arguments for constructing cayenneExp.

    Returns:
    - `str`: The constructed cayenneExp string.
    """  
    
    cayenne_exp_parts = []
    if start_season is not None and end_season is not None:
        cayenne_exp_parts.append(f"seasonId<={end_season} and seasonId>={start_season}")
    elif start_date is not None and end_date is not None:
        formatted_start_date = format_date(start_date)
        formatted_end_date = format_date(end_date)
        cayenne_exp_parts.append(f"gameDate<='{formatted_end_date}' and gameDate>='{formatted_start_date}'")
    elif season is not None:
        cayenne_exp_parts.append(f"seasonId={season}")

    if default_kwargs:
        for key, value in default_kwargs.items():
            if value is not None:
                if key == "game_type":
                    cayenne_exp_parts.append(f"gameTypeId={value}")
                elif key == "franchise_id":
                    cayenne_exp_parts.append(f"franchiseId={int(value)}")
                elif key == "opponent_franchise_id":
                    cayenne_exp_parts.append(f"opponentFranchiseId={int(value)}")
                elif key == "home_or_road":
                    cayenne_exp_parts.append(f"homeRoad='{value}'")
                elif key == "game_result":
                    cayenne_exp_parts.append(f"decision='{value}'")
                elif key == "position":
                    if isinstance(value, str):
                        cayenne_exp_parts.append(f"positionCode='{value}'")
                    elif isinstance(value, list):
                        position_exp = " or ".join([f"positionCode='{pos}'" for pos in value])
                        cayenne_exp_parts.append(f"({position_exp})")
                elif key == "player_name":
                    cayenne_exp_parts.append(f"skaterFullName likeIgnoreCase '%{value}%'")
                elif key == "is_rookie":
                    cayenne_exp_parts.append(f"isRookie={'1' if value else '0'}")
                elif key == "is_active":
                    cayenne_exp_parts.append(f"active={'1' if value else '0'}")
                elif key == "is_in_hall_of_fame":
                    cayenne_exp_parts.append(f"isInHallOfFame={'1' if value else '0'}")
                elif key == "birth_state_province_code":
                    cayenne_exp_parts.append(f"birthStateProvinceCode='{value}'")
                elif key == "nationality_code":
                    cayenne_exp_parts.append(f"nationalityCode='{value}'")
                elif key == "shoots_catches":
                    cayenne_exp_parts.append(f"shootsCatches='{value}'")
                elif key == "draft_round":
                    cayenne_exp_parts.append(f"draftRound={value}")
                elif key == "draft_year":
                    cayenne_exp_parts.append(f"draftYear='{value}'")

    return " and ".join(cayenne_exp_parts)

def construct_fact_cayenne_exp(min_gp: int, max_gp: int, default_kwargs: dict) -> str:
    """
    Construct the factCayenneExp based on provided parameters.

    Parameters:
    - `min_gp` (int): The minimum number of games played.
    - `max_gp` (int): The maximum number of games played.
    - `default_kwargs` (dict): Keyword arguments containing property, comparator, and value.

    Returns:
    - `str`: The constructed factCayenneExp.
    """
    fact_cayenne_exp = f"gamesPlayed>={min_gp}"

    if max_gp is not None:
        fact_cayenne_exp += f" and gamesPlayed<={max_gp}"

    if default_kwargs.get("property") is not None:
        property = default_kwargs.get("property")
        comparator = default_kwargs.get("comparator")
        value = default_kwargs.get("value")

        property = property if isinstance(property, list) else [property]
        comparator = comparator if isinstance(comparator, list) else [comparator]
        value = value if isinstance(value, list) else [value]

        for prop, comp, val in zip(property, comparator, value):
            fact_cayenne_exp += f" and {prop}{comp}{val}"

    return fact_cayenne_exp

def convert_time_to_seconds(time_str: str) -> int:
    """Convert a time string in the format MM:SS to an integer count of seconds."""
    minutes, seconds = map(int, time_str.split(':'))
    return minutes * 60 + seconds

def format_date(date_string: str) -> str:
    try:
        parsed_date = datetime.strptime(date_string, "%Y-%m-%d")
        formatted_date = parsed_date.strftime("%Y-%m-%d") # Format the date as "YYYY-MM-DD"
        return formatted_date
    except ValueError:
        raise ValueError("Error: Invalid date format")

def format_month(date_string: str) -> str:
    try:
        parsed_date = datetime.strptime(date_string, "%Y-%m-%d")
        formatted_date = parsed_date.strftime("%Y-%m") # Format the date as "YYYY-MM"
        return formatted_date
    except ValueError:
        raise ValueError("Error: Invalid date format")
