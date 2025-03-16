import pandas as pd
from datetime import datetime
from pathlib import Path

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
        name=line["Nom de l'épreuve"],
        date=datetime.strptime(line["date"], "%Y-%m-%d"),
        distance=line["km"],
        time=time,
        location=line["Ville"],
        rank=line["scratch"],
        num_participants=line["nb participants"],
    )

    perfs.add_perf(perf)


print(perfs)
file_path = Path("data/perfs.json")
perfs.save_to_json(file_path)
