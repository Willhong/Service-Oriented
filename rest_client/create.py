import requests

if __name__ == "__main__":
    res = requests.post(
        url='http://127.0.0.1:8080/resource/creation',
        data={
            'sensor_id': 't2',
            'temperature': 34.0,
            'datetime': '2019-10-01 09:10:00',
            'location': '2nd Floor, 4th Engineering Building, KoreaTech'
        }
    )

    print(res.status_code)
    print(res.json())