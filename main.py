# This script is used to transpose the last data entry from InfluxDB to Firebase RTDB
# update_frequency is the time in seconds between each update

import sched
import time
import influxdb_client
from transposer import SensorContainer
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

update_frequency = 5

# Initialize InfluxDB client
bucket = ""
org = ""
token = ""
# Store the URL of your InfluxDB instance
url = ""
client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)
query = ' from(bucket: "")\
  |> range(start: -1h)\
  |> last()'

# Initialize Firebase Admin SDK
cred = credentials.Certificate('firebase-adminsdk-key.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': ''
})

s = sched.scheduler(time.time, time.sleep)


def main_task(sc):
    query_api = client.query_api()
    result = query_api.query(org=org, query=query)
    results = []
    for table in result:
        for record in table.records:
            results.append((record.get_measurement(), record.get_value(), record.get_field(), record["UID"]))
    # Update the SensorContainer with the latest data
    container.update_all(results)
    out = container.get_all()
    # Write the data to Firebase
    db.reference("/").update(out)

    # Schedule the next update
    sc.enter(update_frequency, 1, main_task, (sc,))


# Initialize the SensorContainer
container = SensorContainer([])
s.enter(update_frequency, 1, main_task, (s,))
s.run()
