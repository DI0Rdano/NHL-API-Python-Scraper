# NHL API Scraper Documentation

Documentation for the [NHL API Python Scraper](https://github.com/DI0Rdano/NHL-API-Python-Scraper/blob/main/nhlAPI.py). </br>

**NHL API Python Scraper** </br>
Python based scraping functions for various NHL API endpoints. Configured to the work with the new NHL API. </br>
Constructed for personal use, not intended to be comprehensive. </br>

Work in progress.

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
>[get_stats](#get-stats) </br>

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

### `https://search.d3.nhle.com/api/v1` </br>

  Search Endpoints:
  - `/search`
    - `/player` Note: requires `?culture=en-us` modifier to work.

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

### Parameters:
- `playerId` e.g., '8479318' for Auston Matthews.
- `season` e.g., '20232024'.
- `gameType` Range from 1-4. '2' for regular season, '3' for playoffs.
- `teamAbbrev` 3 letter abbreviation of the team e.g., 'TOR' for the Toronto Maple Leafs.
- `date` Date in the format of 'YYYY-MM-DD'.
- `gameId`

</br>

[Back to Top](#table-of-contents)

## Modifiers

Introduce modifiers by adding a `?` suffix to the url. Combine multiple modifiers with `&`.
- `include=`
    - To include parameters not in the response or to filter the response. 
- `sort=`
    - To specify the sort direction, use the following structure. `[{"property": , "direction": }]` </br>
    Sort multiple parameters by adding to the list. Valid sort directions include 'ASC' and 'DESC'. </br>
    Example: `sort=[{"property": "points", "direction": "DESC"}, {"property": "playerId", "direction": "ASC"}]`
- `cayenneExp=`
    - To specify the cayenneExp parameters, use the following structure. `{parameter}={value}` </br>
    Use ' and ' to join together multiple parameters. <br>
    Example: `cayenneExp=seasonId=20232024 and gameTypeId=2`
- `factCayenneExp=`
    - To specify the factCayenneExp parameters, use the following structure. `{parameter}{comparator}{value}` </br>
    Valid comparators include '>=', '=', and '<='. Use ' and ' to join together multiple parameters. <br>
    Example: `factCayenneExp=gamesPlayed>=0 and gamesPlayed<=10` </br>
    Note: factCayenneExp must be included before cayenneExp to work properly.
</br>

[Back to Top](#table-of-contents)

## Python Scraper

### Get Config
Fetch data from the NHL API 'config' endpoint. Returns valid fields for skaters, goalies, and teams stats endpoints.

`get_config(view=None, input_validation=True)`

Parameters:
- `view` (str, optional): The part of the JSON to return, use '.' as a delimiter for subfields. Default is None (returns everything).
- `input_validation` (bool): Flag to enable/disable input validation. Default is 'True'.

Returns:
- `dict`: Configuration data as a JSON dictionary based on the specified view.
    </br>
    <details>
      <summary>Example</summary>

    ```
    get_config()

    {
      "playerReportData": {
        "summary": {
          "game": {
            "displayItems": [
              "playerId",
              "skaterFullName",
              "gameId",
              "opponentTeamAbbrev",
              "gameDate",
              ...
            ],
            "resultFilters": [
              "gamesPlayed",
              "goals",
              "assists",
              "points",
              ...
            ],
            "sortKeys": [
              "points",
              "goals",
              "assists"
            ]
          },
          "season": {...}
        },
        "realtime": {...},
        "penalties": {...},
        "shootout": {...},
        "bios": {...},
        "shottype": {...},
        ...
      },
      "goalieReportData": {...},
      "teamReportData": {...},
      "aggregatedColumns": [...],
      "individualColumns": [...]
    }

    ```
    </details>
    </br>
- `None`: In case of an error.

</br>

[Back to Top](#table-of-contents)

---

### Get Countries
Fetch data from the NHL API 'country' endpoint.

`get_countries(include_stateProvinces=True, sort="countryName", direction="ASC", filter=None, input_validation=True)`

Parameters:
- `include_stateProvinces` (bool): Whether to include state provinces in the response. Default is 'True'.
- `sort` (str, optional): Field to sort the countries by. Default is 'countryName'.
- `direction` (str): Sort direction ('ASC' for ascending, 'DESC' for descending). Default is 'ASC'.
- `filter` (str or list, optional): The fields to include in the json response. Default is 'None' which returns all fields.
- `input_validation` (bool): Flag to enable/disable input validation. Default is 'True'.

Returns:
- `dict`: country data as a json dictionary.
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

- `None`: In case of an error.

</br>

[Back to Top](#table-of-contents)

---


### Get Seasons
Fetch data from the NHL API 'season' endpoint.

`get_seasons(sort="id", direction="DESC", filter=None, input_validation=True)`

Parameters:
- `sort` (str or list, optional): Field to sort the seasons by. Default is 'id'. Valid values are 'id' and other fields present in the NHL API response.
- `direction` (str or list): Direction of sorting. Default is 'DESC'. Valid values are 'ASC' (ascending) and 'DESC' (descending).
- `filter` (str or list, optional): The fields to include in the json response. Default is 'None' which returns all fields.
- `input_validation` (bool): Flag to enable/disable input validation. Default is 'True'.

Returns:
- `dict`: Season data as a JSON dictionary.
  </br>
  <details>
    <summary>Example</summary>

  ```
  get_seasons()

  {
    "data": [
      {
        "id": 20232024,
        "allStarGameInUse": 1,
        "conferencesInUse": 1,
        "divisionsInUse": 1,
        "endDate": "2024-06-18T00:00:00",
        "entryDraftInUse": 1,
        "formattedSeasonId": "2023-24",
        "minimumPlayoffMinutesForGoalieStatsLeaders": 30,
        "minimumRegularGamesForGoalieStatsLeaders": 19,
        "nhlStanleyCupOwner": 1,
        "numberOfGames": 82,
        "olympicsParticipation": 0,
        "pointForOTLossInUse": 1,
        "preseasonStartdate": "2023-09-23T00:05:00",
        "regularSeasonEndDate": "2024-04-18T22:30:00",
        "rowInUse": 1,
        "seasonOrdinal": 106,
        "startDate": "2023-10-10T17:30:00",
        "supplementalDraftInUse": 0,
        "tiesInUse": 0,
        "totalPlayoffGames": 0,
        "totalRegularSeasonGames": 1312,
        "wildcardInUse": 1
      },
      {
        "id": 20222023,
        "allStarGameInUse": 1,
        "conferencesInUse": 1,
        "divisionsInUse": 1,
        "endDate": "2023-06-13T17:00:00",
        ...
      },
      ...
    ],
    "total": 106
  }

  ```
  </details>
  </br>

- `None`: In case of an error.

</br>

[Back to Top](#table-of-contents)

---

### Get Draft Rounds
Fetch data from the NHL API 'draft' endpoint.

`get_draftrounds(sort="draftYear", direction="DESC", filter=None, input_validation=True)`

Parameters:
- `sort` (str or list, optional): Field to sort the draft rounds by. Default is 'draftYear'.
- `direction` (str or list): Direction of sorting. Default is 'DESC'.
- `filter` (str or list, optional): The fields to include in the json response. Default is 'None' which returns all fields.
- `input_validation` (bool): Flag to enable/disable input validation. Default is 'True'.

Returns:
- `dict`: Draft round data as a json dictionary.

    <details>
      <summary>Example</summary>

    ```
    get_draftrounds()

    {
      "data": [
        {
          "id": 62,
          "draftYear": 2023,
          "rounds": 7
        },
        {
          "id": 61,
          "draftYear": 2023,
          "rounds": 1
        },
        ...
      ],
      "total": 62
    }

    ```

    </details>
      </br>

- `None`: In case of an error.

  </br>

[Back to Top](#table-of-contents)

---

### Get Stats
Fetch data from the NHL API 'stats' endpoint for a season, a range of seasons, or a range of dates.

`get_stats(key="skater", **kwargs)`

</br>

**Parameters:** </br>

- `key` (str): The stats to return ('skater', 'goalie', 'team'). Default is 'skater'.

For a season (default)

- `season` (str, optional): The season to return the stats from (e.g., '20232024'). </br>

For range of seasons

- `start_season` (str, optional): The starting season of the range (e.g., '19992000'). Default is 'None'.
- `end_season` (str, optional): The ending season of the range (e.g., '20232024'). Default is 'None'.

For range of dates

- `start_date` (str, optional): The starting date of the range (YYYY-MM-DD). Default is 'None'.
- `end_date` (str, optional): The ending date of the range (YYYY-MM-DD). Default is 'None'.

</br>

**Additional Parameters:**

- `report` (str): The report type to return. Available report types can be found in the config. Default is 'summary'.
- `franchise_id` (int): The franchise identifier to return the stats from. Default is 'None' which returns all franchises.
- `opponent_franchise_id` (int): The opponent franchise identifier to return the stats from. Default is 'None' which returns all opponent franchises.
- `home_or_road` (str): The stats from home or away games ('H' for home, 'R' for road/away).  Default is 'None' which returns all games.
- `game_result` (str): The stats from games with the provided result ('W' for wins, 'L' for losses, and 'O' for overtime losses). Default is 'None' which returns all game results.
- `game_type` (int): The type of game ('1' for pre-season, '2' for regular season, '3' for playoffs, '4' for all-star games). Default is '2'.
- `min_gp` (int): The minimum number of games played. Default is '0'.
- `max_gp` (int): The maximum number of games played. Default is 'None'.
- `position` (str or list): The positions of the skaters. Default is 'None' which returns all positions.
- `shoots_catches` (str): The handedness of the players to return the stats from ('L' for left, 'R' for right). Default is 'None' which returns all players.
- `player_name` (str): The full name of the player to filter. Default is 'None' which returns all players.
- `nationality_code` (str): The nationlity code of the players to return the stats from (e.g., 'CAN'). Default is 'None' which returns all nationalities.
- `birth_state_province_code` (str): The birth state province code of the players to return the stats from (e.g., 'ON'). Default is 'None' which returns all birth state provinces.
- `draft_round` (str or int): The draft round of the players to return the stats from. Default is 'None' which returns all rounds.
- `draft_year` (str or int): The draft year of the players to return the stats from (e.g., '2012'). Note: if no draft round is input, returns from first round, and only returns data for a single draft round. Default is 'None' which returns all draft years.
- `is_rookie` (bool): Whether the players are a rookie (True to return rookies, False to exclude rookies / return veterans). Default is 'None' which returns all players.
- `is_active` (bool): Whether the players are active (True to return active skaters, False to return incactive skaters). Default is 'None' which returns all players.
- `is_in_hall_of_fame` (bool): Wether the players are in the hall of fame. Default is 'None' which returns all players.
- `is_game` (bool): The flag for providing a range of dates. Default is 'False'.
- `property` (str or list): The property to filter by (note: works alongside a provided comparator and value). Default is 'None'.
- `comparator` (str or list): The comparator to filter by ('>=', '=', and '<=') (note: works alongside a provided comparator and value). Default is 'None'.
- `value` (str or int or list): The value to filter by (note: works alongside a provided comparator and value). Default is 'None'.
- `sort` (str or list): The sort field(s) for the query. Can be a single string or a list of strings. 'None' returns skaters with no sorting.
- `direction` (str or list): The sort direction(s) for the query. Can be a single string or a list of strings.
- `limit` (int): The max number of players/teams to return if return_all is set to 'False'.  Default is '100'.
- `start` (int): The starting point of the list to return the skaters from if return_all is set to 'False'. Default is '0'.
- `return_all` (bool): Flag to determine whether to return all skaters or only a single loop of skaters with the provided limit. Default is 'True'.
- `aggregate` (bool): Boolean option to aggregate skaters stats over multiple seasons or games. Default is 'True'.
- `input_validation` (bool): Flag to enable/disable input validation. Default is 'True'.

</br>

**Returns:**
- `list`: List of dictionaries containing skater(s) season stats.
    </br>
    <details>
      <summary>Example for skater stats from a season</summary>

    ```
    get_stats(key="skater", season="20222023")

    [
      0:{
        "assists":89
        "evGoals":39
        "evPoints":75
        "faceoffWinPct":0.51928
        "gameWinningGoals":11
        "gamesPlayed":82
        "goals":64
        "lastName":"McDavid"
        "otGoals":2
        "penaltyMinutes":36
        "playerId":8478402
        "plusMinus":22
        "points":153
        "pointsPerGame":1.86585
        "positionCode":"C"
        "ppGoals":21
        "ppPoints":71
        "shGoals":4
        "shPoints":7
        "shootingPct":0.18181
        "shootsCatches":"L"
        "shots":352
        "skaterFullName":"Connor McDavid"
        "timeOnIcePerGame":1343.1341
      }
      1:{
        "assists":76
        "evGoals":19
        "evPoints":64
        "faceoffWinPct":0.54897
        "gameWinningGoals":11
        "gamesPlayed":80
        "goals":52
        "lastName":"Draisaitl"
        "otGoals":1
        "penaltyMinutes":24
        "playerId":8477934
        "plusMinus":7
        "points":128
        "pointsPerGame":1.6
        "positionCode":"C"
        "ppGoals":32
        "ppPoints":62
        "shGoals":1
        "shPoints":2
        "shootingPct":0.21052
        "shootsCatches":"L"
        "shots":247
        "skaterFullName":"Leon Draisaitl"
        "timeOnIcePerGame":1304.0375
      }
      ...
    ]

    ```

    </details>
    <details>
      <summary>Example for goalie stats for a range of seasons</summary>

    ```
    get_stats(key="goalie", start_season="19992000", end_season="20222023")

    [
      0:{
        "assists":31
        "gamesPlayed":891
        "gamesStarted":885
        "goalieFullName":"Martin Brodeur"
        "goals":2
        "goalsAgainst":1992
        "goalsAgainstAverage":2.26313
        "lastName":"Brodeur"
        "losses":292
        "otLosses":49
        "penaltyMinutes":90
        "playerId":8455710
        "points":33
        "savePct":0.91183
        "saves":20602
        "shootsCatches":"L"
        "shotsAgainst":22594
        "shutouts":89
        "ties":48
        "timeOnIce":3168696
        "wins":490
      }
      1:{
        "assists":28
        "gamesPlayed":649
        "gamesStarted":619
        "goalieFullName":"Kari Lehtonen"
        "goals":0
        "goalsAgainst":1662
        "goalsAgainstAverage":2.70698
        "lastName":"Lehtonen"
        "losses":233
        "otLosses":67
        "penaltyMinutes":42
        "playerId":8470140
        "points":28
        "savePct":0.91215
        "saves":17258
        "shootsCatches":"L"
        "shotsAgainst":18920
        "shutouts":38
        "ties":0
        "timeOnIce":2210278
        "wins":310
      }
      ...
    ]

    ```

    </details>

    <details>
      <summary>Example for team stats for a range of dates</summary>

    ```
    get_stats(key="team", start_date="2000-10-30", end_date="2023-02-10")

    [
      0:{
        "faceoffWinPct":0.516528
        "franchiseId":6
        "franchiseName":"Boston Bruins"
        "gamesPlayed":1690
        "goalsAgainst":4331
        "goalsAgainstPerGame":2.56272
        "goalsFor":4924
        "goalsForPerGame":2.9136
        "losses":538
        "otLosses":194
        "penaltyKillNetPct":0.860911
        "penaltyKillPct":0.832774
        "pointPct":0.61272
        "points":2071
        "powerPlayNetPct":0.164061
        "powerPlayPct":0.190173
        "regulationAndOtWins":847
        "shotsAgainstPerGame":29.39408
        "shotsForPerGame":31.75857
        "ties":39
        "wins":919
        "winsInRegulation":740
        "winsInShootout":72
      }
      1:{
        "faceoffWinPct":0.501734
        "franchiseId":24
        "franchiseName":"Washington Capitals"
        "gamesPlayed":1691
        "goalsAgainst":4753
        "goalsAgainstPerGame":2.81076
        "goalsFor":5074
        "goalsForPerGame":3.00059
        "losses":580
        "otLosses":178
        "penaltyKillNetPct":0.832723
        "penaltyKillPct":0.814273
        "pointPct":0.59402
        "points":2009
        "powerPlayNetPct":0.176797
        "powerPlayPct":0.203921
        "regulationAndOtWins":824
        "shotsAgainstPerGame":30.26788
        "shotsForPerGame":29.7327
        "ties":35
        "wins":898
        "winsInRegulation":708
        "winsInShootout":74
      }
      ...
    ]

    ```

    </details>
    </br>
- `None`: In case of an error.

</br>

[Back to Top](#table-of-contents)

---

### Get Players

Fetch data from the NHL API 'players' endpoint.

`get_players(player_limit=None, is_active=None, input_validation=True)`

Parameters:
  - `is_active` (bool, optional): Whether the players are active (True to return active players, False to return incactive players). Default is 'None' which returns all players.
  - `player_limit` (int, optional): The max number of players to return.  Default is 'None'. There are approximately '2184' active players, and '19986' inactive players.
  - `input_validation` (bool): Flag to enable/disable input validation. Default is 'True'.

  Returns:
  - `dict`: Player data as a json dictionary.
    </br>
    <details>
      <summary>Example</summary>

    ```
    get_players()

    [
      0:{
        "playerId":"8447135"
        "name":"Gord Kannegiesser"
        "positionCode":"D"
        "teamId":NULL
        "teamAbbrev":NULL
        "lastTeamId":NULL
        "lastTeamAbbrev":NULL
        "lastSeasonId":"19711972"
        "sweaterNumber":22
        "active":false
        "height":"6'0""
        "heightInCentimeters":183
        "weightInPounds":190
        "weightInKilograms":86
        "birthCity":"North Bay"
        "birthStateProvince":"Ontario"
        "birthCountry":"CAN"
      }
      1:{
        "playerId":"8482646"
        "name":"Brennan Kapcheck"
        "positionCode":"D"
        "teamId":NULL
        "teamAbbrev":NULL
        "lastTeamId":NULL
        "lastTeamAbbrev":NULL
        "lastSeasonId":NULL
        "sweaterNumber":NULL
        "active":false
        "height":"5'9""
        "heightInCentimeters":175
        "weightInPounds":161
        "weightInKilograms":72
        "birthCity":"Mt. Prospect"
        "birthStateProvince":"Illinois"
        "birthCountry":"USA"
      }
      ...
    ]

    ```

    </details>
    </br>

  - `None`: In case of an error.

</br>

[Back to Top](#table-of-contents)

---

### Get Player Landing

Fetch data from the NHL API 'player/landing' endpoint.

`get_player_landing(player_id, view=None, input_validation=True)`

Parameters:
  - `player_id` (int): The ID of the player.
  - `view` (str, optional): The part of the json to return, use '.' as a delimiter for subfields. Default is None (to return everything).
  - `input_validation` (bool): Flag to enable/disable input validation. Default is True.

  Returns:
  - `dict`: Player landing data as a json dictionary.
    </br>

    <details>
      <summary>Example</summary>

    ```
    get_player_landing(player_id=8479318)

    {
      "playerId": 8479318,
      "isActive": true,
      "currentTeamId": 10,
      "currentTeamAbbrev": "TOR",
      "fullTeamName": {
        "default": "Toronto Maple Leafs",
        "fr": "Maple Leafs de Toronto"
      },
      "firstName": {
        "default": "Auston"
      },
      "lastName": {
        "default": "Matthews"
      },
      "teamLogo": "https://assets.nhle.com/logos/nhl/svg/TOR_light.svg",
      "sweaterNumber": 34,
      "position": "C",
      "headshot": "https://assets.nhle.com/mugs/nhl/20232024/TOR/8479318.png",
      "heroImage": "https://assets.nhle.com/mugs/actionshots/1296x729/8479318.jpg",
      "heightInInches": 75,
      "heightInCentimeters": 191,
      "weightInPounds": 215,
      "weightInKilograms": 98,
      "birthDate": "1997-09-17",
      "birthCity": {
        "default": "San Ramon"
      },
      "birthStateProvince": {
        "default": "California",
        ...
      },
      "birthCountry": "USA",
      "shootsCatches": "L",
      "draftDetails": {
        "year": 2016,
        "teamAbbrev": "TOR",
        ...
      },
      "playerSlug": "auston-matthews-8479318",
      "inTop100AllTime": 0,
      "inHHOF": 0,
      "featuredStats": {
        "season": 20232024,
        "regularSeason": {
          "subSeason": {
            "gamesPlayed": 56,
            "goals": 52,
            "assists": 25,
            "points": 77,
            ...
          },
          "career": {
            "gamesPlayed": 537,
            "goals": 351,
            "assists": 268,
            "points": 619,
            ...
          }
        }
      },
      "careerTotals": {
        "regularSeason": {
          "gamesPlayed": 537,
          "goals": 351,
          "assists": 268,
          ...
        },
        "playoffs": {
          "gamesPlayed": 50,
          "goals": 22,
          "assists": 22,
          ...
        }
      },
      "shopLink": "#TODO",
      "twitterLink": "#TODO",
      "watchLink": "#TODO",
      "last5Games": [
        {
          "assists": 1,
          "gameDate": "2024-02-24",
          "gameId": 2023020908,
          "gameTypeId": 2,
          "goals": 0,
          ...
        },
        ...
      ],
      "seasonTotals": [
        {
          "gameTypeId": 2,
          "gamesPlayed": 3,
          "leagueAbbrev": "QC Int PW",
          "points": 6,
          "season": 20092010,
          "sequence": 173362,
          "teamName": {
            "default": "Druzhba-78 Kharkov"
          }
        },
        ...
      ],
      "awards": [
        {
          "trophy": {
            "default": "Calder Memorial Trophy",
            "fr": "Trophée Calder"
          },
          "seasons": [
            {
              "seasonId": 20162017,
              "gamesPlayed": 82,
              "gameTypeId": 2,
              "goals": 40,
              "assists": 29,
              ...
            }
          ]
        },
        ...
      ],
      "currentTeamRoster": [
        {
          "playerId": 8481122,
          "lastName": {
            "default": "Benoit"
          },
          "firstName": {
            "default": "Simon"
          },
          "playerSlug": "simon-benoit-8481122"
        },
        ...
      ]
    }

    ```

    </details>
    </br>

  - `None`: In case of an error.

</br>

[Back to Top](#table-of-contents)

---

### Get Player Gamelog

Fetch data from the NHL API player 'gamelog' endpoint.

`get_player_gamelog(player_id, season, game_type=2, view="gameLog", input_validation=True)`

Parameters:
  - `player_id` (int): The ID of the player.
  - `season` (str): The season to return the gamelog from, (ex. '20232024').
  - `game_type` (int): The type of game (2 for regular season, 3 for playoffs). Default is '2'.
  - `view` (str, optional): The part of the json to return, use '.' as a delimiter for subfields. Default is 'gameLog'.
  - `input_validation` (bool): Flag to enable/disable input validation. Default is 'True'.

  Returns:
  - `dict`: Player gamelog data as a json dictionary based on the specified view.
    </br>
    <details>
      <summary>Example</summary>

    ```
    get_player_gamelog(player_id=8479318, season="20212022")

    [
      0:{
        "gameId":2021020829
        "teamAbbrev":"TOR"
        "homeRoadFlag":"H"
        "gameDate":"2022-04-26"
        "goals":2
        "assists":0
        "commonName":{
          "default":"Maple Leafs"
        }
        "opponentCommonName":{
          "default":"Red Wings"
        }
        "points":2
        "plusMinus":1
        "powerPlayGoals":1
        "powerPlayPoints":1
        "gameWinningGoals":1
        "otGoals":0
        "shots":7
        "shifts":19
        "shorthandedGoals":0
        "shorthandedPoints":0
        "pim":0
        "toi":"19:21"
        "opponentAbbrev":"DET"
      }
      1:{
        "gameId":2021021265
        "teamAbbrev":"TOR"
        "homeRoadFlag":"R"
        "gameDate":"2022-04-24"
        "goals":0
        "assists":2
        "commonName":{
          "default":"Maple Leafs"
        }
        "opponentCommonName":{
          "default":"Capitals" 
        }
        "points":2
        "plusMinus":1
        "powerPlayGoals":0
        "powerPlayPoints":0
        "gameWinningGoals":0
        "otGoals":0
        "shots":4
        "shifts":28
        "shorthandedGoals":0
        "shorthandedPoints":0
        "pim":0
        "toi":"25:19"
        "opponentAbbrev":"WSH"
      }
      ...
    ]

    ```

    </details>
    </br>

  - `None`: In case of an error.


[Back to Top](#table-of-contents)

---

### Get Franchises
Fetch data from the NHL API 'franchise' endpoint.

`get_franchises(include_firstSeason=True, include_lastSeason=True, sort="fullName", direction="ASC", filter=None, input_validation=True)`

Parameters:
- `include_firstSeason` (bool): Whether to include first season information. Default is True.
- `include_lastSeason` (bool): Whether to include last season information. Default is True.
- `sort` (str, optional): Field to sort the franchises by. Default is "fullName". Valid values are "fullName", "teamCommonName", "teamPlaceName", and "id".
- `direction` (str): Sort direction. Default is "ASC".
- `filter` (str or list, optional): The fields to include in the json response. Default is 'None' which returns all fields.
- `input_validation` (bool): Flag to enable/disable input validation. Default is True.

Returns:
- `dict`: Franchise data as a JSON dictionary.
  </br>
  <details>
    <summary>Example</summary>

  ```
  get_franchises()

  #TODO add example response

  ```

  </details>
  </br>

- `None`: In case of an error.

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
  <summary>Example</summary>

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
  <summary>Example</summary>

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
  <summary>Example</summary>

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
  <summary>Example</summary>

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
  <summary>Example</summary>

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
  <summary>Example</summary>

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
  <summary>Example</summary>

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
  <summary>Example</summary>

```
get_standings_seasons()

#TODO add example response

```

</details>
</br>

[Back to Top](#table-of-contents)

---
