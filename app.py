import streamlit as st

from src import st_utils

if "perfs" not in st.session_state:
    perfs = st_utils.load_data()
    st.session_state["perfs"] = perfs
    st.session_state["df"] = perfs.table()


st.title("Performances of All Time")
st.write("This app allows you to track your performances over time.")
df = st.session_state["df"]

st.sidebar.header("Filters")
df = st_utils.filter_location(df)
df = st_utils.filter_distance(df)
if st.sidebar.button("Reset filters"):
    df = st.session_state["df"]

st.sidebar.subheader("Display performances")
st.write("Here are your best performances:")

if "perfs" in st.session_state:
    st.sidebar.dataframe(
        st_utils.get_pbs_as_dataframe(), hide_index=True, use_container_width=True
    )

st.data_editor(
    df,
    column_config={
        "rank": st.column_config.ProgressColumn(
            "Ratio",
            help="The ratio of the rank and the number of participants.",
            min_value=0,
            max_value=1,
        ),
        "sub_perfs": st.column_config.BarChartColumn(
            "Intermediate times on 5k",
            help="The intermediate times for each 5k split.",
            y_min=0,
            y_max=1500,
        ),
    },
    hide_index=True,
    use_container_width=True,
)


# Bouton pour afficher le formulaire
if "show_form" not in st.session_state:
    st.session_state["show_form"] = False

if st.button("➕ Ajouter une course"):
    st.session_state["show_form"] = not st.session_state["show_form"]

if st.session_state["show_form"]:
    with st.form(key="add_course_form"):
        st_utils.add_new_race()
