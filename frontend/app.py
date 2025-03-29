import streamlit as st

import utils

# hide_menu_style = """
#     <style>
#         [data-testid="stSidebarNav"] {
#             display: none;
#         }
#     </style>
# """
# st.markdown(hide_menu_style, unsafe_allow_html=True)

if "perfs" not in st.session_state:
    perfs = utils.load_data()
    st.session_state["perfs"] = perfs
    st.session_state["df"] = perfs.table()


st.title("Performances of All Time")
st.write("This app allows you to track your performances over time.")
df = st.session_state["df"]

st.sidebar.header("Filters")
df = utils.filter_location(df)
df = utils.filter_distance(df)
if st.sidebar.button("Reset filters"):
    df = st.session_state["df"]

st.sidebar.subheader("Display performances")
st.write("Here are your best performances:")

if "perfs" in st.session_state:
    st.sidebar.dataframe(
        utils.get_pbs_as_dataframe(), hide_index=True, use_container_width=True
    )

df["View"] = [f"/view?race_id={i}" for i in range(len(df))]

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
        "View": st.column_config.LinkColumn(
            "📝 View",
            help="Click to edit this race",
        ),
    },
    hide_index=True,
    use_container_width=True,
)


# Add new race
if "show_form" not in st.session_state:
    st.session_state["show_form"] = False

if st.button("➕ Ajouter une course"):
    st.session_state["show_form"] = not st.session_state["show_form"]

if st.session_state["show_form"]:
    with st.form(key="add_course_form"):
        utils.add_new_race()

# View race
