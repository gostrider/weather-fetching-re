from datetime import datetime, timedelta
from json import dumps as json_dumps
from os import environ

import gevent
from gevent import monkey
from pytz import timezone

monkey.patch_all()

import requests
from celery import Celery

host = environ['REDIS_HOST']
port = environ['REDIS_PORT']

API_KEY = '48bbaebf7c231fd1aa7bb98ef93d6f39'
HK = 1819730
SG = 1880251

cel = Celery('tasks', broker='redis://' + host + ':' + port + '/0')


def ticks(**kwargs):
    return datetime.now(timezone("Asia/Hong_Kong")) + timedelta(**kwargs)


@cel.task(name='scrape_data')
def scrape():
    country_code = {
        1819730: "HK",
        1880251: "SG",
    }

    r = requests.get(
        "http://api.openweathermap.org/data/2.5/group",
        params={
            "id": str(HK) + "," + str(SG),
            "APPID": API_KEY,
            "units": "metric",
        },
    )

    if r.status_code == 200:
        data = r.json()['list']
        for d in data:
            data = {
                'temp': d['main']['temp'],
                'temp_min': d['main']['temp_min'],
                'temp_max': d['main']['temp_max'],
                'humidity': d['main']['humidity'],
                'dt': d['dt'],
                'city': country_code.get(d["id"], "XX")
            }
            cel.send_task('save_data', kwargs=dict(data=json_dumps(data)))

        cel.send_task('scrape_data', eta=ticks(minutes=1), queue='timer')

    elif r.status_code == 429:
        print('429 retrying much later')
        cel.send_task('scrape_data', eta=ticks(hours=1), queue='timer')

    else:
        print('warn users, there is an error')
        cel.send_task('scrape_data', eta=ticks(hours=1), queue='timer')


def event_loop():
    while True:
        scrape()


if __name__ == "__main__":
    event_loop()
