import streamlit as st
from pathlib import Path

from src.perfs_tracker import PerfOfAllTime


st.title("Performance of All Time")
st.write("This app allows you to track your performances over time.")

perfs = PerfOfAllTime()
perfs.load_from_json(Path("data/perfs.json"))

df = perfs.table()
print(df)

st.dataframe(df, use_container_width=True)
