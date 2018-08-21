from datetime import datetime

from pytz import timezone
from sqlalchemy import Column, String, Integer, Numeric, Date

from base import Base


class Weather(Base):
    __tablename__ = 'weather'

    id = Column(Integer, primary_key=True)
    temp = Column(Numeric)
    temp_min = Column(Integer)
    temp_max = Column(Integer)
    humidity = Column(Integer)
    city = Column(String)
    dt = Column(Integer)
    created_at = Column(Date)

    def __init__(self, temp, temp_min, temp_max, dt, humidity, city):
        self.temp = temp
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.humidity = humidity
        self.dt = dt
        self.city = city
        self.created_at = datetime.now(timezone('Asia/Hong_Kong'))
