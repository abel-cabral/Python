class FakeSensor(object):
    def __init__(self, sensorType = "", metric = 0, time = 0, message = "", status = False, id = ""):
        self.sensorType = sensorType
        self.metric = metric
        self.time = time
        self.message = message
        self.status = status
        self.id = id