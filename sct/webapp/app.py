import streamlit as st
import plotly.express as px
import pandas as pd
import time
import requests
import sct

st.markdown('''# Social Choice Theory''')

# Initialize session state for words and agents
if "words" not in st.session_state:
    st.session_state.words = []
if "agents" not in st.session_state:
    st.session_state.agents = {}  # Dictionary to store agents and their preferences

st.title("An implementation of Plurality & Borda rules for social decision-making")

# Step 1: Add words
st.header("Step 1: What are you choosing amongst?")
word = st.text_input("Enter a candidate:", "")

if st.button("Add Candidate"):
    if word.strip():  # Check that the input is not empty
        st.session_state.words.append(word.strip())
        st.success(f"Added '{word}'")
    else:
        st.warning("Please enter a valid word.")

# Display entered words
st.subheader("Candidates:")
if st.session_state.words:
    st.write(", ".join(st.session_state.words))
else:
    st.write("No words added yet.")

# Option to clear words
if st.button("Clear Words"):
    st.session_state.words = []
    st.info("All words cleared!")

# Step 2: Add agents and rank preferences
st.header("Step 2: Who is choosing and how do they rank the candidates?")

# Input for agent name
agent_name = st.text_input("Enter agent name:", "")

if st.button("Add Agent"):
    if agent_name.strip():  # Check that the agent name is not empty
        if agent_name in st.session_state.agents:
            st.warning(f"Agent '{agent_name}' already exists.")
        else:
            st.session_state.agents[agent_name] = []  # Initialize with empty preferences
            st.success(f"Added agent '{agent_name}'")
    else:
        st.warning("Please enter a valid agent name.")

# Display agents
st.subheader("Agents:")
if st.session_state.agents:
    for agent, preferences in st.session_state.agents.items():
        st.write(f"**{agent}**: {preferences if preferences else 'No preferences set'}")
else:
    st.write("No agents added yet.")

# Assign preferences for an agent
if st.session_state.agents:
    st.subheader("Assign Preferences")
    selected_agent = st.selectbox("Select an agent:", list(st.session_state.agents.keys()))
    if st.session_state.words:
        ranked_words = st.multiselect(
            f"Rank words for {selected_agent}:",
            options=st.session_state.words,
            default=st.session_state.agents[selected_agent],
        )
        if st.button(f"Save Preferences for {selected_agent}"):
            st.session_state.agents[selected_agent] = ranked_words
            st.success(f"Preferences updated for {selected_agent}")
    else:
        st.warning("No words available to rank. Add words first.")

# Option to clear agents and preferences
if st.button("Clear Agents and Preferences"):
    st.session_state.agents = {}
    st.info("All agents and preferences cleared!")

# Step 3: Choose Voting Method and Run Election
st.header("Step 3: Run Election")

if st.session_state.agents and st.session_state.words:
    voting_method = st.selectbox("Choose a voting method:", ["Plurality", "Borda"])

    if st.button("Run Election"):
        # Compute results based on the selected voting method
        results = {}
        # Create sct.Agent objects for each agent
        curr_agents = [sct.Agent(name, 1, preferences) for name, preferences in st.session_state.agents.items()]

        if voting_method == "Plurality":
            # Count the top-ranked word for each agent
            elec = sct.Plurality(st.session_state.words, curr_agents)
            results = elec.calculate_results()

        elif voting_method == "Borda":
            # Assign points based on rank and sum them
            elec = sct.Borda(st.session_state.words, curr_agents)
            results = elec.calculate_results()

        # Display the results
        st.subheader(f"Election Results ({voting_method} Method):")
        for word, score in results.items():
            st.write(f"**{word}**: {score} votes/points")

else:
    st.warning("Please ensure both words and agent preferences are set before running an election.")

# Debugging: Show current session state (optional)
st.sidebar.header("Session State Debugging")
st.sidebar.write(st.session_state)
