"""
Python wrapper functions for the various NHL API endpoints. Not intended to be comprehensive, created for personal use. 
Documentation for methods on github [https://github.com/DI0Rdano/NHL-API-Python-Scraper/blob/main/scraperDocumentation.md].
Follow @DI0Rdano on Twitter/X [https://x.com/DI0Rdano].
"""

from dataclasses import dataclass
from typing import Union, Any
from generalFunctions import make_api_request, construct_sorting_params, construct_cayenne_exp, construct_fact_cayenne_exp, filter_view, filter_json_data, format_date, format_month, get_nested_value, convert_time_to_seconds

@dataclass
class nhlAPI:
    base_urls = {
        "config": "https://api.nhle.com/stats/rest/en/config",
        "country": "https://api.nhle.com/stats/rest/en/country?",
        "franchise": "https://api.nhle.com/stats/rest/en/franchise?",
        "season": "https://api.nhle.com/stats/rest/en/season?",
        "draft": "https://api.nhle.com/stats/rest/en/draft?",
        "search_player": "https://search.d3.nhle.com/api/v1/search/player?culture=en-us",
        "player": "https://api-web.nhle.com/v1/player/",
        "players": "https://api.nhle.com/stats/rest/en/players",
        "roster": "https://api-web.nhle.com/v1/roster/", 
        "roster_season": "https://api-web.nhle.com/v1/roster-season/",
        "stats": "https://api.nhle.com/stats/rest/en/",
        "schedule_calendar": "https://api-web.nhle.com/v1/schedule-calendar/",
        "schedule": "https://api-web.nhle.com/v1/schedule/",
        "standings": "https://api-web.nhle.com/v1/standings/",
        "standings_season": "https://api-web.nhle.com/v1/standings-season",
        "score": "https://api-web.nhle.com/v1/score/",
        "gamecenter": "https://api-web.nhle.com/v1/gamecenter/",
        "shiftcharts": "https://api.nhle.com/stats/rest/en/shiftcharts",
        "reports": "https://www.nhl.com/scores/htmlreports/",
        "club_stats_season": "https://api-web.nhle.com/v1/club-stats-season/",
        "club_schedule": "https://api-web.nhle.com/v1/club-schedule/",
        "record": "https://records.nhl.com/site/api", 
        "record_category": "https://records.nhl.com/site/api/record-category",
        "record_component_season": "https://records.nhl.com/site/api/component-season",
        "record_menu": "https://records.nhl.com/site/api/nhl/menu?cayenneExp=parent=null&include=children&include=children.children",
        "playoffs_carousel": "https://api-web.nhle.com/v1/playoff-series/carousel/" #TODO playoffs_carousel  
    }
    default_params = {
        "season": None,
        "start_season": None,
        "end_season": None,
        "start_date": None,
        "end_date": None,
        "aggregate": True,
        "franchise_id": None,
        "opponent_franchise_id": None,
        "home_or_road": None,
        "game_result": None,
        "game_type": 2, 
        "min_gp": 0,
        "max_gp": None,
        "property": None,
        "comparator": None,
        "value": None,
        "sort": None,
        "direction": None,
        "start": 0,
        "player_limit": None,
        "active_players": 2500, #approx
        "inactive_players": 22000, #approx
        "total_players": 25000, #approx
        "is_active": None,
        "include_state_provinces": True,
        "include_first_season": True,
        "include_last_season": True,
        "view": None,
        "filter_fields": None,
        "filter_data": None,
        "filter_range": None,
        "exclude_data": None,
        "exclude_range": None,
        "return_all": True,
        "return_info": False,
        "validation": False,
        "timeout": 10,
        "retries": 3,
        "backoff": 0.3
    }
    report_params = {
        "skater": {
            "position": None,
            "shoots_catches": None,
            "player_name": None,
            "nationality_code": None,
            "birth_state_province_code": None,
            "draft_round": None,
            "draft_year": None,
            "is_rookie": None,
            "is_active": None,
            "is_in_hall_of_fame": None,
            "limit": 100,
        },
        "goalie": {
            "shoots_catches": None,
            "player_name": None,
            "nationality_code": None,
            "birth_state_province_code": None,
            "draft_round": None,
            "draft_year": None,
            "is_rookie": None,
            "is_active": None,
            "is_in_hall_of_fame": None,
            "limit": 100,
        },
        "team": {
            "limit": 50,
        }
    }

    @staticmethod
    def get_config(**kwargs: Any) -> dict:
        """
        Fetch data from the NHL API 'config' endpoint.

        Optional Parameters:
        - `view` (str | None): To drilldown the JSON dictionary, use '.' as a delimiter for subfields. Default is 'None' which returns everything.

        Additional Parameters:
        - `return_info` (bool): Flag to return additional information along with the response. Default is 'False'.
        - `validation` (bool): Flag to enable/disable input validation. Default is 'False'. Note: partially implemented.
        - `timeout` (int): The timeout duration for the request in seconds. Default is '10'.
        - `retries` (int): The number of retry attempts in case of failure. Default is '3'.
        - `backoff` (float): The delay before the next retry attempt in seconds. Default is '0.3'.

        Returns:
        - `json` (dict | None): Configuration data with relevant fields for the stats endpoint.
        """
        params = nhlAPI.default_params
        params.update(kwargs)

        input_params = ["view", "validation", "return_info", "timeout", "retries", "backoff"]
        view, validation, return_info, timeout, retries, backoff = (params.get(param) for param in input_params)

        url = nhlAPI.base_urls.get("config")
        data = make_api_request(url, timeout, retries, backoff, validation)

        if data is None:
            return None

        filtered_data = filter_view(data, view, validation) if view is not None else data

        return {"path": url, "view": view, "response": filtered_data} if return_info else filtered_data

    @staticmethod
    def get_countries(include_state_provinces: bool = True, **kwargs: Any) -> dict:
        """
        Fetch JSON data from the NHL API 'country' endpoint.

        Parameters:
        - `include_state_provinces` (bool | None): Whether to include state provinces in the response. Default is 'True'.
        
        Optional Parameters:
        - `sort` (str | list[str] | None): Field to sort the countries by. Default is 'None'.
        - `direction` (str | list[str] | None): Sort direction ('ASC' for ascending, 'DESC' for descending). Default is 'None'.
        - `filter_fields` (str | list[str] | None): The fields to include in the json response. Default is 'None' which returns all fields.
        - `filter_data` (dict | None): Dictionary containing filter parameters and their corresponding values. Default is 'None' which returns everything.
        - `exclude_data` (dict | None): Dictionary containing filter parameters and their corresponding values to exclude from the response. Default is 'None' which excludes nothing.
        - `view` (str | None): To drilldown the JSON dictionary, use '.' as a delimiter for subfields. Default is 'None' which returns everything.

        Additional Parameters:
        - `return_info` (bool): Flag to return additional information along with the response. Default is 'False'.
        - `validation` (bool): Flag to enable/disable input validation. Default is 'False'. Note: partially implemented.
        - `timeout` (int): The timeout duration for the request in seconds. Default is '10'.
        - `retries` (int): The number of retry attempts in case of failure. Default is '3'.
        - `backoff` (float): The delay before the next retry attempt in seconds. Default is '0.3'.

        Returns:
        - `json` (dict | None): Country data.
        """

        params = nhlAPI.default_params
        params.update(kwargs)

        input_params = ["sort", "direction", "filter_fields", "filter_data", "exclude_data", "view", "validation", "return_info", "timeout", "retries", "backoff"]
        sort, direction, filter_fields, filter_data, exclude_data, view, validation, return_info, timeout, retries, backoff = (params.get(param) for param in input_params)

        url = nhlAPI.base_urls.get("country")
        url += construct_sorting_params(sort, direction, validation) if sort is not None else ""
        url += "&" if sort is not None and include_state_provinces else ""
        url += "include=stateProvinces" if include_state_provinces else ""

        if filter_fields:
            url += "&" if sort is not None or include_state_provinces else ""
            url += f"include={filter_fields}" if isinstance(filter_fields, str) else ""
            url += "&".join([f"include={field}" for field in filter_fields]) if isinstance(filter_fields, list) else ""

        data = make_api_request(url, timeout, retries, backoff, validation)

        if data is None:
            return None
            
        filtered_data = filter_json_data(data.get("data", []), filter_data) if filter_data is not None else data.get("data", [])
        filtered_data = {"data": filter_json_data(filtered_data, exclude_data, exclude=True)} if exclude_data is not None else {"data": filtered_data}
        filtered_data = filter_view(filtered_data, view, validation) if view is not None else {**filtered_data, "total": len(filtered_data["data"])}
        sort, direction = ([sort], [direction]) if isinstance(sort, str) else (sort, direction)

        return {"path": url, "view": view, "fields": filter_fields, "filters": filter_data, "exclude": exclude_data, "sort": {s: d for s, d in zip(sort, direction)} if sort is not None else None, "response": filtered_data} if return_info else filtered_data

    @staticmethod
    def get_franchises(include_first_season: bool = True, include_last_season: bool = True, **kwargs: Any) -> dict:
        """
        Fetch JSON data from the NHL API 'franchise' endpoint.

        Parameters:
        - `include_first_season` (bool | None): Whether to include first season information. Default is 'True'.
        - `include_last_season` (bool | None): Whether to include last season information. Default is 'True'.

        Optional Parameters:
        - `sort` (str | list[str] | None): Field to sort the franchises by. Default is 'None'.
        - `direction` (str | list[str] | None): Sort direction. Default is 'None'.
        - `filter_fields` (str | list[str] | None): The fields to include in the json response. Default is 'None' which returns all fields.
        - `filter_data` (dict | None): Dictionary containing filter parameters and their corresponding values. Default is 'None' which returns everything.
        - `exclude_data` (dict | None): Dictionary containing filter parameters and their corresponding values to exclude from the response. Default is 'None' which excludes nothing.
        - `view` (str | None): To drilldown the JSON dictionary, use '.' as a delimiter for subfields. Default is 'None' which returns everything.

        Additional Parameters:
        - `return_info` (bool): Flag to return additional information along with the response. Default is 'False'.
        - `validation` (bool): Flag to enable/disable input validation. Default is 'False'. Note: partially implemented.
        - `timeout` (int): The timeout duration for the request in seconds. Default is '10'.
        - `retries` (int): The number of retry attempts in case of failure. Default is '3'.
        - `backoff` (float): The delay before the next retry attempt in seconds. Default is '0.3'.

        Returns:
        - `json` (dict | None): Franchise data.
        """

        params = nhlAPI.default_params
        params.update(kwargs)

        input_params = ["sort", "direction", "filter_fields", "filter_data", "exclude_data", "view", "validation", "return_info", "timeout", "retries", "backoff"]
        sort, direction, filter_fields, filter_data, exclude_data, view, validation, return_info, timeout, retries, backoff = (params.get(param) for param in input_params)

        url = nhlAPI.base_urls.get("franchise")
        url += construct_sorting_params(sort, direction, validation) if sort is not None else ""

        if include_first_season:
            url += "&" if sort is not None else ""
            url += "include=firstSeason"
        if include_last_season:
            url += "&" if sort is not None or include_first_season is not None else ""
            url += "include=lastSeason"

        if filter_fields:
            url += "&" if sort is not None or include_first_season or include_last_season else ""
            url += f"include={filter_fields}" if isinstance(filter_fields, str) else ""
            url += "&".join([f"include={field}" for field in filter_fields]) if isinstance(filter_fields, list) else ""

        data = make_api_request(url, timeout, retries, backoff, validation)
        if data is None:
            return None
        
        filtered_data = filter_json_data(data.get("data", []), filter_data) if filter_data is not None else data.get("data", [])
        filtered_data = {"data": filter_json_data(filtered_data, exclude_data, exclude=True)} if exclude_data is not None else {"data": filtered_data}
        filtered_data = filter_view(filtered_data, view, validation) if view is not None else {**filtered_data, "total": len(filtered_data["data"])}
        sort, direction = ([sort], [direction]) if isinstance(sort, str) else (sort, direction)

        return {"path": url, "view": view, "fields": filter_fields, "filters": filter_data, "exclude": exclude_data, "sort": {s: d for s, d in zip(sort, direction)} if sort is not None else None, "response": filtered_data} if return_info else filtered_data

    @staticmethod
    def get_seasons(**kwargs: Any) -> dict:
        """
        Fetch data from the NHL API 'season' endpoint.

        Optional Parameters:
        - `sort` (str | list[str] | None): Field to sort the seasons by. Default is 'None'.
        - `direction` (str | list[str] | None): Direction of sorting. Default is 'None'.
        - `filter_fields` (str | list[str] | None): The fields to include. Default is 'None' which returns all fields.
        - `filter_data` (dict | None): Dictionary containing filter parameters and their corresponding values. Default is 'None' which returns everything.
        - `exclude_data` (dict | None): Dictionary containing filter parameters and their corresponding values to exclude from the response. Default is 'None' which excludes nothing.
        - `view` (str | None): To drilldown the JSON dictionary, use '.' as a delimiter for subfields. Default is 'None' which returns everything.

        Additional Parameters:
        - `return_info` (bool): Flag to return additional information along with the response. Default is 'False'.
        - `validation` (bool): Flag to enable/disable input validation. Default is 'False'. Note: partially implemented.
        - `timeout` (int): The timeout duration for the request in seconds. Default is '10'.
        - `retries` (int): The number of retry attempts in case of failure. Default is '3'.
        - `backoff` (float): The delay before the next retry attempt in seconds. Default is '0.3'.

        Returns:
        - `json` (dict | None): Available seasons data.
        """

        params = nhlAPI.default_params
        params.update(kwargs)

        input_params = ["sort", "direction", "filter_fields", "filter_data", "exclude_data", "view", "validation", "return_info", "timeout", "retries", "backoff"]
        sort, direction, filter_fields, filter_data, exclude_data, view, validation, return_info, timeout, retries, backoff = (params.get(param) for param in input_params)

        url = nhlAPI.base_urls.get("season")
        url += construct_sorting_params(sort, direction, validation) if sort is not None else ""

        if filter_fields:
            url += "&" if sort is not None else ""
            url += f"include={filter_fields}" if isinstance(filter_fields, str) else ""
            url += "&".join([f"include={field}" for field in filter_fields]) if isinstance(filter_fields, list) else ""

        data = make_api_request(url, timeout, retries, backoff, validation)

        if data is None:
            return None
            
        filtered_data = filter_json_data(data.get("data", []), filter_data) if filter_data is not None else data.get("data", [])
        filtered_data = {"data": filter_json_data(filtered_data, exclude_data, exclude=True)} if exclude_data is not None else {"data": filtered_data}
        filtered_data = filter_view(filtered_data, view, validation) if view is not None else {**filtered_data, "total": len(filtered_data["data"])}
        sort, direction = ([sort], [direction]) if isinstance(sort, str) else (sort, direction)

        return {"path": url, "view": view, "fields": filter_fields, "filters": filter_data, "exclude": exclude_data, "sort": {s: d for s, d in zip(sort, direction)} if sort is not None else None, "response": filtered_data} if return_info else filtered_data

    @staticmethod
    def get_draftrounds(**kwargs: Any) -> dict:
        """
        Fetch data from the NHL API 'draft' endpoint.

        Optional Parameters:
        - `sort` (str | list[str] | None): Field to sort the draft rounds by. Default is `None`.
        - `direction` (str | list[str] | None): Direction of sorting. Default is `None`.
        - `filter_fields` (str | list[str] | None): The fields to include. Default is `None` which returns all fields.
        - `filter_data` (dict | None): Dictionary containing filter parameters and their corresponding values. Default is `None` which returns everything.
        - `exclude_data` (dict | None): Dictionary containing filter parameters and their corresponding values to exclude from the response. Default is 'None' which excludes nothing.
        - `view` (str | None): To drilldown the JSON dictionary, use `.` as a delimiter for subfields. Default is `None` which returns everything.

        Additional Paramters:
        - `return_info` (bool): Flag to return additional information along with the response. Default is `False`.
        - `validation` (bool): Flag to enable/disable input validation. Default is `False`. Note: partially implemented.
        - `timeout` (int): The timeout duration for the request in seconds. Default is '10'.
        - `retries` (int): The number of retry attempts in case of failure. Default is '3'.
        - `backoff` (float): The delay before the next retry attempt in seconds. Default is '0.3'.

        Returns:
        - `json` (dict | None): Draft round data.
        """
        
        params = nhlAPI.default_params
        params.update(kwargs)

        input_params = ["sort", "direction", "filter_fields", "filter_data", "exclude_data", "view", "validation", "return_info", "timeout", "retries", "backoff"]
        sort, direction, filter_fields, filter_data, exclude_data, view, validation, return_info, timeout, retries, backoff = (params.get(param) for param in input_params)

        url = nhlAPI.base_urls.get("draft")
        url += construct_sorting_params(sort, direction, validation) if sort is not None else ""

        if filter_fields:
            url += "&" if sort is not None else ""
            url += f"include={filter_fields}" if isinstance(filter_fields, str) else ""
            url += "&".join([f"include={field}" for field in filter_fields]) if isinstance(filter_fields, list) else ""

        data = make_api_request(url, timeout, retries, backoff, validation)

        if data is None:
            return None
            
        filtered_data = filter_json_data(data.get("data", []), filter_data) if filter_data is not None else data.get("data", [])
        filtered_data = {"data": filter_json_data(filtered_data, exclude_data, exclude=True)} if exclude_data is not None else {"data": filtered_data}
        filtered_data = filter_view(filtered_data, view, validation) if view is not None else {**filtered_data, "total": len(filtered_data["data"])}
        sort, direction = ([sort], [direction]) if isinstance(sort, str) else (sort, direction)

        return {"path": url, "view": view, "fields": filter_fields, "filters": filter_data, "exclude": exclude_data, "sort": {s: d for s, d in zip(sort, direction)} if sort is not None else None, "response": filtered_data} if return_info else filtered_data

    @staticmethod
    def get_players(**kwargs: Any) -> dict:
        """
        Fetch data from the NHL API 'players' endpoint.

        Optional Parameters:
        - `is_active` (bool | None): Whether the players are active (True to return active players, False to return incactive players). Default is 'None' which returns all players.
        - `player_limit` (int | None): The max number of players to return.  Default is 'None'. There are approximately '2184' active players, and '19986' inactive players.
        - `sort` (str | list[str] | None): Field to sort the players by. Default is `None`.
        - `direction` (str | list[str] | None): Direction of sorting. Default is `None`.
        - `filter_fields` (str | list[str] | None): The fields to include. Default is `None` which returns all fields.
        - `filter_data` (dict | None): Dictionary containing filter parameters and their corresponding values. Default is 'None' which returns everything.
        - `exclude_data` (dict | None): Dictionary containing filter parameters and their corresponding values to exclude from the response. Default is 'None' which excludes nothing.
        - `view` (str | None): To drilldown the JSON dictionary, use '.' as a delimiter for subfields. Default is 'None' which returns everything.

        Additional Parameters:
        - `return_info` (bool): Flag to return additional information along with the response. Default is 'False'.
        - `validation` (bool): Flag to enable/disable input validation. Default is 'False'. Note: partially implemented.
        - `timeout` (int): The timeout duration for the request in seconds. Default is '10'.
        - `retries` (int): The number of retry attempts in case of failure. Default is '3'.
        - `backoff` (float): The delay before the next retry attempt in seconds. Default is '0.3'.
    
        Returns:
        - `json` (dict | None): Players bio data.
        """

        params = nhlAPI.default_params
        params.update(kwargs)

        input_params = ["player_limit", "is_active", "sort", "direction", "filter_fields", "filter_data", "exclude_data", "view", "validation", "return_info", "timeout", "retries", "backoff"]
        player_limit, is_active, sort, direction, filter_fields, filter_data, exclude_data, view, validation, return_info, timeout, retries, backoff = (params.get(param) for param in input_params)
        active_players, inactive_players, total_players = (params.get(param) for param in ("active_players", "inactive_players", "total_players"))

        limit = player_limit if player_limit is not None else (active_players if is_active else (total_players if is_active is None else inactive_players))

        base_url = nhlAPI.base_urls.get("search_player")
        url = f"{base_url}&limit={limit}&q=%2A"
        url += f"&active={is_active}" if is_active is not None else ""
        data = make_api_request(url, timeout, retries, backoff, validation)

        if data is None:
            return None

        if sort:
            sort, direction = ([sort], [direction]) if isinstance(sort, str) else (sort, direction)
            for s, d in reversed(list(zip(sort, direction))):
                reverse = d.upper() == 'DESC'
                data.sort(key=lambda x: (x.get(s) is None, x.get(s)), reverse=reverse)

        filtered_data = filter_json_data(data, filter_data) if filter_data is not None else data
        filtered_data = {"data": filter_json_data(filtered_data, exclude_data, exclude=True)} if exclude_data is not None else {"data": filtered_data}
        
        if filter_fields:
            filter_fields = [filter_fields] if isinstance(filter_fields, str) else filter_fields
            filtered_data["data"] = [{key: player[key] for key in filter_fields if key in player} for player in filtered_data["data"]]

        filtered_data = filter_view(filtered_data, view, validation) if view is not None else {**filtered_data, "total": len(filtered_data["data"])}

        return {"path": url, "view": view, "fields": filter_fields, "filters": filter_data, "exclude": exclude_data, "sort": {s: d for s, d in zip(sort, direction)} if sort is not None else None, "response": filtered_data} if return_info else filtered_data

    @staticmethod
    def get_roster(team_code: str = "TOR", season: str = "20232024", **kwargs: Any) -> dict:
        """
        Fetch data from the NHL API 'team roster' endpoint.

        Parameters:
        - `team_code` (str): The abbreviated code of the team, (ex. 'TOR').
        - `season` (str): The season in the format of '20232024'.

        Optional Parameters:
        - `sort` (str | list[str] | None): Field to sort the players by. Default is `None`.
        - `direction` (str | list[str] | None): Direction of sorting. Default is `None`.
        - `filter_fields` (str | list[str] | None): The fields to include. Default is `None` which returns all fields.
        - `filter_data` (dict | None): Dictionary containing filter parameters and their corresponding values. Default is 'None' which returns everything.
        - `exclude_data` (dict | None): Dictionary containing filter parameters and their corresponding values to exclude from the response. Default is 'None' which excludes nothing.
        - `view` (str | None): To drilldown the JSON dictionary, use '.' as a delimiter for subfields. Default is 'None' which returns everything.

        Additional Parameters:
        - `return_info` (bool): Flag to return additional information along with the response. Default is 'False'.
        - `validation` (bool): Flag to enable/disable input validation. Default is 'False'. Note: partially implemented.
        - `timeout` (int): The timeout duration for the request in seconds. Default is '10'.
        - `retries` (int): The number of retry attempts in case of failure. Default is '3'.
        - `backoff` (float): The delay before the next retry attempt in seconds. Default is '0.3'.
        
        Returns:
        - `json` (dict | None): Team roster data for a specific season.
        """

        params = nhlAPI.default_params
        params.update(kwargs)

        input_params = ["sort", "direction", "filter_fields", "filter_data", "exclude_data", "view", "validation", "return_info", "timeout", "retries", "backoff"]
        sort, direction, filter_fields, filter_data, exclude_data, view, validation, return_info, timeout, retries, backoff = (params.get(param) for param in input_params)

        base_url = nhlAPI.base_urls.get("roster")
        url = f"{base_url}{team_code}/{season}"
        data = {"data": make_api_request(url, timeout, retries, backoff, validation)}

        if sort:
            sort, direction = ([sort], [direction]) if isinstance(sort, str) else (sort, direction)
            for s, d in reversed(list(zip(sort, direction))):
                reverse = d.upper() == 'DESC'
                for pos_group in data["data"]:
                    data["data"][pos_group].sort(key=lambda x: (x.get(s) is None, x.get(s)), reverse=reverse)

        total = 0
        for pos_group in data["data"]:
            position_group_data = data["data"][pos_group]
            if filter_data is not None:
                position_group_data = filter_json_data(position_group_data, filter_data)
            if exclude_data is not None:
                position_group_data = filter_json_data(position_group_data, exclude_data, exclude=True)
            data["data"][pos_group] = position_group_data
            total += len(position_group_data)

        if filter_fields:
            for pos_group in data["data"]:
                filter_fields = [filter_fields] if isinstance(filter_fields, str) else filter_fields
                data["data"][pos_group] = [{key: player[key] for key in filter_fields if key in player} for player in data["data"][pos_group]]

        data["data"]["total"] = total
        filtered_data = filter_view(data, view, validation) if view is not None else data

        return {"path": url, "view": view, "fields": filter_fields, "filters": filter_data, "exclude": exclude_data, "sort": {s: d for s, d in zip(sort, direction)} if sort is not None else None, "response": filtered_data} if return_info else filtered_data

    @staticmethod
    def get_roster_seasons(team_code: str = "MTL", **kwargs: Any) -> dict:
        """
        Fetch data from the NHL API 'roster-season' endpoint.

        Parameters:
        - `team_code` (str): The abbreviated code of the team, (ex. 'TOR'). Default is 'MTL'.

        Optional Parameters:
        - `sort` (bool | None): Boolean flag to enable sorting. Default is 'None'.
        - `direction` (str | list[str] | None): Direction of sorting. Default is 'None'.
        - `view` (str | None): To drilldown the JSON dictionary, use '.' as a delimiter for subfields. Default is 'None' which returns everything.
        - `filter_data` (str | int | list [str, int] | None): Seasons to include in the response. Default is 'None' which returns everything.
        - `exclude_data` (str | int | list [str, int] | None): Seasons to exclude from the response. Default is 'None' which excludes nothing.

        Additional Parameters:
        - `return_info` (bool): Flag to return additional information along with the response. Default is 'False'.
        - `validation` (bool): Flag to enable/disable input validation. Default is 'False'. Note: partially implemented.
        - `timeout` (int): The timeout duration for the request in seconds. Default is '10'.
        - `retries` (int): The number of retry attempts in case of failure. Default is '3'.
        - `backoff` (float): The delay before the next retry attempt in seconds. Default is '0.3'.

        Returns:
        - `json` (list | None): Team roster seasons data.
        """

        params = nhlAPI.default_params
        params.update(kwargs)

        input_params = ["sort", "direction", "view", "filter_data", "exclude_data", "validation", "return_info", "timeout", "retries", "backoff"]
        sort, direction, view, filter_data, exclude_data, validation, return_info, timeout, retries, backoff = (params.get(param) for param in input_params)

        base_url = nhlAPI.base_urls.get("roster_season")
        url = f"{base_url}{team_code}"
        data = {"data": make_api_request(url, timeout, retries, backoff, validation)}

        if exclude_data is not None: #TODO make it handle range like 20182025
            if not isinstance(exclude_data, list):
                exclude_data = [exclude_data]
            exclude_data = [int(exclude) for exclude in exclude_data]
            data["data"] = [season for season in data["data"] if season not in exclude_data]

        if filter_data is not None: #TODO make it handle range like 20182025
            if not isinstance(filter_data, list):
                filter_data = [filter_data]
            filter_data = [int(season) for season in filter_data]
            data["data"] = [season for season in data["data"] if season in filter_data]

        if sort:
            direction = [direction] if isinstance(direction, str) else direction
            for d in reversed(list(direction)):
                reverse = d.upper() == 'DESC'
                data["data"].sort(key=lambda x: (x is None, x), reverse=reverse)

        filtered_data = filter_view(data, view, validation) if view is not None else {**data, "total": len(data["data"])}

        return {"path": url, "view": view, "filters": filter_data, "exclude": exclude_data, "sort": direction if sort else sort, "response": filtered_data} if return_info else filtered_data

    @staticmethod 
    def get_player_landing(player_id: Union[int, str], **kwargs: Any) -> dict:
        """
        Fetch data from the NHL API 'player/landing' endpoint.

        Parameters:
        - `player_id` (int | str): The ID of the player.

        Optional Parameters:
        - `sort` (str | list[str] | None): Field to sort the players by. Default is `None`. Note: only applies to 'seasonTotals'.
        - `direction` (str | list[str] | None): Direction of sorting. Default is `None`. Note: only applies to 'seasonTotals'.
        - `filter_fields` (str | list[str] | None): The fields to include. Default is `None` which returns all fields. Note: only applies to 'seasonTotals'.
        - `filter_data` (dict | None): Dictionary containing filter parameters and their corresponding values. Default is 'None' which returns everything. Note: only applies to 'seasonTotals'.
        - `exclude_data` (dict | None): Dictionary containing filter parameters and their corresponding values to exclude from the response. Default is 'None' which excludes nothing. Note: only applies to 'seasonTotals'.
        - `view` (str | None): To drilldown the JSON dictionary, use '.' as a delimiter for subfields. Default is 'None' which returns everything.

        Additional Parameters:
        - `return_info` (bool): Flag to return additional information along with the response. Default is 'False'.
        - `validation` (bool): Flag to enable/disable input validation. Default is 'False'. Note: partially implemented.
        - `timeout` (int): The timeout duration for the request in seconds. Default is '10'.
        - `retries` (int): The number of retry attempts in case of failure. Default is '3'.
        - `backoff` (float): The delay before the next retry attempt in seconds. Default is '0.3'.

        Returns:
        - `json` (dict | None): Player landing data.
        """

        params = nhlAPI.default_params
        params.update(kwargs)
        
        input_params = ["sort", "direction", "filter_fields", "filter_data", "exclude_data", "view", "validation", "return_info", "timeout", "retries", "backoff"]
        sort, direction, filter_fields, filter_data, exclude_data, view, validation, return_info, timeout, retries, backoff = (params.get(param) for param in input_params)

        player_id = int(player_id)
        base_url = nhlAPI.base_urls.get("player")
        url = f"{base_url}{player_id}/landing"
        data = {"data": make_api_request(url, timeout, retries, backoff, validation)}

        if data is None:
            return None
        
        if sort:
            sort, direction = ([sort], [direction]) if isinstance(sort, str) else (sort, direction)
            for s, d in reversed(list(zip(sort, direction))):
                reverse = d.upper() == 'DESC'
                data["data"]["seasonTotals"].sort(key=lambda x: (x.get(s) is None, x.get(s)), reverse=reverse)

        if filter_fields:
            filter_fields = [filter_fields] if isinstance(filter_fields, str) else filter_fields
            data["data"]["seasonTotals"] = [{key: player[key] for key in filter_fields if key in player} for player in data["data"]["seasonTotals"]]

        data["data"]["seasonTotals"] = filter_json_data(data["data"]["seasonTotals"], filter_data) if filter_data is not None else data["data"]["seasonTotals"]
        data["data"]["seasonTotals"] = filter_json_data(data["data"]["seasonTotals"], exclude_data, exclude=True) if exclude_data is not None else data["data"]["seasonTotals"]

        filtered_data = filter_view(data, view, validation) if view is not None else data

        return {"path": url, "view": view, "fields": filter_fields, "filters": filter_data, "exclude": exclude_data, "sort": {s: d for s, d in zip(sort, direction)} if sort is not None else None, "response": filtered_data} if return_info else filtered_data

    @staticmethod
    def get_player_gamelog(player_id: Union[int, str], season: Union[int, str] = "20232024", game_type: Union[int, str] = 2, **kwargs: Any) -> dict:
        """
        Fetch gamelog data for a specific player from the NHL API 'player/gamelog' endpoint.

        Parameters:
        - `player_id` (int | str): The ID of the player.
        - `season` (str | int): The season to return the gamelog from, (ex. '20232024').
        - `game_type` (int | str): The type of game (2 for regular season, 3 for playoffs). Default is '2'.

        Optional Parameters:
        - `sort` (str | list[str] | None): Field to sort the players by. Default is `None`.
        - `direction` (str | list[str] | None): Direction of sorting. Default is `None`.
        - `filter_fields` (str | list[str] | None): The fields to include. Default is `None` which returns all fields.
        - `filter_data` (dict | None): Dictionary containing filter parameters and their corresponding values. Default is 'None' which returns everything.
        - `exclude_data` (dict | None): Dictionary containing filter parameters and their corresponding values to exclude from the response. Default is 'None' which excludes nothing.
        - `view` (str | None): To drilldown the JSON dictionary, use '.' as a delimiter for subfields. Default is 'None' which returns everything.

        Additional Parameters:
        - `return_info` (bool): Flag to return additional information along with the response. Default is 'False'.
        - `validation` (bool): Flag to enable/disable input validation. Default is 'False'. Note: partially implemented.
        - `timeout` (int): The timeout duration for the request in seconds. Default is '10'.
        - `retries` (int): The number of retry attempts in case of failure. Default is '3'.
        - `backoff` (float): The delay before the next retry attempt in seconds. Default is '0.3'.

        Returns:
        - `json` (dict | None): Player gamelog data based on the specified view.
        """

        params = nhlAPI.default_params
        params.update(kwargs)
        
        input_params = ["sort", "direction", "filter_fields", "filter_data", "exclude_data", "view", "validation", "return_info", "timeout", "retries", "backoff"]
        sort, direction, filter_fields, filter_data, exclude_data, view, validation, return_info, timeout, retries, backoff = (params.get(param) for param in input_params)

        season = str(season)
        game_type = int(game_type)
        player_id = int(player_id)
        base_url = nhlAPI.base_urls.get("player")
        url = f"{base_url}{player_id}/game-log/{season}/{game_type}"
        data = {"data": make_api_request(url, timeout, retries, backoff, validation)}

        if data is None:
            return None

        if sort:
            sort, direction = ([sort], [direction]) if isinstance(sort, str) else (sort, direction)
            for s, d in reversed(list(zip(sort, direction))):
                reverse = d.upper() == 'DESC'
                data["data"]["gameLog"].sort(key=lambda x: (x.get(s) is None, x.get(s)), reverse=reverse)

        if filter_fields:
            filter_fields = [filter_fields] if isinstance(filter_fields, str) else filter_fields
            data["data"]["gameLog"] = [{key: player[key] for key in filter_fields if key in player} for player in data["data"]["gameLog"]]

        filtered_data = {"data": {"seasonId": data.get("data", []).get("seasonId"), "gameTypeId": data.get("data", []).get("gameTypeId"), "playerStatsSeasons": data.get("data", []).get("playerStatsSeasons", []), "gameLog": filter_json_data(data.get("data", []).get("gameLog", []), filter_data)}} if filter_data is not None else data
        filtered_data = {"data": {"seasonId": data.get("data", []).get("seasonId"), "gameTypeId": data.get("data", []).get("gameTypeId"), "playerStatsSeasons": data.get("data", []).get("playerStatsSeasons", []), "gameLog": filter_json_data(data.get("data", []).get("gameLog", []), exclude_data, exclude=True)}} if exclude_data is not None else filtered_data
        filtered_data = filter_view(filtered_data, view, validation) if view is not None else filtered_data

        return {"path": url, "view": view, "fields": filter_fields, "filters": filter_data, "exclude": exclude_data, "sort": {s: d for s, d in zip(sort, direction)} if sort is not None else None, "response": filtered_data} if return_info else filtered_data

    @staticmethod
    def get_schedule_calendar(date: str = "now", **kwargs: Any) -> dict:
        """
        Fetches schedule data for a specific date from the NHL API 'schedule-calendar' endpoint.

        Parameters:
        - `date` (str | None): The date for which to fetch the schedule calendar data (in 'YYYY-MM-DD' format). Default is 'now'.

        Optional Parameters:
        - `view` (str | None): To drilldown the JSON dictionary, use '.' as a delimiter for subfields. Default is 'None' which returns everything.
        
        Additional Parameters:
        - `return_info` (bool): Flag to return additional information along with the response. Default is 'False'.
        - `validation` (bool): Flag to enable/disable input validation. Default is 'False'.

        Returns:
        - `json` (dict | None): Schedule calendar data.
        """
        
        params = nhlAPI.default_params
        params.update(kwargs)
        
        input_params = ["view", "validation", "return_info", "timeout", "retries", "backoff"]
        view, validation, return_info, timeout, retries, backoff = (params.get(param) for param in input_params)

        base_url = nhlAPI.base_urls.get("schedule_calendar")
        url = f"{base_url}now" if date == "now" else f"{base_url}{date}"
        data = {"data": make_api_request(url, timeout, retries, backoff, validation)}

        if data is None:
            return None

        filtered_data = filter_view(data, view, validation) if view is not None else data

        return {"path": url, "view": view, "response": filtered_data} if return_info else filtered_data

    @staticmethod 
    def get_schedule(date: str = "now", **kwargs: Any) -> dict:
        """
        Fetches schedule data for a specific date or today's date from the NHL API 'schedule' endpoint.

        Paramters:
        - `date` (str): The date for which to fetch the schedule data (in 'YYYY-MM-DD' format). Default is 'now'.

        Optional Parameters:
        - `view` (str| None): To drilldown the JSON dictionary, use '.' as a delimiter for subfields. Default is 'None' which returns everything.

        Additional Parameters:
        - `return_info` (bool): Flag to return additional information along with the response. Default is 'False'.
        - `validation` (bool): Flag to enable/disable input validation. Default is 'False'.
        
        Returns:
        - `json` (dict | None): Schedule data for a specific data based on a specified view.
        """

        #TODO inplement filter/exclude data
        params = nhlAPI.default_params
        params.update(kwargs)
        
        input_params = ["sort", "direction", "filter_fields", "filter_data", "exclude_data", "view", "validation", "return_info", "timeout", "retries", "backoff"]
        sort, direction, filter_fields, filter_data, exclude_data, view, validation, return_info, timeout, retries, backoff = (params.get(param) for param in input_params)

        base_url = nhlAPI.base_urls.get("schedule")
        url = f"{base_url}now" if date == "now" else f"{base_url}{date}"
        data = {"data": make_api_request(url, timeout, retries, backoff, validation)}

        if data is None:
            return None

        if sort:
            sort, direction = ([sort], [direction]) if isinstance(sort, str) else (sort, direction)
            for s, d in reversed(list(zip(sort, direction))):
                reverse = d.upper() == 'DESC'
                for game in data["data"]["gameWeek"]:
                        game["games"].sort(key=lambda x: (x.get(s) is None, x.get(s)), reverse=reverse)

        if filter_fields:
            filter_fields = [filter_fields] if isinstance(filter_fields, str) else filter_fields
            for games in data["data"]["gameWeek"]:
                games["games"] = [{key: game[key] for key in filter_fields if key in game} for game in games["games"]]

        filtered_data = filter_view(data, view, validation) if view is not None else data

        return {"path": url, "view": view, "response": filtered_data} if return_info else filtered_data

    @staticmethod
    def get_standings(date: str = "now", **kwargs: Any) -> dict:
        """
        Fetches NHL standings data for a specific date or today's date from the NHL API 'standings' enpoint.

        Parameters:
        - `date` (str): The date for which to fetch the standings data (in 'YYYY-MM-DD' format). Default is 'now'.

        Optional Parameters:
        - `sort` (str | list[str] | None): Field to sort the teams by. Default is `None`.
        - `direction` (str | list[str] | None): Direction of sorting. Default is `None`.
        - `filter_fields` (str | list[str] | None): The fields to include. Default is `None` which returns all fields.
        - `filter_data` (dict | None): Dictionary containing filter parameters and their corresponding values. Default is 'None' which returns everything.
        - `exclude_data` (dict | None): Dictionary containing filter parameters and their corresponding values to exclude from the response. Default is 'None' which excludes nothing.
        - `view` (str | None): To drilldown the JSON dictionary, use '.' as a delimiter for subfields. Default is 'None' which returns everything.

        Additional Parameters:
        - `return_info` (bool): Flag to return additional information along with the response. Default is 'False'.
        - `validation` (bool): Flag to enable/disable input validation. Default is 'False'. Note: partially implemented.
        - `timeout` (int): The timeout duration for the request in seconds. Default is '10'.
        - `retries` (int): The number of retry attempts in case of failure. Default is '3'.
        - `backoff` (float): The delay before the next retry attempt in seconds. Default is '0.3'.

        Returns:
        - `json` (dict | None): Standings data for a provided date.
        """
        
        params = nhlAPI.default_params
        params.update(kwargs)
        
        input_params = ["sort", "direction", "filter_fields", "filter_data", "exclude_data", "view", "validation", "return_info", "timeout", "retries", "backoff"]
        sort, direction, filter_fields, filter_data, exclude_data, view, validation, return_info, timeout, retries, backoff = (params.get(param) for param in input_params)

        base_url = nhlAPI.base_urls.get("standings")
        url = f"{base_url}now" if date == "now" else f"{base_url}{date}"
        data = {"data": make_api_request(url, timeout, retries, backoff, validation)}

        if sort:
            sort, direction = ([sort], [direction]) if isinstance(sort, str) else (sort, direction)
            for s, d in reversed(list(zip(sort, direction))):
                reverse = d.upper() == 'DESC'
                data["data"]["standings"].sort(key=lambda x: (x.get(s) is None, x.get(s)), reverse=reverse)

        filtered_data = filter_json_data(data["data"]["standings"], filter_data) if filter_data is not None else data["data"]["standings"]
        filtered_data = {"data":{"wildCardIncicator": data["data"].get("wildCardIndicator", {}), "standings": filter_json_data(filtered_data, exclude_data, exclude=True)}} if exclude_data is not None else {"data":{"wildCardIndicator": data["data"].get("wildCardIndicator", {}), "standings": filtered_data}}

        if filter_fields:
            filter_fields = [filter_fields] if isinstance(filter_fields, str) else filter_fields
            filtered_data["data"]["standings"] = [{key: team[key] for key in filter_fields if key in team} for team in filtered_data["data"]["standings"]]

        filtered_data["data"]["total"] = len(filtered_data["data"]["standings"])
        filtered_data = filter_view(filtered_data, view, validation) if view is not None else filtered_data

        return {"path": url, "view": view, "fields": filter_fields, "filters": filter_data, "exclude": exclude_data, "sort": {s: d for s, d in zip(sort, direction)} if sort is not None else None, "response": filtered_data} if return_info else filtered_data

    @staticmethod
    def get_standings_seasons(**kwargs: Any) -> dict:
        """
        Fetch data from the NHL API 'standings-season' endpoint.

        Optional Parameters:
        - `sort` (str | list[str] | None): Field to sort the teams by. Default is `None`.
        - `direction` (str | list[str] | None): Direction of sorting. Default is `None`.
        - `filter_fields` (str | list[str] | None): The fields to include. Default is `None` which returns all fields.
        - `filter_data` (dict | None): Dictionary containing filter parameters and their corresponding values. Default is 'None' which returns everything.
        - `exclude_data` (dict | None): Dictionary containing filter parameters and their corresponding values to exclude from the response. Default is 'None' which excludes nothing.
        - `view` (str | None): To drilldown the JSON dictionary, use '.' as a delimiter for subfields. Default is 'None' which returns everything.

        Additional Parameters:
        - `return_info` (bool): Flag to return additional information along with the response. Default is 'False'.
        - `validation` (bool): Flag to enable/disable input validation. Default is 'False'. Note: partially implemented.
        - `timeout` (int): The timeout duration for the request in seconds. Default is '10'.
        - `retries` (int): The number of retry attempts in case of failure. Default is '3'.
        - `backoff` (float): The delay before the next retry attempt in seconds. Default is '0.3'.

        Returns:
        - `json` (dict | None): NHL standings available seasons data.
        """

        params = nhlAPI.default_params
        params.update(kwargs)

        input_params = ["sort", "direction", "filter_fields", "filter_data", "exclude_data", "view", "validation", "return_info", "timeout", "retries", "backoff"]
        sort, direction, filter_fields, filter_data, exclude_data, view, validation, return_info, timeout, retries, backoff = (params.get(param) for param in input_params)

        url = nhlAPI.base_urls.get("standings_season")
        data = {"data": make_api_request(url, timeout, retries, backoff, validation)}

        if sort:
            sort, direction = ([sort], [direction]) if isinstance(sort, str) else (sort, direction)
            for s, d in reversed(list(zip(sort, direction))):
                reverse = d.upper() == 'DESC'
                data["data"]["seasons"].sort(key=lambda x: (x.get(s) is None, x.get(s)), reverse=reverse)

        filtered_data = filter_json_data(data["data"]["seasons"], filter_data) if filter_data is not None else data["data"]["seasons"]
        #TODO troubleshoot excluding by fields with a bool value of 'false' which doesnt work even though it works for bool values of 'true'.
        filtered_data = {"data":{"currentDate": data["data"].get("currentDate", {}), "seasons": filter_json_data(filtered_data, exclude_data, exclude=True)}} if exclude_data is not None else {"data":{"currentDate": data["data"].get("currentDate", {}), "seasons": filtered_data}}

        if filter_fields:
            filter_fields = [filter_fields] if isinstance(filter_fields, str) else filter_fields
            filtered_data["data"]["seasons"] = [{key: season[key] for key in filter_fields if key in season} for season in filtered_data["data"]["seasons"]]

        filtered_data["data"]["total"] = len(filtered_data["data"]["seasons"])
        filtered_data = filter_view(filtered_data, view, validation) if view is not None else filtered_data

        return {"path": url, "view": view, "fields": filter_fields, "filters": filter_data, "exclude": exclude_data, "sort": {s: d for s, d in zip(sort, direction)} if sort is not None else None, "response": filtered_data} if return_info else filtered_data

    @staticmethod 
    def get_scores(date: str = "now", **kwargs: Any) -> dict:
        """
        Fetches NHL scores data for a specific date or today's date.

        Parameters:
        - `date` (str): The date for which to fetch the scores data (in 'YYYY-MM-DD' format). Default is 'now'.

        Optional Parameters:
        - `view` (str| None): To drilldown the JSON dictionary, use '.' as a delimiter for subfields. Default is 'None' which returns everything.
        
        Additional Parameters:
        - `return_info` (bool): Flag to return additional information along with the response. Default is 'False'.
        - `validation `(bool): Flag to enable/disable input validation. Default is 'False'.

        Returns:
        - `json` (dict | None): Scores data.
        """
        params = nhlAPI.default_params
        params.update(kwargs)

        #TODO implement filter/exclude data
        input_params = ["sort", "direction", "filter_fields", "filter_data", "exclude_data", "view", "validation", "return_info", "timeout", "retries", "backoff"]
        sort, direction, filter_fields, filter_data, exclude_data, view, validation, return_info, timeout, retries, backoff = (params.get(param) for param in input_params)

        base_url = nhlAPI.base_urls.get("score")
        url = f"{base_url}now" if date == "now" else f"{base_url}{date}"
        data = {"data":make_api_request(url, timeout, retries, backoff, validation)}

        if sort:
            sort, direction = ([sort], [direction]) if isinstance(sort, str) else (sort, direction)            
            for s, d in reversed(list(zip(sort, direction))):
                reverse = d.upper() == 'DESC'
                data["data"]["games"].sort(key=lambda x: (x.get(s) is None, x.get(s)), reverse=reverse)

        if filter_fields:
            filter_fields = [filter_fields] if isinstance(filter_fields, str) else filter_fields
            data["data"]["games"] = [{key: game[key] for key in filter_fields if key in game} for game in data["data"]["games"]]

        filtered_data = filter_view(data, view, validation) if view is not None else data

        return {"path": url, "view": view, "response": filtered_data} if return_info else filtered_data

    @staticmethod
    def get_playbyplay(game_id: Union[int, str], **kwargs: Any) -> dict:
        """
        Fetch data from the NHL API player 'play-by-play' endpoint.

        Parameters:
        - `game_id` (int | str): The ID of the game.

        Optional Parameters:
        - `sort` (str | list[str] | None): Field to sort the plays by. Default is 'None'.
        - `direction` (str | list[str] | None): Direction of sorting. Default is 'None'.
        - `filter_fields` (str | list[str] | None): The fields to include. Default is 'None' which returns all fields.
        - `filter_data` (dict | None): Dictionary containing filter parameters and their corresponding values. Default is 'None' which returns everything.
        - `exclude_data` (dict | None): Dictionary containing filter parameters and their corresponding values to exclude from the response. Default is 'None' which excludes nothing.
        - `view` (str | None): To drilldown the JSON dictionary, use '.' as a delimiter for subfields. Default is 'None' which returns everything.

        Additional Parameters:
        - `return_info` (bool): Flag to return additional information along with the response. Default is 'False'.
        - `validation` (bool): Flag to enable/disable input validation. Default is 'False'. Note: partially implemented.
        - `timeout` (int): The timeout duration for the request in seconds. Default is '10'.
        - `retries` (int): The number of retry attempts in case of failure. Default is '3'.
        - `backoff` (float): The delay before the next retry attempt in seconds. Default is '0.3'.
        
        Returns:
        - `json` (dict | None): Play by play data.
        """
        
        params = nhlAPI.default_params
        params.update(kwargs)
        
        input_params = ["sort", "direction", "filter_fields", "filter_data", "exclude_data", "view", "validation", "return_info", "timeout", "retries", "backoff"]
        sort, direction, filter_fields, filter_data, exclude_data, view, validation, return_info, timeout, retries, backoff = (params.get(param) for param in input_params)

        game_id = int(game_id)
        base_url = nhlAPI.base_urls.get("gamecenter")
        url = f"{base_url}{game_id}/play-by-play"

        data = {"data": make_api_request(url, timeout, retries, backoff, validation)}

        if data["data"] is None:
            return None

        if sort:
            sort, direction = ([sort], [direction]) if isinstance(sort, str) else (sort, direction)            
            for s, d in reversed(list(zip(sort, direction))):
                reverse = d.upper() == 'DESC'
                data["data"]["plays"].sort(key=lambda x: (x.get(s) is None, x.get(s)), reverse=reverse)

        if filter_fields:
            filter_fields = [filter_fields] if isinstance(filter_fields, str) else filter_fields
            data["data"]["plays"] = [{key: play[key] for key in filter_fields if key in play} for play in data["data"]["plays"]]

        data["data"]["plays"] = filter_json_data(data["data"]["plays"], filter_data) if filter_data is not None else data["data"]["plays"]
        data["data"]["plays"] = filter_json_data(data["data"]["plays"], exclude_data, exclude=True) if exclude_data is not None else data["data"]["plays"]

        filtered_data = filter_view(data, view, validation) if view is not None else data

        return {"path": url, "view": view, "fields": filter_fields, "filters": filter_data, "exclude": exclude_data, "sort": {s: d for s, d in zip(sort, direction)} if sort is not None else None, "response": filtered_data} if return_info else filtered_data

    @staticmethod
    def get_boxscore(game_id: Union[int, str], **kwargs: Any) -> dict:
        """
        Fetch data from the NHL API player 'boxscore' endpoint.

        Parameters:
        - `game_id` (int | str): The ID of the game.

        Optional Parameters:
        - `sort` (str | list[str] | None): Field to sort the plays by. Default is 'None'. Note: only applies to 'playerByGameStats'.
        - `direction` (str | list[str] | None): Direction of sorting. Default is 'None'. Note: only applies to 'playerByGameStats'.
        - `filter_fields` (str | list[str] | None): The fields to include. Default is 'None' which returns all fields. Note: only applies to 'playerByGameStats'.
        - `filter_data` (dict | None): Dictionary containing filter parameters and their corresponding values. Default is 'None' which returns everything. Note: only applies to 'playerByGameStats'.
        - `exclude_data` (dict | None): Dictionary containing filter parameters and their corresponding values to exclude from the response. Default is 'None' which excludes nothing. Note: only applies to 'playerByGameStats'.
        - `view` (str | None): To drilldown the JSON dictionary, use '.' as a delimiter for subfields. Default is 'None' which returns everything.

        Additional Parameters:
        - `return_info` (bool): Flag to return additional information along with the response. Default is 'False'.
        - `validation` (bool): Flag to enable/disable input validation. Default is 'False'. Note: partially implemented.
        - `timeout` (int): The timeout duration for the request in seconds. Default is '10'.
        - `retries` (int): The number of retry attempts in case of failure. Default is '3'.
        - `backoff` (float): The delay before the next retry attempt in seconds. Default is '0.3'.

        Returns:
        - `json` (dict | None): Boxscore data.
        """

        params = nhlAPI.default_params
        params.update(kwargs)
        
        input_params = ["sort", "direction", "filter_fields", "filter_data", "exclude_data", "view", "validation", "return_info", "timeout", "retries", "backoff"]
        sort, direction, filter_fields, filter_data, exclude_data, view, validation, return_info, timeout, retries, backoff = (params.get(param) for param in input_params)

        game_id = int(game_id)
        base_url = nhlAPI.base_urls.get("gamecenter")
        url = f"{base_url}{game_id}/boxscore"
        data = {"data": make_api_request(url, timeout, retries, backoff, validation)}

        if data["data"] is None:
            return None
        
        if sort:
            sort, direction = ([sort], [direction]) if isinstance(sort, str) else (sort, direction)            
            for s, d in reversed(list(zip(sort, direction))):
                reverse = d.upper() == 'DESC'
                for team in data["data"]["playerByGameStats"]:
                    for pos_group in data["data"]["playerByGameStats"][team]:
                        data["data"]["playerByGameStats"][team][pos_group].sort(key=lambda x: (x.get(s) is None, x.get(s)), reverse=reverse)

        for team in data["data"]["playerByGameStats"]:   
            for pos_group in data["data"]["playerByGameStats"][team]:
                position_group_data = data["data"]["playerByGameStats"][team][pos_group]
                if filter_data is not None:
                    position_group_data = filter_json_data(position_group_data, filter_data)
                if exclude_data is not None:
                    position_group_data = filter_json_data(position_group_data, exclude_data, exclude=True)
                data["data"]["playerByGameStats"][team][pos_group] = position_group_data

        if filter_fields:
            for team in data["data"]["playerByGameStats"]:
                for pos_group in data["data"]["playerByGameStats"][team]:
                    filter_fields = [filter_fields] if isinstance(filter_fields, str) else filter_fields
                    data["data"]["playerByGameStats"][team][pos_group] = [{key: player[key] for key in filter_fields if key in player} for player in data["data"]["playerByGameStats"][team][pos_group]]

        filtered_data = filter_view(data, view, validation) if view is not None else data

        return {"path": url, "view": view, "fields": filter_fields, "filters": filter_data, "exclude": exclude_data, "sort": {s: d for s, d in zip(sort, direction)} if sort is not None else None, "response": filtered_data} if return_info else filtered_data

    @staticmethod 
    def get_shifts(game_id: Union[int, str], **kwargs: Any) -> dict:
        """
        Fetch data from the NHL API player 'shiftcharts' endpoint.

        Parameters:
        - `game_id` (int): The ID of the game.

        Optional Parameters:
        - `sort` (str | None): The field to sort the data by. Default is 'None'.
        - `direction` (str | None): The sorting direction. Default is 'None'.
        - `view` (str | None): The part of the json to return, use '.' as a delimiter for subfields. Default is 'None' (to return everything).

        Additional Parameters:
        - `return_info` (bool): Flag to return the API path along with the response. Default is 'False'.
        - `validation` (bool): Flag to enable/disable input validation. Default is 'False'.

        Returns:
        - `json` (dict | None): Shift data for a specific game.
        """

        params = nhlAPI.default_params
        params.update(kwargs)
        
        input_params = ["sort", "direction", "filter_fields", "filter_data", "exclude_data", "view", "validation", "return_info", "timeout", "retries", "backoff"]
        sort, direction, filter_fields, filter_data, exclude_data, view, validation, return_info, timeout, retries, backoff = (params.get(param) for param in input_params)

        game_id = int(game_id)
        base_url = nhlAPI.base_urls.get("shiftcharts")
        sort_param = construct_sorting_params(sort, direction, validation) if sort is not None else ""
        url = f"{base_url}?{sort_param}&cayenneExp=gameId%3E={game_id}" if sort_param else f"{base_url}?cayenneExp=gameId%3E={game_id}"
        data = make_api_request(url, timeout, retries, backoff, validation)

        if data is None:
            return None
        
        #TODO troubleshoot
        filtered_data = filter_json_data(data["data"], filter_data) if filter_data is not None else data["data"]
        filtered_data = {"data": filter_json_data(filtered_data, exclude_data, exclude=True)} if exclude_data is not None else {"data": filtered_data}
        
        #TODO troubleshoot
        if filter_fields:
            filter_fields = [filter_fields] if isinstance(filter_fields, str) else filter_fields
            filtered_data["data"] = [{key: shift[key] for key in filter_fields if key in shift} for shift in filtered_data["data"]]
        
        filtered_data = filter_view(data, view, validation) if view is not None else data
        sort, direction = ([sort], [direction]) if isinstance(sort, str) else (sort, direction)

        return {"path": url, "view": view, "fields": filter_fields, "filters": filter_data, "exclude": exclude_data, "sort": {s: d for s, d in zip(sort, direction)} if sort is not None else None, "response": filtered_data} if return_info else filtered_data

    @staticmethod
    def get_stats(key: str = "skater", report: str = "summary", **kwargs: Any) -> dict:
        """
        Fetch data from the NHL API 'stats' endpoint for a season, a range of seasons, or a range of dates.

        Parameters:
        - `key` (str): 'skater', 'goalie', or 'team'.
        - `report` (str): The report type to return. Default is 'summary'. Note: need to troubleshoot shootout and penaltyShots report.

        For a season:
        - `season` (str): The season to return the skaters stats from (e.g., '20232024').

        For a range of seasons:
        - `start_season` (str): The starting season of the range. Default is 'None'.
        - `end_season` (str): The ending season of the range. Default is 'None'.

        For a range of dates:
        - `start_date` (str): The starting date of the range (YYYY-MM-DD). Default is 'None'.
        - `end_date` (str): The ending date of the range (YYYY-MM-DD). Default is 'None'.

        Returns:
        - `json`: Skater, Goalie, or Team season stats for the specified report.

        Additional Parameters:
        - `aggregate` (bool): Boolean option to aggregate skaters stats over multiple seasons or games. Default is 'True'.
        - `game_type` (int): The type of game ('1' for pre-season, '2' for regular season, '3' for playoffs, '4' for all-star games). Default is '2'.
        - `home_or_road` (str): The players/teams stats from home or away games ('H' for home, 'R' for road/away).  Default is 'None' which returns all games.
        - `game_result` (str): The players/teams stats from games with the provided result ('W' for wins, 'L' for losses, and 'O' for overtime losses). Default is 'None' which returns all game results.
        - `min_gp` (int): The minimum number of games played. Default is '0'.
        - `max_gp` (int): The maximum number of games played. Default is 'None'.
        - `franchise_id` (int): The franchise identifier to return the players/teams stats from. Default is 'None' which returns all franchises.
        - `opponent_franchise_id` (int): The opponent franchise identifier to return the players/teams stats from. Default is 'None' which returns all opponent franchises.
        - `position` (str | list): The positions of the players. Default is 'None' which returns all positions. Note: only valid for a key of 'skater' or 'goalie'.
        - `player_name` (str): The full name of the player to filter. Default is 'None' which returns all players. Note: only valid for a key of 'skater' or 'goalie'.
        - `nationality_code` (str): The nationlity code of the players to return the stats from (e.g., 'CAN'). Default is 'None' which returns all nationalities. Note: only valid for a key of 'skater' or 'goalie'.
        - `birth_state_province_code` (str): The birth state province code of the players to return the stats from (e.g., 'ON'). Default is 'None' which returns all birth state provinces. Note: only valid for a key of 'skater' or 'goalie'.
        - `is_rookie` (bool): Whether the players are a rookie (True to return rookies, False to exclude rookies / return veterans). Default is 'None' which returns all players. Note: only valid for a key of 'skater' or 'goalie'.
        - `is_active` (bool): Whether the players are active (True to return active players, False to return incactive players). Default is 'None' which returns all players. Note: only valid for a key of 'skater' or 'goalie'.
        - `is_in_hall_of_fame` (bool): Wether the players are in the hall of fame. Default is 'None' which returns all players. Note: only valid for a key of 'skater' or 'goalie'.
        - `draft_round` (str | int): The draft round of the players to return the stats from. Default is 'None' which returns all rounds. Note: only valid for a key of 'skater' or 'goalie'.
        - `draft_year` (str | int): The draft year of the players to return the stats from (e.g., '2012'). Note: if no draft round is input, returns from first round, and only returns data for a single draft round.  Default is 'None' which returns all draft years. Note: only valid for a key of 'skater' or 'goalie'.
        - `shoots_catches` (str): The handedness of the players to return the stats from ('L' for left, 'R' for right). Default is 'None' which returns all players. Note: only valid for a key of 'skater' or 'goalie'.
        - `sort` (str | list): The sort field(s) for the query. Can be a single string or a list of strings. 'None' returns skaters with no sorting.
        - `direction` (str | list): The sort direction(s) for the query. Can be a single string or a list of strings.
        - `property` (str | list): The property to filter by (note: works alongside a provided comparator and value). Default is 'None'.
        - `comparator` (str | list): The comparator to filter by ('>=', '=', and '<=') (note: works alongside a provided comparator and value). Default is 'None'.
        - `value` (str | int | list): The value to filter by (note: works alongside a provided comparator and value). Default is 'None'.
        - `limit` (int): The max number of players/teams to return if return_all is set to 'False'.  Default is '100'.
        - `start` (int): The starting point of the list to return the players/teams from if return_all is set to 'False'. Default is '0'.
        - `return_all` (bool): Flag to determine whether to return all players/teams or only a single loop with the provided limit. Default is 'True'.
        - `return_info` (bool): Flag to return the API path along with the response. Default is 'False'.
        - `validation` (bool): Flag to enable/disable input validation. Default is 'True'.

        """

        default_params = {**nhlAPI.default_params, **nhlAPI.report_params.get(key, {})}
        default_params.update(kwargs)
        
        input_params = ["season", "start_season", "end_season", "start_date", "end_date", "min_gp", "max_gp", "sort", "direction", "filter_fields", "view", "validation", "return_info", "timeout", "retries", "backoff"]
        season, start_season, end_season, start_date, end_date, min_gp, max_gp, sort, direction, filter_fields, view, validation, return_info, timeout, retries, backoff = (default_params.get(param) for param in input_params)
        is_game = start_date is not None or end_date is not None

        base_url = nhlAPI.base_urls.get("stats")
        cayenneExp = construct_cayenne_exp(season=season, start_season=start_season, end_season=end_season, start_date=start_date, end_date=end_date, default_kwargs=default_params)
        factCayenneExp = construct_fact_cayenne_exp(min_gp=min_gp, max_gp=max_gp, default_kwargs=default_params)
        params = {"isAggregate": str(default_params.get("aggregate", True)), "isGame": str(is_game), "start": "0", "limit": str(default_params.get("limit", True)), "factCayenneExp": factCayenneExp, "cayenneExp": cayenneExp}

        if sort is not None:
            sort_param = construct_sorting_params(sort=sort, direction=direction, validation=validation)
            sort_param = sort_param[len("sort="):] if sort_param.startswith("sort=") else sort_param 
            params["sort"] = sort_param

        all_data = []
        if default_params.get("return_all", True):
            while True:
                url = f"{base_url}{key}/{report}?{'&'.join([f'{key}={value}' for key, value in params.items()])}"
                data = make_api_request(url, timeout, retries, backoff, validation)
                if data is None:
                    return None
                all_data.extend(data.get("data", []))
                if len(all_data) >= data.get("total", 0):
                    break
                params["start"] = str(len(all_data)) #update starting position

            if filter_fields:
                filter_fields = [filter_fields] if isinstance(filter_fields, str) else filter_fields
                all_data = [{key: player[key] for key in filter_fields if key in player} for player in all_data]

            all_data = {"data": all_data, "total": len(all_data)}
            filtered_data = filter_view(all_data, view, validation) if view is not None else all_data
            sort = [sort] if isinstance(sort, str) else sort
            direction = [direction] if isinstance(direction, str) else direction

            return {"path": url, "view": view, "fields": filter_fields, "sort": {s: d for s, d in zip(sort, direction)} if sort is not None else None, "response": filtered_data} if return_info else filtered_data

        else:
            params["start"] = str(default_params.get("start", True))
            url = f"{base_url}{key}/{report}?{'&'.join([f'{key}={value}' for key, value in params.items()])}"
            data = make_api_request(url, timeout, retries, backoff, validation)

            if filter_fields:
                filter_fields = [filter_fields] if isinstance(filter_fields, str) else filter_fields
                data["data"] = [{key: player[key] for key in filter_fields if key in player} for player in data["data"]]

            filtered_data = filter_view(data, view, validation) if view is not None else data
            sort = [sort] if isinstance(sort, str) else sort
            direction = [direction] if isinstance(direction, str) else direction

            return {"path": url, "view": view, "fields": filter_fields, "sort": {s: d for s, d in zip(sort, direction)} if sort is not None else None, "response": filtered_data} if return_info else filtered_data
