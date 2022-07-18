class SensorContainer:
    """ SensorContainer class containing all the SensorType instances
    Pass raw data from InfluxDB last() into this class object
    """

    def __init__(self, raw):
        """ Initialize SensorContainer class. """
        self.sensorTypeList = []
        self.sensorRawList = raw
        self.update_all(raw)

    def update_all(self, raw):
        """ Update all the SensorType instances in the container. """
        for row in raw:
            stype = row[0]
            value = row[1]
            field = row[2]
            uid = row[3]
            # Change or remove stype filters as necessary
            if stype != 'Battery' and stype != 'Status':
                # Returns SensorType if there exists such an instance with stype
                instance = _SensorType.find(stype)
                # Update the SensorType instance if there exists such an instance
                if len(instance) > 0 and instance[0].get_stype() == stype:
                    instance[0].update_sensor(value, field, uid)
                # Create a new SensorType instance if there does not exist such an instance
                else:
                    self.sensorTypeList.append(_SensorType(stype, value, field, uid))

            elif stype == 'Status' or stype == 'Battery':
                instance = _Sensor.find(uid)
                if len(instance) > 0:
                    instance[0].update_data(value, field)

    def get_all(self):
        """ Return all the SensorType instances in the container. """
        container_data = {}
        for element in self.sensorTypeList:
            container_data.update({element.get_stype(): element.get_sensor_data()})
        return container_data


class _SensorType(object):
    """ Internal SensorType class containing all the sensors of the same sensor type (stype)
    Constructor should be called if classmethod find(stype) does not return any
    instances of SensorType stype
    """
    instances = [] # List to store all the instances of SensorType

    def __init__(self, stype, data, measurement, uid):
        self.sensorList = []
        self.stype = stype
        instance = _Sensor.find(uid)

        self.update_sensor(data, measurement, uid)
        _SensorType.instances.append(self)

    def get_sensor_data(self):
        data = {}
        for sensor in self.sensorList:
            data.update(sensor.get_data())
        return data

    def update_sensor(self, data, measurement, uid):
        instance = _Sensor.find(uid)

        if len(instance) > 0 and instance[0].get_uid() == uid:
            instance[0].update_data(data, measurement)
            # Create a new SensorType instance if there does not exist such an instance
        else:
            self.sensorList.append(_Sensor(data, measurement, uid))

    def get_stype(self):
        return self.stype

    def get_list(self):
        return self.sensorList

    @classmethod
    def find(cls, stype):
        return [inst for inst in cls.instances if inst.stype == stype]


class _Sensor(object):
    """ Internal Sensor class containing all the data for a sensor in key-value pairs
    Constructor should be called if classmethod find(uid) does not return any
    instances of Sensor uid.
    """
    sensors = [] # List to store all the instances of Sensor

    def __init__(self, data, measurement, uid):
        self.readings = {}
        self.uid = uid
        self.readings.update({measurement: data})
        _Sensor.sensors.append(self)

    def get_data(self):
        return {self.uid: self.readings}

    def update_data(self, data, measurement):
        self.readings.update({measurement: data})

    def get_uid(self):
        return self.uid

    @classmethod
    def find(cls, uid):
        return [inst for inst in cls.sensors if inst.uid == uid]
