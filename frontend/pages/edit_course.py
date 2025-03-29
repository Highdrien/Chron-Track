import streamlit as st
import pandas as pd
import urllib.parse

# Récupérer l'ID de la course depuis l'URL
query_params = st.query_params.to_dict()
course_id = int(query_params.get("course_id", -1))  # -1 si aucun ID trouvé

# Simuler le chargement des données (tu peux utiliser une vraie base de données)
data = {
    "Nom": ["Marathon de Paris", "10km de Montpellier", "Semi de Lyon"],
    "Participants": [2000, 500, 1200],
    "Rank": [150, 50, 300],
    "Distance (km)": [42.2, 10.0, 21.1],
    "Chrono": ["3h57min33s", "39min17s", "1h25min22s"],
    "Date": ["2024-03-15", "2024-02-10", "2024-04-05"],
}
df = pd.DataFrame(data)

# Vérifier si l'ID est valide
if 0 <= course_id < len(df):
    st.title(f"📝 Éditer la course : {df.loc[course_id, 'Nom']}")

    new_name = st.text_input("Nom", value=df.loc[course_id, "Nom"])
    new_participants = st.number_input(
        "Nombre de participants", min_value=1, value=df.loc[course_id, "Participants"]
    )
    new_rank = st.number_input(
        "Votre rang", min_value=1, value=df.loc[course_id, "Rank"]
    )
    new_distance = st.number_input(
        "Distance (km)", min_value=0.1, value=df.loc[course_id, "Distance (km)"]
    )
    new_chrono = st.text_input("Chrono", value=df.loc[course_id, "Chrono"])
    new_date = st.date_input(
        "Date", value=pd.to_datetime(df.loc[course_id, "Date"]).date()
    )

    if st.button("✅ Enregistrer les modifications"):
        df.loc[course_id, "Nom"] = new_name
        df.loc[course_id, "Participants"] = new_participants
        df.loc[course_id, "Rank"] = new_rank
        df.loc[course_id, "Distance (km)"] = new_distance
        df.loc[course_id, "Chrono"] = new_chrono
        df.loc[course_id, "Date"] = new_date.strftime("%Y-%m-%d")
        st.success("✅ Course mise à jour avec succès !")
else:
    st.error("❌ Course introuvable !")
