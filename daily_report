import urllib.request, json

# Grabs the latest data from citibikenyc.com to use for the next hourly report.
def pull_data():
    with urllib.request.urlopen(
        "https://gbfs.citibikenyc.com/gbfs/en/station_information.json"
    ) as stations_info_url:
        stations_info = json.load(stations_info_url)

    with urllib.request.urlopen(
        "https://gbfs.citibikenyc.com/gbfs/en/station_status.json"
    ) as stations_status_url:
        stations_status = json.load(stations_status_url)

    return {"stations_info": stations_info, "stations_status": stations_status}


# Generates a daily report for each station, provide the hour of the day for their lowest and highest bike availability
# def daily_report():
#     get data from database about the last 24 hours split by station id
#     for each station
#         find highest avail hour
#         find lowest avail hour
