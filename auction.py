import streamlit as st
import pandas as pd
import random

# Single Definitions for Team Names, Base Price, and Budget
TEAMS = ["Team Arun", "Team Mayank", "Team Sanjay"]  # Add or remove teams here
BASE_PRICE = 50
BUDGET = 1200

# Session State Initialization
if 'players_df' not in st.session_state:
    st.session_state.players_df = None
if 'auctioned_players' not in st.session_state:
    st.session_state.auctioned_players = {}
# Make budgets a dict from TEAMS
if 'budgets' not in st.session_state:
    st.session_state.budgets = {team: BUDGET for team in TEAMS}
# Make teams a dict from TEAMS
if 'teams' not in st.session_state:
    st.session_state.teams = {team: [] for team in TEAMS}
if 'current_player_index' not in st.session_state:
    st.session_state.current_player_index = 0
# Track if the current player is sold
if 'player_sold' not in st.session_state:
    st.session_state.player_sold = False

st.title("🏏 Welcome PPL Auction")

# CSV Upload
st.sidebar.header("Upload Player List")
file = st.sidebar.file_uploader("Upload CSV with Player Details", type=["csv"])

if file is not None and st.session_state.players_df is None:
    df = pd.read_csv(file)
    # Shuffle once
    st.session_state.players_df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    st.session_state.current_player_index = 0
    st.session_state.player_sold = False
    st.success("Player list loaded and shuffled successfully!")

# Auction Logic
if st.session_state.players_df is not None and len(st.session_state.players_df) > 0:
    # Check if there are still players left
    if st.session_state.current_player_index < len(st.session_state.players_df):
        current_player = st.session_state.players_df.iloc[st.session_state.current_player_index]

        st.subheader("Current Player Details")
        st.write(current_player)
        st.write(f"Base Price: ${BASE_PRICE}")

        if not st.session_state.player_sold:
            # Show bidding inputs only if player is not yet sold
            bid_amounts = {}
            for team in TEAMS:
                bid_amounts[team] = st.number_input(
                    label=f"{team}'s Bid",
                    min_value=BASE_PRICE,
                    max_value=st.session_state.budgets[team],
                    value=BASE_PRICE,
                    step=10,
                    key=f"bid_{team}_{st.session_state.current_player_index}"
                )

            if st.button("Submit Bids", key=f"submit_{st.session_state.current_player_index}"):
                winning_team = max(bid_amounts, key=bid_amounts.get)
                winning_bid = bid_amounts[winning_team]

                if winning_bid <= st.session_state.budgets[winning_team]:
                    # Deduct from that team's budget
                    st.session_state.budgets[winning_team] -= winning_bid

                    # Add this player to the winning team's list
                    st.session_state.teams[winning_team].append(current_player.to_dict())

                    # Store the auction info
                    player_name = str(current_player.get('Name', f'Player {st.session_state.current_player_index}'))
                    st.session_state.auctioned_players[player_name] = (winning_team, winning_bid)

                    st.success(f"{player_name} sold to {winning_team} for ${winning_bid}")

                    # Mark the player as sold
                    st.session_state.player_sold = True
                else:
                    st.error(f"{winning_team} does not have enough budget!")
        else:
            # Player is sold, show Next Player button
            st.success("Player sold! Proceed to the next player.")
            if st.button("Next Player"):
                st.session_state.current_player_index += 1
                st.session_state.player_sold = False
    else:
        # No more players to auction
        st.subheader("Final Team Assignments")
        final_data = []
        for team, players in st.session_state.teams.items():
            st.write(f"### {team}")
            for player in players:
                name = player.get('Name', 'Unknown')
                bid_value = st.session_state.auctioned_players[name][1] if name in st.session_state.auctioned_players else 0
                st.write(f"- {name} (${bid_value})")
                final_data.append([team, *list(player.values()), bid_value])

        columns = ["Team"] + list(st.session_state.players_df.columns) + ["Bid Amount"]
        final_df = pd.DataFrame(final_data, columns=columns)
        csv = final_df.to_csv(index=False).encode('utf-8')

        st.download_button(
            label="Download Team Assignments CSV",
            data=csv,
            file_name="team_assignments.csv",
            mime="text/csv"
        )

    # Show 3 tables for each team's picks
    st.subheader("Team Summaries")
    team_columns = st.columns(len(TEAMS))

    for i, team in enumerate(TEAMS):
        with team_columns[i]:
            st.write(f"### {team}")
            team_data = []
            for p in st.session_state.teams[team]:
                player_name = p.get('Name', 'Unknown')
                bid_value = st.session_state.auctioned_players[player_name][1] if player_name in st.session_state.auctioned_players else 0
                team_data.append({"Player Name": player_name, "Bid Amount": bid_value})
            if team_data:
                st.table(pd.DataFrame(team_data))
            else:
                st.write("No players yet.")

    # Show Remaining Budgets
    st.subheader("Remaining Budgets")
    for team in TEAMS:
        st.write(f"{team}: ${st.session_state.budgets[team]}")
else:
    st.info("Please upload a valid CSV with player details.")
