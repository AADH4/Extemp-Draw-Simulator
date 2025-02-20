import streamlit as st
import random
import time

# Function to handle the timer logic
def timer_function():
    # Initialize session state if not already done
    if 'time_left' not in st.session_state:
        st.session_state.time_left = 30 * 60  # 30 minutes in seconds
        st.session_state.timer_running = False
        st.session_state.timer_started = False
    
    # Function to start the timer
    def start_timer():
        st.session_state.timer_running = True
        st.session_state.timer_started = True
        st.session_state.start_time = time.time() - st.session_state.time_left
    
    # Function to stop the timer
    def stop_timer():
        st.session_state.timer_running = False
        st.session_state.time_left = max(0, int(st.session_state.time_left - (time.time() - st.session_state.start_time)))
    
    # Function to reset the timer
    def reset_timer():
        st.session_state.time_left = 30 * 60  # Reset to 30 minutes
        st.session_state.timer_running = False
        st.session_state.timer_started = False
    
    # Start/Stop/Reset buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if not st.session_state.timer_running:
            if st.button('Start Timer'):
                start_timer()
        else:
            if st.button('Stop Timer'):
                stop_timer()
    
    with col2:
        if st.button('Reset Timer'):
            reset_timer()

    # Timer countdown logic
    if st.session_state.timer_running:
        st.session_state.time_left = max(0, int(time.time() - st.session_state.start_time))

    minutes = st.session_state.time_left // 60
    seconds = st.session_state.time_left % 60

    time_display = f"{minutes:02d}:{seconds:02d}"
    st.write("### Timer: ", time_display)

    # Alert the user for 10 and 5 minute warnings
    if st.session_state.time_left == 600:
        st.warning("10-minute warning!")
    elif st.session_state.time_left == 300:
        st.warning("5-minute warning!")
    
    # When time is over
    if st.session_state.time_left == 0:
        st.error("Time is up! Please stop your speech.")
    
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
            # Save the selected topic in session state
            st.session_state.selected_topic = selected_topic
            
            # Move to the next screen to display the topic with the timer
            st.experimental_rerun()

# Check if a topic has been selected (from the dropdown)
if 'selected_topic' in st.session_state:
    # Display the chosen topic in big letters
    st.write(f"### {st.session_state.selected_topic.upper()}")
    
    # Call the timer function
    timer_function()
