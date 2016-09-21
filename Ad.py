import json


class Ad(object):
    url = ""
    id = 0
    latitude = 0
    longitude = 0
    title = ""
    price = ""
    town = ""
    district = ""
    flatSize = ""
    roomCount = ""
    floor = ""
    heating = ""
    isFull = ""
    subscription = ""

    def Ad(self):
        pass

    def __str__(self):
        return self.id + "," + self.latitude + "," + self.longitude + "," + self.title + "," + self.price + "," + self.town\
               + "," + self.district + "," + self.flatSize + "," + self.roomCount + "," + self.floor + "," + self.heating \
               + "," + self.isFull + "," + self.subscription

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, ensure_ascii=False)