import streamlit as st
import random
import time

# Function to handle the timer logic
def timer_function():
    # Initialize session state if not already done
    if 'time_left' not in st.session_state:
        st.session_state.time_left = 30 * 60  # 30 minutes in seconds
        st.session_state.timer_running = False
        st.session_state.start_time = None
        st.session_state.timer_started = False

    # Layout the buttons in columns
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if not st.session_state.timer_running:
            if st.button('Start Timer', key="start"):
                st.session_state.timer_running = True
                st.session_state.start_time = time.time()  # Record the start time when "Start" is pressed
                st.session_state.timer_started = True

        else:
            if st.button('Stop Timer', key="stop"):
                st.session_state.timer_running = False
                st.session_state.time_left = max(0, int(st.session_state.time_left - (time.time() - st.session_state.start_time)))

    with col2:
        if st.button('Reset Timer', key="reset"):
            st.session_state.time_left = 30 * 60  # Reset to 30 minutes
            st.session_state.timer_running = False
            st.session_state.timer_started = False

    # Timer countdown logic
    if st.session_state.timer_running:
        # Update the timer every second
        current_time = time.time()
        elapsed_time = current_time - st.session_state.start_time
        st.session_state.time_left = max(0, int(30 * 60 - elapsed_time))

        # Display the countdown timer using st.empty() for live updating
        timer_display = f"{st.session_state.time_left // 60:02d}:{st.session_state.time_left % 60:02d}"

        timer_placeholder = st.empty()  # Create an empty placeholder
        timer_placeholder.text(f"<h1 style='color: #FF6347; text-align: center;'>{timer_display}</h1>", unsafe_allow_html=True)  # Update the display

        # Stop timer once it reaches 0
        if st.session_state.time_left == 0:
            timer_placeholder.text("<h1 style='color: #FF6347; text-align: center;'>Time's up!</h1>", unsafe_allow_html=True)
            st.session_state.timer_running = False
            st.error("Time is up! Please stop your speech.")
    else:
        # Display the initial 30 minutes timer
        timer_placeholder = st.empty()
        timer_placeholder.text("<h1 style='color: #008CBA; text-align: center;'>30:00</h1>", unsafe_allow_html=True)

# Page 1 - Topic Selection
def topic_selection():
    st.write("<h1 style='color: #FF6347;'>Extemp Speech Topics</h1>", unsafe_allow_html=True)

    # Prompt user to enter topics separated by newlines
    topics_input = st.text_area("Enter your topics, each on a new line:", height=200)

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
            st.write("<h3>Here are your 3 randomly selected topics:</h3>", unsafe_allow_html=True)
            for i, topic in enumerate(chosen_topics, 1):
                st.write(f"{i}. {topic}")
            
            # Let the user choose one of the three topics
            selected_topic = st.selectbox("Choose one topic for your extemp:", chosen_topics)
            
            # Save the selected topic in session state
            if selected_topic:
                st.session_state.selected_topic = selected_topic
                st.session_state.screen = "timer"  # Change screen to timer

# Page 2 - Timer Screen
def timer_screen():
    # Display the chosen topic in big letters
    st.write(f"<h1 style='color: #008CBA; text-align: center;'>{st.session_state.selected_topic.upper()}</h1>", unsafe_allow_html=True)
    
    # Call the timer function
    timer_function()

    # Button to go back to topic selection
    if st.button("Back to Topic Selection"):
        st.session_state.screen = "topics"  # Go back to topic selection screen

# Main app logic (decides which screen to display)
def main():
    if 'screen' not in st.session_state:
        st.session_state.screen = "topics"  # Initial screen is topic selection

    if st.session_state.screen == "topics":
        topic_selection()
    elif st.session_state.screen == "timer":
        timer_screen()

# Run the app
main()
