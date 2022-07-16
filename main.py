import sched
import time
import influxdb_client
from sensor_data import SensorContainer

# Initialize InfluxDB client
bucket = "████████████████"
org = "████████████████"
token = "████████████████"
# Store the URL of your InfluxDB instance
url = "████████████████"
client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)
query = ' from(bucket: "████████████████")\
  |> range(start: -1h)\
  |> last()'

s = sched.scheduler(time.time, time.sleep)


def main_task(sc):
    query_api = client.query_api()
    result = query_api.query(org=org, query=query)
    results = []
    for table in result:
        for record in table.records:
            results.append((record.get_measurement(),
            record.get_value(), record.get_field(), record["UID"]))
    # Create a new SensorType object
    container.update_all(results)
    container.get_all()
    sc.enter(2, 1, main_task, (sc,))


container = SensorContainer([])
s.enter(2, 1, main_task, (s,))
s.run()
