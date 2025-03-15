from src.basic_class import Time
from src.perf_tracker import Perf
from datetime import datetime

t = Time(hours=1, minutes=25, seconds=22)
p = Perf(time=t, distance=21, date=datetime.now())
print(p)
print(p.pace)