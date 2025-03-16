from datetime import datetime

from src.perf_tracker import Perf
from time_an_pace import Time

t = Time(hours=1, minutes=25, seconds=22)
perf = Perf(time=t, distance=21.1, date=datetime.now())
print(perf)
print(perf.pace)
print(perf.get_event())
