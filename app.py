import streamlit as st
import random

# Title for the app
st.title("Extemp Draw Simulation")

# Prompt user to enter topics separated by newlines
topics_input = st.text_area("Enter your topics, each on a new line:")

# When the user presses a button to submit
if st.button("Generate Topics"):
    # Split the input string into a list of topics based on newlines
    topics = [topic.strip() for topic in topics_input.split('\n') if topic.strip()]
    
    if len(topics) < 3:
        st.error("Please enter at least 3 topics.")
    else:
        # Randomly select 3 topics from the list
        chosen_topics = random.sample(topics, 3)
        
        # Display the 3 randomly selected topics
        st.write("Here are your 3 randomly selected topics:")
        st.write("1. ", chosen_topics[0])
        st.write("2. ", chosen_topics[1])
        st.write("3. ", chosen_topics[2])
        
        # Let the user choose one of the three topics
        selected_topic = st.selectbox("Choose one topic for your extemp:", chosen_topics)
        
        # Display the chosen topic after selection
        if selected_topic:
            st.write(f"Your selected topic is: {selected_topic}")
