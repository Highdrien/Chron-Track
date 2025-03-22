from datetime import datetime
from pathlib import Path

import pandas as pd

from src.perfs_tracker import MainPerf, PerfOfAllTime
from src.time_an_pace import Time

perfs = PerfOfAllTime(gender="male")

# Load the data
data_path = Path("data/courses.csv")
df = pd.read_csv(data_path)

for i, line in df.iterrows():
    time_str = line["temps"].split(":")
    time = Time(hours=time_str[0], minutes=time_str[1], seconds=time_str[2])
    perf = MainPerf(
        name_event=line["Nom de l'épreuve"],
        date=datetime.strptime(line["date"], "%Y-%m-%d"),
        distance=line["km"],
        time=time,
        location=line["Ville"],
        rank=line["scratch"],
        num_participants=line["nb participants"],
    )

    perfs.add_perf(perf)


# add subperformances
perf = MainPerf(
    name_event="10 km de Paris",
    date=datetime(2019, 10, 6),
    distance=10,
    time=Time(hours=0, minutes=41, seconds=0),
    location="Paris",
    rank=1,
    num_participants=10000,
)
sub_perfs_10k: list[Time] = [
    Time(hours=0, minutes=21, seconds=0),
    Time(hours=0, minutes=19, seconds=0),
]
perf.add_sub_perf(sub_perfs_10k, sub_distance=5)
perfs.add_perf(perf)


print(perfs)
perfs.compute_iaaf_scores()
for distance, perf in perfs.get_all_personal_best().items():
    print(f"Personal best for {distance} km: {perf}")

file_path = Path("data/perfs.json")
print(f"length: {len(perfs)}")
perfs.save_to_json(file_path)

df = perfs.table()
print(df)

# perfs = PerfOfAllTime(gender="male")
# print(perfs)
# perfs.load_from_json(file_path)
# print(f"length: {len(perfs)}")
