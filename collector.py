from json import loads as json_loads
from os import environ

from celery import Celery

from base import Session
from weather import Weather

host = environ['REDIS_HOST']
port = environ['REDIS_PORT']

app = Celery('tasks', broker='redis://' + host + ':' + port + '/0')


@app.task(name='save_data')
def save(data):
    d = json_loads(data)
    session = Session()

    time_equals = Weather.dt == d["dt"]
    city_equals = Weather.city == d["city"]

    # check if data is in the DB
    q = session.query(Weather).filter(time_equals).filter(city_equals).count()
    print(q)

    # if data is not in db, save it
    if q <= 0:
        w = Weather(
            d['temp'],
            d['temp_min'],
            d['temp_max'],
            d['dt'],
            d['humidity'],
            d['city']
        )
        session.add(w)
        session.commit()
        session.close()
        print(str(data) + 'is saved')
    else:
        print('not saved')
    return
