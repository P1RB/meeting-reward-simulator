import streamlit as st

def calculate_decay_multiplier(participation_count, decay_per_event=0.2, min_multiplier=0.2):
    decay = decay_per_event * (participation_count - 1)
    return max(1.0 - decay, min_multiplier)

def calculate_attendee_reward(base_reward, tier_multiplier, participation_count):
    decay_multiplier = calculate_decay_multiplier(participation_count)
    return base_reward * tier_multiplier * decay_multiplier

def calculate_organiser_reward(attendee_rewards, organiser_participation_count):
    total_attendee_rewards = sum(attendee_rewards)
    organiser_decay_multiplier = calculate_decay_multiplier(organiser_participation_count)
    raw_organiser_reward = 0.5 * total_attendee_rewards
    return raw_organiser_reward * organiser_decay_multiplier

def simulate_event(base_reward, tier_multiplier, attendee_participations, organiser_participation_count):
    attendee_rewards = []
    for p_count in attendee_participations:
        reward = calculate_attendee_reward(base_reward, tier_multiplier, p_count)
        attendee_rewards.append(reward)
    organiser_reward = calculate_organiser_reward(attendee_rewards, organiser_participation_count)
    return attendee_rewards, organiser_reward

# Streamlit App
st.title("Meeting Reward Simulator")

base_reward = st.slider("Base Reward (points)", 1, 50, 10)
tier_multiplier = st.slider("Tier Multiplier", 1, 5, 2)
num_attendees = st.slider("Number of Attendees", 1, 30, 5)

st.subheader("Set Attendees' Participation Counts")
attendee_participations = []
for i in range(num_attendees):
    participation = st.slider(f"Attendee {i+1} Participation Count", 1, 10, 1)
    attendee_participations.append(participation)

organiser_participation_count = st.slider("Organiser Participation Count", 1, 10, 1)

if st.button("Calculate Rewards"):
    attendee_rewards, organiser_reward = simulate_event(base_reward, tier_multiplier, attendee_participations, organiser_participation_count)
    st.subheader("Results")
    for idx, reward in enumerate(attendee_rewards):
        st.write(f"Attendee {idx+1}: {reward:.2f} points")
    st.write(f"Organiser Reward: {organiser_reward:.2f} points")