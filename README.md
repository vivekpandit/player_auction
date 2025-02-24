# Cricket Auction System

This project is a Streamlit-based **Cricket Auction System** that allows multiple team captains to bid on players.

## Features
1. **CSV Upload**:  
   - Upload a CSV file with the player details.  
   - Automatically shuffles the uploaded list of players once, ensuring a random order.

2. **Bidding**:  
   - Each team can place a bid on the current player, ensuring the bid does not exceed the team’s budget.  
   - Once a bid is submitted, the player is marked “sold.” The user can then proceed to the next player.

3. **Multiple Teams**:  
   - Teams are defined in a single list (`TEAMS`), so you can easily add or remove teams.  
   - Each team starts with a defined budget (`BUDGET`) and references the same base price (`BASE_PRICE`).

4. **Team Summaries**:  
   - Real-time tables showing which players each team has bought and at what bid.  
   - Displays remaining budgets for all teams.

5. **Final Team Assignments**:  
   - Once all players are auctioned, displays a summary of each team’s roster.  
   - Provides a **Download** button to obtain a CSV with the final assignments.

## Getting Started

### Prerequisites
- **Python 3.7+**
- **Streamlit** (`pip install streamlit`)
- **Pandas** (`pip install pandas`)

### Installation
1. **Clone or Download** this repository.
2. **Install dependencies** if not already:
   ```bash
   pip install streamlit pandas
