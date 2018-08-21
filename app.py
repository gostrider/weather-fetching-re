from os import environ

from celery import Celery
from flask import Flask, jsonify, request

from weather import Weather

MAX_LIMIT = 20
app = Flask(__name__)
host = environ['REDIS_HOST']
port = environ['REDIS_PORT']

cel = Celery('tasks', broker='redis://' + host + ':' + port + '/0')


@app.route('/')
def main():
    return 'ok'


@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    start = request.args.get('start')
    end = request.args.get('end')
    limit = request.args.get('limit')

    # session = Session()
    # weather = _filter(session, city, start, end, limit)
    # data = []
    # for w in weather:
    #     d = w.__dict__
    #     d['temp'] = float(d['temp'])
    #     del d['_sa_instance_state']
    #     data.append(d)
    # session.close()
    data = cel.send_task(
        'query_data',
        kwargs=dict(city=city, start=start, end=end, limit=limit),
    )
    return jsonify(data)


def _filter(session, city, start, end, limit):
    q = session.query(Weather)

    if city:
        q = q.filter(Weather.city == city)

    if start:
        q = q.filter(Weather.dt >= start)

    if end:
        q = q.filter(Weather.dt <= end)

    return q.limit(limit if limit else MAX_LIMIT).all()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002)
