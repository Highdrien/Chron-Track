import streamlit as st
import pandas as pd

from frontend import utils
from src.perfs_tracker import MainPerf, PerfsRaces

# Récupérer l'ID de la course depuis l'URL
race_id: int = int(st.query_params.get("race_id", None))
print(f"race id: {race_id}")


if "perfs" not in st.session_state:
    perfs = utils.load_data()
    st.session_state["perfs"] = perfs
    st.session_state["df"] = perfs.table()

df: pd.DataFrame = st.session_state["df"]
perfs: PerfsRaces = st.session_state["perfs"]

# Vérifier si l'ID est valide
if 0 <= race_id < len(df):
    perf: MainPerf = perfs[race_id]
    st.write(f"{perf}")

    if perf.location.lower() in perf.name_event.lower():
        st.title(perf.name_event)
    else:
        st.title(f"{perf.name_event} - {perf.location}")
    st.markdown(f"## {perf.distance} km - `{perf.time}` on *{perf.date.date()}*")
    st.markdown(f"- Pace: `{perf.pace}` min/kim ({perf.pace.kmh:.2f} km/h)")
    st.markdown(f"- Rank: {perf.rank} / {perf.num_participants} participants")
    if perf.url_results:
        st.markdown(f"- Results: {perf.url_results}")
    if perf.url_strava:
        st.markdown(f"- Strava: {perf.url_strava}")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("✍️ Edit"):
            pass

    with col2:
        if st.button("❌ Delete"):
            st.write("Not implemented yet")
            pass

else:
    st.error("❌ Course introuvable !")
