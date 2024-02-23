# NHL API Scraper Documentation

Documentation for the [NHL API Python Scraper](https://github.com/DI0Rdano/NHL-API-Python-Scraper/blob/main/nhlAPI.py). </br>

**NHL API Python Scraper** </br>
Python based scraping functions for various NHL API endpoints. Configured to the work with the new NHL API. </br>
Constructed for personal use, not intended to be comprehensive. </br>


## Table of Contents

### NHL API Information

>[Base URLs & Endpoints](#base-urls--endpoints) </br>
>[Modifiers](#modifiers)

### Scraping Functions

>**General** </br>
>[get_config](#get-config) </br>
>[get_countries](#get-countries) </br>
>[get_seasons](#get-seasons) </br>
>[get_draftrounds](#get-draft-rounds) </br>

>**Stats** </br>
>[get_skaters_stats](#get-skaters-stats) </br>
>[get_teams_stats](#get-teams-stats)</br>
>[get_goalies_stats](#get-goalies-stats)</br>

>**Players** </br>
>[get_players](#get-players) </br>
>[get_player_landing](#get-player-landing)</br>
>[get_player_gamelog](#get-player-gamelog)</br>

>**Teams** </br>
>[get_franchises](#get-franchises) </br>
>[get_team_information](#get-team-information)</br>
>[get_roster](#get-roster) </br>
>[get_roster_seasons](#get-roster-seasons) </br>
>[get_club_stats_seasons](#get-club-stats-seasons)</br>
>[get_club_stats](#get-club-stats)</br>

>**Games** </br>
>[get_playbyplay](#get-play-by-play)</br>
>[get_boxscore](#get-boxscore)</br>
>[get_shifts](#get-shifts)</br>
>[get_scores](#get-scores)</br>

>**Schedule** </br>
>[get_schedule_calendar](#get-schedule-calendar)</br>
>[get_schedule](#get-schedule)</br>
>[get_club_schedule](#get-club-schedule)</br>

>**Standings** </br>
>[get_standings](#get-standings)</br>
>[get_standings_seasons](#get-standings-seasons)</br>
</br>

## Base URLs & Endpoints

### `https://api.nhle.com/stats/rest/en` </br>

General Endpoints:
- `/config`
- `/country`
- `/franchise`
- `/season`
</br>
</br>

### `https://api-web.nhle.com/v1` </br>

Player Endpoints:
- `/player/{playerId}`
    - `/landing`
    - `/game-log/{season}/{gameType}`

Club Endpoints:
- `/club-schedule/{teamAbbrev}`
    - `/month`
        - `/now`
        - `/{date}`
    - `/week`
        - `/now`
        - `/{date}`
- `/club-stats-season/{teamAbbrev}`

Roster Endpoints:
- `/roster-season/{teamAbbrev}`
- `/roster/{teamAbbrev}/{season}`

Gamecenter Endpoints:
- `/gamecenter/{gameId}`
    - `/play-by-play`
    - `/boxscore`

Score Endpoints:
- `/score`
    - `/now`
    - `/{date}`

Schedule Endpoints:
- `/schedule`
    - `/now`
    - `/{date}`
- `/schedule-calendar`
    - `/now`
    - `/{date}`

Standings Endpoints:
- `/standings`
- `/standings-season`
- `/standings`
    - `/now`
    - `/{date}`
</br>
</br>

#TODO add more base urls & endpoints

Parameters:
- `playerId` e.g., '8479318' for Auston Matthews.
- `season` e.g., '20232024'.
- `gameType` Range from 1-4. '2' for regular season, '3' for playoffs.
- `teamAbbrev` 3 letter abbreviation of the team e.g., 'TOR' for the Toronto Maple Leafs.
- `date` Date in the format of 'YYYY-MM-DD'.
- `gameId`

[Back to Top](#table-of-contents)

## Modifiers

Introduce modifiers by adding a `?` suffix to the url. Combine multiple modifiers with `&`.
- `include=`
- `sort=`
    - To specify the sort direction, use the following structure. `[{"property": , "direction": }]` </br>
    Sort multiple parameters by adding to the list. Valid sort directions include `"ASC"` and `"DESC"`. </br>
    Example: `sort=[{"property": "points", "direction": "DESC"}, {"property": "playerId", "direction": "ASC"}]`
- `cayenneExp=`
    - To specify the cayenneExp parameters, use the following structure. `{parameter}={value}` </br>
    Use `" and "` to join together multiple parameters. <br>
    Example: `cayenneExp=seasonId=20232024 and gameTypeId=2`
- `factCayenneExp=`
    - To specify the factCayenneExp parameters, use the following structure. `{parameter}{comparator}{value}` </br>
    Valid comparators include `>=`, `=`, and `<=`. Use `" and "` to join together multiple parameters. <br>
    Example: `factCayenneExp=gamesPlayed>=0 and gamesPlayed<=10` </br>
    Note: factCayenneExp must be included before cayenneExp to work properly.
</br>

[Back to Top](#table-of-contents)

## Python Scraper

### Get Config
Fetch data from the NHL API 'config' endpoint.

`get_config(view=None)`

Parameters:
- view (str, optional): The part of the JSON to return, use '.' as a delimiter for subfields. Default is None (returns everything).

Returns:
- dict: Configuration data as a JSON dictionary based on the specified view.
- None: In case of an error.
</br>

<details>
  <summary>Example:</summary>

```
get_config()

#TODO add example response

```

</details>
</br>

[Back to Top](#table-of-contents)

---

### Get Countries
Fetch data from the NHL API 'country' endpoint.

`get_countries(include_stateProvinces=True, sort="countryName", direction="ASC", filter=None, input_validation=True)`

Parameters:
- include_stateProvinces (bool): Whether to include state provinces in the response. Default is 'True'.
- sort (str, optional): Field to sort the countries by. Default is 'countryName'.
- direction (str): Sort direction ('ASC' for ascending, 'DESC' for descending). Default is 'ASC'.
- filter (str or list, optional): The fields to include in the json response. Default is 'None' which returns all fields.
- input_validation (bool): Flag to enable/disable input validation. Default is 'True'.

Returns:
- dict: country data as a json dictionary.
- None: In case of an error.
</br>

<details>
  <summary>Example:</summary>

```
get_countries()

{
    "data": [
        ...,
        {
            "id": "CAN",
            "country3Code": "CAN",
            "countryCode": "CA",
            "countryName": "Canada",
            "hasPlayerStats": 1,
            "imageUrl": "/images/country/48/CAN.png",
            "iocCode": "CAN",
            "isActive": 1,
            "nationalityName": "Canadian",
            "olympicUrl": "/ice/page.htm?id=60524",
            "stateProvinces": [
                {
                    "id": "AB",
                    "country3Code": "CAN",
                    "stateProvinceName": "Alberta"
                },
                ...
            ],
            "thumbnailUrl": "/images/country/16/CAN.png"
        },
        ...
    ],
    "total": 49
}
```

</details>
</br>

[Back to Top](#table-of-contents)

---


### Get Seasons
Fetch data from the NHL API 'season' endpoint.

`get_seasons(sort="id", direction="DESC", filter=None, input_validation=True)`

Parameters:
- sort (str or list, optional): Field to sort the seasons by. Default is "id". Valid values are "id" and other fields present in the NHL API response.
- direction (str or list): Direction of sorting. Default is "DESC". Valid values are "ASC" (ascending) and "DESC" (descending).
- filter (str or list, optional): The fields to include in the json response. Default is 'None' which returns all fields.
- input_validation (bool): Flag to enable/disable input validation. Default is True.

Returns:
- dict: Season data as a JSON dictionary.
- None: In case of an error.

</br>

<details>
  <summary>Example:</summary>

```
get_seasons()

#TODO add example response

```

</details>
</br>

[Back to Top](#table-of-contents)

---

### Get Draft Rounds
Fetch data from the NHL API 'draft' endpoint.

`get_draftrounds(sort="draftYear", direction="DESC", filter=None, input_validation=True)`

Parameters:
- sort (str or list, optional): Field to sort the draft rounds by. Default is "draftYear".
- direction (str or list): Direction of sorting. Default is "DESC".
- filter (str or list, optional): The fields to include in the json response. Default is 'None' which returns all fields.
- input_validation (bool): Flag to enable/disable input validation. Default is True.

Returns:
- dict: Draft round data as a json dictionary.
- None: In case of an error.

</br>

<details>
  <summary>Example:</summary>

```
get_draftrounds()

#TODO add example response

```

</details>
</br>

[Back to Top](#table-of-contents)

---

### Get Skaters Stats
Fetch data from the NHL API skater 'skater' endpoint.

`get_skaters_stats(season=None, report="summary", aggregate=True, min_gp=0, max_gp=None, sort=["points", "goals", "assists", "playerId"], sort_direction=["DESC", "DESC", "DESC", "ASC"], game_type=2, start_season=None, end_season=None, is_game=False, start_date=None, end_date=None, franchise_id=None, opponent_franchise_id=None, position=None, skater_full_name=None, is_rookie=None, is_active=None, is_in_hall_of_fame=None, nationality_code=None, birth_state_province_code=None, home_or_road=None, game_result=None, draft_round=None, draft_year=None, shoots=None, property=None, comparator=None, value=None, skater_limit=100, input_validation=True)`

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

</br>
<details>
  <summary>Example for a season:</summary>

```
get_skaters_stats()

#TODO add example response

```

</details>
</br>

<details>
  <summary>Example for a range of seasons:</summary>

```
get_skaters_stats()

#TODO add example response

```

</details>
</br>

<details>
  <summary>Example for a range of games:</summary>

```
get_skaters_stats()

#TODO add example response

```

</details>
</br>

[Back to Top](#table-of-contents)

---

### Get Teams Stats

</br>

<details>
  <summary>Example:</summary>

```
get_teams_stats()

#TODO add example response

```

</details>
</br>

[Back to Top](#table-of-contents)

---

### Get Goalies Stats

</br>

<details>
  <summary>Example:</summary>

```
get_goalies_stats()

#TODO add example response

```

</details>
</br>

[Back to Top](#table-of-contents)

---

### Get Players

</br>

<details>
  <summary>Example:</summary>

```
get_players()

#TODO add example response

```

</details>
</br>

[Back to Top](#table-of-contents)

---

### Get Player Landing

</br>

<details>
  <summary>Example:</summary>

```
get_player_landing()

#TODO add example response

```

</details>
</br>

[Back to Top](#table-of-contents)

---

### Get Player Gamelog

</br>

<details>
  <summary>Example:</summary>

```
get_player_gamelog()

#TODO add example response

```

</details>
</br>

[Back to Top](#table-of-contents)

---

### Get Franchises
Fetch data from the NHL API 'franchise' endpoint.

`get_franchises(include_firstSeason=True, include_lastSeason=True, sort="fullName", direction="ASC", filter=None, input_validation=True)`

Parameters:
- include_firstSeason (bool): Whether to include first season information. Default is True.
- include_lastSeason (bool): Whether to include last season information. Default is True.
- sort (str, optional): Field to sort the franchises by. Default is "fullName". Valid values are "fullName", "teamCommonName", "teamPlaceName", and "id".
- direction (str): Sort direction. Default is "ASC".
- filter (str or list, optional): The fields to include in the json response. Default is 'None' which returns all fields.
- input_validation (bool): Flag to enable/disable input validation. Default is True.

Returns:
- dict: Franchise data as a JSON dictionary.
- None: In case of an error.
</br>

<details>
  <summary>Example:</summary>

```
get_franchises()

#TODO add example response

```

</details>
</br>

[Back to Top](#table-of-contents)

---

### Get Team Information

</br>

[Back to Top](#table-of-contents)

---

### Get Roster

</br>

<details>
  <summary>Example:</summary>

```
get_roster()

#TODO add example response

```

</details>
</br>

[Back to Top](#table-of-contents)

---

### Get Roster Seasons

</br>

<details>
  <summary>Example:</summary>

```
get_roster_seasons()

#TODO add example response

```

</details>
</br>

[Back to Top](#table-of-contents)

---

### Get Club Stats Seasons

</br>

[Back to Top](#table-of-contents)

---

### Get Club Stats

</br>

[Back to Top](#table-of-contents)

---

### Get Club Schedule

</br>

[Back to Top](#table-of-contents)


---

### Get Play By Play

</br>

<details>
  <summary>Example:</summary>

```
get_playbyplay()

#TODO add example response

```

</details>
</br>

[Back to Top](#table-of-contents)

---

### Get Boxscore

</br>

[Back to Top](#table-of-contents)

---

### Get Shifts

</br>

[Back to Top](#table-of-contents)

---

### Get Scores

</br>

<details>
  <summary>Example:</summary>

```
get_scores()

#TODO add example response

```

</details>
</br>

[Back to Top](#table-of-contents)

---

### Get Schedule Calendar

</br>

<details>
  <summary>Example:</summary>

```
get_schedule_calendar()

#TODO add example response

```

</details>
</br>

[Back to Top](#table-of-contents)

---

### Get Schedule

</br>

<details>
  <summary>Example:</summary>

```
get_schedule()

#TODO add example response

```

</details>
</br>

[Back to Top](#table-of-contents)

---

### Get Standings

</br>

<details>
  <summary>Example:</summary>

```
get_standings()

#TODO add example response

```

</details>
</br>

[Back to Top](#table-of-contents)

---

### Get Standings Seasons

</br>

<details>
  <summary>Example:</summary>

```
get_standings_seasons()

#TODO add example response

```

</details>
</br>

[Back to Top](#table-of-contents)

---
