import streamlit as st

from frontend import utils
from src.perfs_tracker import MainPerf, PerfsRaces

if "perfs" not in st.session_state:
    perfs = utils.load_data()
    st.session_state["perfs"] = perfs
    st.session_state["df"] = perfs.table()
if "show_form_edit" not in st.session_state:
    st.session_state["show_form_edit"] = False

perfs: PerfsRaces = st.session_state["perfs"]

# Récupérer l'ID de la course depuis l'URL
race_id: int = int(st.query_params.get("race_id", -1))

if race_id == -1:
    st.sidebar.title("Race viewer")
    name = st.sidebar.selectbox(
        "Select a race to view", options=perfs.race_names, index=None
    )
    race_id = perfs.race_names.index(name) if name else -1


if 0 <= race_id < len(perfs):
    perf: MainPerf = perfs[race_id]

    if perf.location.lower() in perf.name_event.lower():
        st.title(perf.name_event)
    else:
        st.title(f"{perf.name_event} - {perf.location}")
    st.markdown(f"## {perf.distance} km - `{perf.time}` on *{perf.date.date()}*")
    st.markdown(f"- Pace: `{perf.pace}` min/km ({perf.pace.kmh:.2f} km/h)")
    st.markdown(
        f"- Rank: {perf.rank} / {perf.num_participants} participants"
        + f" (top {perf.ratio:.2%})"
    )
    url_results = ""
    if perf.url_results:
        url_results += f"[Race results]({perf.url_results})"
    if perf.url_strava:
        url_results += f"[Strava]({perf.url_strava})"

    if url_results:
        st.markdown(f"- {url_results}")

    if perf.image_parcours:
        st.image(perf.image_parcours, caption="Parcours", width=700)

    if st.button("✍️ Edit"):
        st.session_state["show_form_edit"] = not st.session_state["show_form_edit"]

    if st.session_state["show_form_edit"]:
        with st.form(key="add_course_form"):
            response = utils.edit_race(perf, race_id=race_id)
            if response:
                print("reload data")
                del st.session_state["perfs"]
                perfs = utils.load_data()
                st.session_state["perfs"] = perfs
                print("reload data done")
                print(perfs[race_id].url_strava)

    _, right_col = st.columns([5, 1])
    with right_col:
        if st.button("❌ Delete"):
            st.write("Not implemented yet")


else:
    st.error("❌ Course introuvable !")
