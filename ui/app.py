import streamlit as st
import requests
import json
from s3fs.core import S3FileSystem


# Load matches from a local JSON file
@st.cache_data
def fetch_matches():
    s3 = S3FileSystem()
    # S3 bucket directory (data lake)
    DIR = 's3://ece5984-s3-sabarishm/Cricketdata'  # Insert your S3 bucket address here. Read from the directory you created in batch ingest: Lab2/batch_ingest/
    # Get data from S3 bucket as a pickle file
    file_name="cricket_data.json"
    with s3.open(f'{DIR}{file_name}', 'r') as s3_file, open(file_name, 'w') as local_file:
        for line in s3_file:
            local_file.write(line)
    with open("cricket_data.json", "r") as f:  # Replace with S3 fetch logic if needed
        return json.load(f)


# Second API: Fetch match details using `id`
@st.cache_data
def fetch_match_details(match_id):
    url = f"https://api.cricapi.com/v1/match_info?apikey=a1de8753-c1aa-430f-a383-57075927b424&offset=0&id={match_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Unable to fetch match details"}


# Title and Header
st.title("Winner's Circle Live - Cricket Scores🏏")
st.markdown("### Stay updated with live cricket scores!")

# Refresh Main Page Button
if st.button("Refresh Matches"):
    st.cache_data.clear()  # Clear cache to reload data
    st.rerun()

# Fetch and display matches
matches = fetch_matches()

# Match list view
if "selected_match_id" not in st.session_state:
    for match in matches:
        st.divider()  # Adds a separator for better UI
        col1, col2, col3 = st.columns([1, 3, 1])  # Layout for image, details, and refresh

        # Placeholder for cricket image (replace with dynamic content if available)
        with col1:
            st.image("https://via.placeholder.com/100x100.png?text=🏏", width=100)

        # Match details
        with col2:
            st.markdown(f"**{match['name']}**")
            st.text(f"Venue: {match['venue']}")
            if st.button(f"View Match", key=match['id']):
                st.session_state["selected_match_id"] = match['id']
                st.rerun()

        # Refresh Match Details
        with col3:
            if st.button(f"🔄", key=f"refresh_{match['id']}"):
                st.session_state[f"match_details_{match['id']}"] = fetch_match_details(match['id'])
                st.rerun()

# Match details view
else:
    selected_match_id = st.session_state["selected_match_id"]

    # Fetch match details using cached data
    if f"match_details_{selected_match_id}" in st.session_state:
        match_details = st.session_state[f"match_details_{selected_match_id}"]
    else:
        match_details = fetch_match_details(selected_match_id)
        st.session_state[f"match_details_{selected_match_id}"] = match_details

    if "error" in match_details:
        st.error(match_details["error"])
    else:
        st.markdown("### Match Information")
        data = match_details.get("data", {})
        if data:
            st.text(f"Name: {data.get('name', 'N/A')}")
            st.text(f"Type: {data.get('matchType', 'N/A')}")
            st.text(f"Venue: {data.get('venue', 'N/A')}")
            st.text(f"Date/Time: {data.get('dateTimeGMT', 'N/A')}")
            st.text(f"Status: {data.get('status', 'N/A')}")

            teams = data.get("teams", [])
            if len(teams) == 2:
                team1, team2 = teams
                score = data.get("score", [])
                team1_score = next((s for s in score if team1 in s["inning"]), {})
                team2_score = next((s for s in score if team2 in s["inning"]), {})

                st.text(
                    f"{team1}: {team1_score.get('r', 0)}/{team1_score.get('w', 0)} in {team1_score.get('o', 0)} overs")
                st.text(
                    f"{team2}: {team2_score.get('r', 0)}/{team2_score.get('w', 0)} in {team2_score.get('o', 0)} overs")

            if data.get("matchWinner"):
                st.success(f"Winner: {data['matchWinner']}")
        else:
            st.error("No data available for this match.")

    # Back button to return to match list
    if st.button("Back to Matches"):
        del st.session_state["selected_match_id"]
        st.rerun()
