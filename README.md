# WMNS TRANSPOSER

Python script to transpose InfluxDB time-series data to Firebase RTDB.

## Usage

Import transposer

```python
from transposer import SensorContainer
```

Takes in the returned results from a flux "|> last()" query in the form of a list _results_
with fluxrecord elements _measurement, _value, _field and a user-defined id value.

```python
for record in table.records:
    results.append((record.get_measurement(), record.get_value(), record.get_field(), record["UID"]))
```

Pass the list into SensorContainer.
```python
container = SensorContainer(results)
```

The data will be structured in a json serializable format:
```
SensorContainer
|
└───_SensorType (_measurement)
│   │
│   └───_Sensor (user-defined id value)
│   |   │   {_field : _value}
│   |   │   {_field : _value}
│   |   │   ...
|   |    ...
│   
└───_SensorType (_measurement)
|    │
|    └───_Sensor (user-defined id value)
|    │   |   ...
|    └───_Sensor (user-defined id value)
|    │   |   ...
|   ...
...
```

Update SensorContainer. Adds new and overwrites existing. Deletions not supported.
```python
container.update_all(results)
```


Get the above structure as dict
```python
out = container.get_all()
```


Part of [WMNS](https://github.com/edward62740/Wireless-Mesh-Network-System).

