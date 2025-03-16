from datetime import datetime
from pathlib import Path

from src.perfs_tracker import MainPerf, PerfOfAllTime
from src.time_an_pace import Time

t = Time(hours=1, minutes=25, seconds=22)
perf = MainPerf(time=t, distance=21.1, date=datetime.now())
print(perf)
print(perf.pace)

perf.add_sub_perf(
    list_sub_time=[
        Time(hours=0, minutes=40, seconds=0),
        Time(hours=0, minutes=39, seconds=58),
    ],
    sub_distance=10,
)


all_perfs = PerfOfAllTime(perfs=[], gender="male")
all_perfs.add_perf(perf)
all_perfs.compute_iaaf_scores()
all_perfs.save_to_json(Path("data") / "perfs.json")

best_10k = all_perfs.get_personal_best(10)
print(best_10k)
print(best_10k.pace)
print(best_10k.iaaf_score)
