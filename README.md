# NHL API Python Scraper

Python based scraping functions for various NHL API endpoints. Configured to the work with the new NHL API. </br>
Constructed for personal use, not intended to be comprehensive. </br>

MIT License [2024] </br>

Follow [@DI0Rdano](https://twitter.com/DI0Rdano) on Twitter/X

## Table of Contents

[Base URLs & Endpoints](#base-urls--endpoints)

[Modifiers](#modifiers)

[Python Scraper](#python-scraper)

* [make_api_request](#make-api-request)

* [get_countries](#get-countries)

* [get_franchises](#get-franchises)

* [get_seasons](#get-seasons)

* [get_draftrounds](#get-draft-rounds)

* [get_roster](#get-roster)

* [get_roster_seasons](#get-roster-seasons)

* [get_skaters_stats](#get-skaters-stats)

* [get_schedule_calendar](#get-schedule-calendar)

## Base URLs & Endpoints

Base URL: `https://api.nhle.com/stats/rest/en`
- `/config`
- `/country`
- `/franchise`
- `/season`
</br>
</br>


Base URL: `https://api-web.nhle.com/v1/`
- `/player/{playerId}`
    - `/landing`
    - `game-log/{season}/{game_type}`
- `/standings`
- `/standings-season`
- `/club-stats-season/{teamAbbrev}`
- `/roster-season/{teamAbbrev}`
</br>

[Back to Top](#table-of-contents)

## Modifiers

Introduce modifiers by adding a `?` suffix to the url. Combine multiple modifiers with `&`.
- `include=`
- `sort=`
    - To specify the sort direction, use the following structure.
</br>

[Back to Top](#table-of-contents)

## Python Scraper

### Make API Request
Make a request to the API and handle retries and error conditions.

`make_api_request(url, timeout=10, retries=3, input_validation=True)`

Parameters:
- url (str): The URL to make the API request to.
- timeout (int): The timeout duration for the request in seconds. Default is 10.
- retries (int): The number of retry attempts in case of failure. Default is 3.
- input_validation (bool): Flag to enable/disable input validation. Default is True.

Returns:
- dict or None: The JSON response from the API or None in case of error.
</br>

[Back to Top](#table-of-contents)

---

### Get Config
Fetch data from the NHL API 'config' endpoint.

`get_config(view=None)`

Parameters:
- view (str, optional): The part of the JSON to return. Default is None (returns everything). </br> Allowed views are 'playerReportData', 'goalieReportData', 'teamReportData', 'aggregatedColumns', 'individualColumns'.

Returns:
- dict: Configuration data as a JSON dictionary based on the specified view.
- None: In case of an error.
</br>

[Back to Top](#table-of-contents)

---

### Get Countries

</br>

[Back to Top](#table-of-contents)

---

### Get Franchises

</br>

[Back to Top](#table-of-contents)

---

### Get Seasons

</br>

[Back to Top](#table-of-contents)

---

### Get Draft Rounds

</br>

[Back to Top](#table-of-contents)

---

### Get Roster

</br>

[Back to Top](#table-of-contents)

---

### Get Roster Seasons

</br>

[Back to Top](#table-of-contents)

---

### Get Skaters Stats

</br>

[Back to Top](#table-of-contents)

---

### Get Schedule Calendar

</br>

[Back to Top](#table-of-contents)

---
