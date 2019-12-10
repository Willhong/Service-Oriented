import requests
from flask_restful import Resource, abort, reqparse

from database.resource_db_access import TemperatureResourceDatabase
from keys import KAKAO_ADMIN_KEY
from rest_client.read_kakao import KAKAO_BASE_URL


class TemperatureResource(Resource):
    def __init__(self):
        self.temperature_resource_db = TemperatureResourceDatabase()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('temperature')
        self.parser.add_argument('datetime')
        self.parser.add_argument('location')

    def get(self, sensor_id):
        headers = {"Authorization": 'KakaoAK ' + KAKAO_ADMIN_KEY}
        res1 = requests.get(
            url=KAKAO_BASE_URL + "/v3/search/book?target=authors&query=정태윤",
            headers=headers
        )
        if res1.status_code == 200:
            books = res1.json()

        else:
            books={}

        #temperature = self.temperature_resource_db.readBySensorId(sensor_id=sensor_id)
        #if temperature is None:
        #    abort(404, message="Sensor id {0} doesn't exist".format(sensor_id))
        #else:
        return books, 200

    def put(self, sensor_id):
        args = self.parser.parse_args()
        temperature = self.temperature_resource_db.readBySensorId(sensor_id=sensor_id)
        if temperature is None:
            abort(404, message="Error! Sensor id {0} doesn't exist".format(sensor_id))
        else:
            self.temperature_resource_db.update(
                sensor_id=sensor_id,
                temperature=args['temperature'],
                datetime=args['datetime'],
                location=args['location']
            )
            return {"sensor_id": sensor_id}, 200

    def delete(self, sensor_id):
        temperature = self.temperature_resource_db.readBySensorId(sensor_id=sensor_id)
        if temperature is None:
            abort(404, message="Error! Sensor id {0} doesn't exist".format(sensor_id))
        else:
            self.temperature_resource_db.delete(sensor_id=sensor_id)
            return {"sensor_id": sensor_id}, 204


class TemperatureCreationResource(Resource):
    def __init__(self):
        self.temperature_resource_db = TemperatureResourceDatabase()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('sensor_id')
        self.parser.add_argument('temperature')
        self.parser.add_argument('datetime')
        self.parser.add_argument('location')

    def post(self):
        args = self.parser.parse_args()
        sensor_id = args['sensor_id']
        temperature = self.temperature_resource_db.readBySensorId(sensor_id=sensor_id)
        if temperature is not None:
            abort(409, message="Error! Sensor id {0} already exist".format(sensor_id))
        else:
            self.temperature_resource_db.create(
                sensor_id=sensor_id,
                temperature=args['temperature'],
                datetime=args['datetime'],
                location=args['location']
            )
            return {"sensor_id": sensor_id}, 201


class TemperatureByLocationResource(Resource):
    def __init__(self):
        self.temperature_resource_db = TemperatureResourceDatabase()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('temperature')
        self.parser.add_argument('datetime')
        self.parser.add_argument('location')

    def get(self, location):
        temperature = self.temperature_resource_db.readByLocation(location=location)
        if temperature is None:
            abort(404, message="The sensor where the location includes {0} doesn't exist".format(location))
        else:
            return temperature, 200

class DiscomfortIndexResource(Resource):
    def __init__(self):
        self.temperature_resource_db=TemperatureResourceDatabase()

    def get(self):
        pass