import urllib.request, json
import psycopg2
import boto3

ENDPOINT = "citibikenyc.clenayirevcu.us-east-1.rds.amazonaws.com"
PORT = "5432"
USER = "postgres"
REGION = "us-east-1"
DBNAME = "citibikenyc"

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


# Generates an hourly report ranking the stations based on their bikes availability (lowest availability first)
def hourly_report(stations):
    stations.sort(key=lambda x: x["num_bikes_available"] + x["num_ebikes_available"])
    # for station in stations:
    # insert into database
    # report id (maybe id from lambda) ???
    # station id
    # date
    # hour
    # bike availability

    # gets the credentials from .aws/credentials
    session = boto3.Session(profile_name="default")
    client = session.client("rds")

    token = client.generate_db_auth_token(
        DBHostname=ENDPOINT, Port=PORT, DBUsername=USER, Region=REGION
    )

    try:
        conn = psycopg2.connect(
            host=ENDPOINT,
            port=PORT,
            database=DBNAME,
            user=USER,
            password=token,
            sslrootcert="SSLCERTIFICATE",
        )
        cur = conn.cursor()
        cur.execute("""SELECT now()""")
        query_results = cur.fetchall()
        print(query_results)
    except Exception as e:
        print("Database connection failed due to {}".format(e))

    return stations


def main():
    hourly_data = pull_data()
    stations_info = hourly_data["stations_info"]
    stations_status = hourly_data["stations_status"]
    print(hourly_report(stations_status["data"]["stations"])[0:10])


if __name__ == "__main__":
    main()
