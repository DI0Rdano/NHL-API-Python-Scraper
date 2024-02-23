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

>### `https://api.nhle.com/stats/rest/en` </br>
>
>General Endpoints:
>- `/config`
>- `/country`
>- `/franchise`
>- `/season`
></br>
</br>

>### `https://api-web.nhle.com/v1` </br>
>
>Player Endpoints:
>- `/player/{playerId}`
>    - `/landing`
>    - `/game-log/{season}/{gameType}`
>
>Club Endpoints:
>- `/club-schedule/{teamAbbrev}`
>    - `/month`
>        - `/now`
>        - `/{date}`
>    - `/week`
>        - `/now`
>        - `/{date}`
>- `/club-stats-season/{teamAbbrev}`
>
>Roster Endpoints:
>- `/roster-season/{teamAbbrev}`
>- `/roster/{teamAbbrev}/{season}`
>
>Gamecenter Endpoints:
>- `/gamecenter/{gameId}`
>    - `/play-by-play`
>    - `/boxscore`
>
>Score Endpoints:
>- `/score`
>    - `/now`
>    - `/{date}`
>
>Schedule Endpoints:
>- `/schedule`
>    - `/now`
>    - `/{date}`
>- `/schedule-calendar`
>    - `/now`
>    - `/{date}`
>
>Standings Endpoints:
>- `/standings`
>- `/standings-season`
>- `/standings`
>    - `/now`
>    - `/{date}`
></br>
</br>

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

</br>

<details>
  <summary>Example:</summary>

```
get_seasons()


```

</details>
</br>

[Back to Top](#table-of-contents)

---

### Get Draft Rounds

</br>

<details>
  <summary>Example:</summary>

```
get_draftrounds()


```

</details>
</br>

[Back to Top](#table-of-contents)

---

### Get Skaters Stats

</br>

<details>
  <summary>Example:</summary>

```
get_skaters_stats()


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


```

</details>
</br>

[Back to Top](#table-of-contents)

---