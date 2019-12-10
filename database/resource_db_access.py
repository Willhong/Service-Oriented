import sqlite3

insertion_resource = """
    INSERT INTO TEMPERATURE VALUES (null, ?, ?, ?, ?);
"""

selection_resource_by_sensor_id = """
    SELECT * FROM TEMPERATURE WHERE sensor_id=?
"""

selection_resource_by_location = """
    SELECT * FROM TEMPERATURE WHERE location LIKE ?
"""

update_resource_by_sensor_id = """
    UPDATE TEMPERATURE SET temperature=?, datetime=?, location=? WHERE sensor_id=?
"""

delete_resource_by_sensor_id = """
    DELETE FROM TEMPERATURE WHERE sensor_id = ?
"""


class TemperatureResourceDatabase:
    def __init__(self):
        self.conn = sqlite3.connect('database/database_sql.db')

    def create(self, sensor_id, temperature, datetime, location):
        cur = self.conn.cursor()
        cur.execute(
            insertion_resource,
            (sensor_id, temperature, datetime, location)
        )
        self.conn.commit()

    def update(self, sensor_id, temperature, datetime, location):
        cur = self.conn.cursor()
        cur.execute(
            update_resource_by_sensor_id,
            (temperature, datetime, location, sensor_id)
        )
        self.conn.commit()

    def delete(self, sensor_id):
        cur = self.conn.cursor()
        cur.execute(
            delete_resource_by_sensor_id, (sensor_id,)
        )
        self.conn.commit()

    def readBySensorId(self, sensor_id):
        cur = self.conn.cursor()
        cur.execute(
            selection_resource_by_sensor_id, (sensor_id,)
        )
        row = cur.fetchone()
        if row is not None:
            temperature = {
                "id": row[0],
                "sensor_id": row[1],
                "temperature": row[2],
                "datetime": row[3],
                "location": row[4]
            }
        else:
            temperature = None
        self.conn.commit()
        return temperature

    def readByLocation(self, location):
        cur = self.conn.cursor()
        cur.execute(
            selection_resource_by_location, ('%' + location + '%',)
        )
        row = cur.fetchone()
        if row:
            temperature = {
                "id": row[0],
                "sensor_id": row[1],
                "temperature": row[2],
                "datetime": row[3],
                "location": row[4]
            }
        else:
            temperature = None
        self.conn.commit()
        return temperature