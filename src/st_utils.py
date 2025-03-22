import datetime
from pathlib import Path

import pandas as pd
import streamlit as st

from .perfs_tracker import MainPerf, PerfsRaces
from .time_an_pace import Time


@st.cache_data
def load_data() -> PerfsRaces:
    """
    Loads performance data from a JSON file.
    """
    filepath = Path("data/perfs.json")
    perfs = PerfsRaces()
    if filepath.exists():
        perfs.load_from_json(Path("data/perfs.json"))

    return perfs


def filter_location(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filters the given DataFrame by a selected location using
    a Streamlit sidebar selectbox.

    Args:
        df (pd.DataFrame): The input DataFrame containing a "Location" column.

    Returns:
        pd.DataFrame: The filtered DataFrame based on the selected location.
            If "All" is selected, the original DataFrame is returned.
    """
    locations = df["Location"].unique()
    locations.sort()
    selected_location = st.sidebar.selectbox(
        "Filter by location :", ["All"] + list(locations)
    )
    if selected_location != "All":
        df = df[df["Location"] == selected_location]

    return df


def filter_distance(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filters the given DataFrame based on the selected distance from a Streamlit sidebar.

    Args:
        df (pd.DataFrame): The input DataFrame containing a column "Distance (km)".

    Returns:
        pd.DataFrame: The filtered DataFrame based on the selected distance.
    """
    distances = df["Distance (km)"].unique()
    distances.sort()
    selected_distance = st.sidebar.selectbox(
        "Filter by distance (km) :", ["All"] + list(distances)
    )
    if selected_distance != "All":
        df = df[df["Distance (km)"] == selected_distance]

    return df


def add_new_race():
    """
    Displays a form to add a new race event with details such as name, location, time,
    and distance. On form submission, the new race is added to the session state
    DataFrame and saved to a JSON file.
    """
    st.subheader("Enter the race detail:")
    name = st.text_input("Race name", placeholder="Ex: Marathon de Paris")
    location = st.text_input("City", placeholder="Ex: Montpellier")
    date = st.date_input("Race date", datetime.date.today())

    col1, col2, col3 = st.columns(3)
    with col1:
        hours = st.number_input("Hours", min_value=0, max_value=78, value=0, step=1)
    with col2:
        minutes = st.number_input("Minutes", min_value=0, max_value=59, value=0, step=1)
    with col3:
        seconds = st.number_input(
            "Secondes", min_value=0, max_value=59, value=0, step=1
        )

    distance = st.number_input(
        "Distance (km)", min_value=0.1, max_value=500.0, value=10.0, step=0.1
    )

    st.subheader("Additional information (optional):")

    col1, col2 = st.columns(2)
    with col1:
        rank = st.number_input("Rank (optional)", min_value=0, step=1)
    with col2:
        num_participants = st.number_input(
            "Number of participants (optional)", min_value=0, step=1
        )

    url_results = st.text_input("URL results (optional)")
    url_strava = st.text_input("URL Strava (optional)")

    submit_button = st.form_submit_button(label="✅ Add the race to the database")

    if submit_button:
        # Ajouter la nouvelle course au DataFrame de session_state
        new_time = Time(hours=hours, minutes=minutes, seconds=seconds)
        new_perf = MainPerf(
            name_event=name,
            date=date,
            distance=distance,
            time=new_time,
            location=location,
            rank=rank if rank != 0 else None,
            num_participants=num_participants if num_participants != 0 else None,
            url_results=url_results,
            url_strava=url_strava,
        )
        perfs: PerfsRaces = st.session_state["perfs"]
        perfs.add_perf(new_perf)
        st.session_state["df"] = perfs.table()

        if perfs:
            perfs.save_to_json(Path("data/perfs.json"))

        st.success("✅ Race added successfully!")

        # Masquer le formulaire après ajout
        st.session_state["show_form"] = False
        st.rerun()


def get_pbs_as_dataframe() -> pd.DataFrame:
    """
    Retrieve personal best performances from the session state and
    return them as a pandas DataFrame.

    Returns:
        pd.DataFrame: A DataFrame containing all personal best performances.
    """
    perfs: PerfsRaces = st.session_state["perfs"]
    pb = perfs.get_all_personal_best()
    pb_with_time: dict[float, str] = {
        distance: str(perf.time) for distance, perf in pb.items()
    }
    return pd.DataFrame(list(pb_with_time.items()), columns=["Distance (km)", "Chrono"])
