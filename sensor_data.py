class Sensor(object):
    sensors = []

    def __init__(self, data, measurement, uid):
        self.readings = {}
        self.uid = uid
        self.readings.update({measurement: data})
        Sensor.sensors.append(self)

    def get_data(self):
        return [self.readings, self.uid]

    def update_data(self, data, measurement):
        self.readings.update({measurement: data})

    def get_uid(self):
        return self.uid

    @classmethod
    def get(cls, uid):
        return [inst for inst in cls.sensors if inst.uid == uid]


class SensorType(object):
    instances = []

    def __init__(self, stype, data, measurement, uid):
        self.sensorList = []
        self.stype = stype
        instance = Sensor.get(uid)

        self.update_sensor(data, measurement, uid)
        SensorType.instances.append(self)

    def get_data(self):
        data = []
        for sensor in self.sensorList:
            data.append(sensor.get_data())
        return data

    def update_sensor(self, data, measurement, uid):
        instance = Sensor.get(uid)

        if len(instance) > 0 and instance[0].get_uid() == uid:
            instance[0].update_data(data, measurement)
            # Create a new SensorType instance if there does not exist such an instance
        else:
            self.sensorList.append(Sensor(data, measurement, uid))

    def get_stype(self):
        return self.stype

    def get_list(self):
        return self.sensorList

    @classmethod
    def get(cls, stype):
        return [inst for inst in cls.instances if inst.stype == stype]


class SensorContainer:

    def __init__(self, raw):
        self.sensorTypeList = []
        self.sensorRawList = raw
        self.update_all(raw)

    def update_all(self, raw):
        for row in raw:
            if row[0] != 'Battery' and row[0] != 'Status':
                # Returns SensorType if there exists such an instance with stype = row[0]
                instance = SensorType.get(row[0])

                # Update the SensorType instance if there exists such an instance
                if len(instance) > 0 and instance[0].get_stype() == row[0]:
                    instance[0].update_sensor(row[1], row[2], row[3])
                # Create a new SensorType instance if there does not exist such an instance
                else:
                    self.sensorTypeList.append(SensorType(row[0], row[1], row[2], row[3]))

    def get_all(self):
        for element in self.sensorTypeList:
            print(str(element.get_stype()) + " : " + str(element.get_data()))