import streamlit as st
import random
import time
import threading

# Function to handle the timer logic with threading
def start_timer():
    start_time = time.time()
    while st.session_state.timer_running:
        elapsed_time = time.time() - start_time
        st.session_state.time_left = max(0, int(30 * 60 - elapsed_time))  # 30 minutes
        time.sleep(1)  # Update every second

    # Once timer finishes, show the alert
    st.session_state.timer_running = False
    st.session_state.time_left = 0

# Function to display the timer and control buttons
def timer_function():
    if 'time_left' not in st.session_state:
        st.session_state.time_left = 30 * 60  # 30 minutes
        st.session_state.timer_running = False

    # Layout the buttons
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if not st.session_state.timer_running:
            if st.button('Start Timer'):
                st.session_state.timer_running = True
                threading.Thread(target=start_timer, daemon=True).start()

        else:
            if st.button('Stop Timer'):
                st.session_state.timer_running = False

    with col2:
        if st.button('Reset Timer'):
            st.session_state.time_left = 30 * 60  # Reset to 30 minutes
            st.session_state.timer_running = False

    # Display the countdown timer
    minutes = st.session_state.time_left // 60
    seconds = st.session_state.time_left % 60
    st.write(f"### {minutes:02d}:{seconds:02d}")

    if st.session_state.time_left == 0:
        st.error("Time's up!")

# Page 1 - Topic Selection
def topic_selection():
    st.write("<h1 style='color: #FF6347;'>Extemp Speech Topics</h1>", unsafe_allow_html=True)

    topics_input = st.text_area("Enter your topics, each on a new line:", height=200)

    if st.button("Generate Topics"):
        topics = [topic.strip() for topic in topics_input.split('\n') if topic.strip()]

        if len(topics) < 3:
            st.error("Please enter at least 3 topics.")
        else:
            chosen_topics = random.sample(topics, 3)
            st.write("<h3>Here are your 3 randomly selected topics:</h3>", unsafe_allow_html=True)
            for i, topic in enumerate(chosen_topics, 1):
                st.write(f"{i}. {topic}")

            selected_topic = st.selectbox("Choose one topic for your extemp:", chosen_topics)
            
            if selected_topic:
                st.session_state.selected_topic = selected_topic
                st.session_state.screen = "timer"

# Page 2 - Timer Screen
def timer_screen():
    st.write(f"<h1 style='color: #008CBA; text-align: center;'>{st.session_state.selected_topic.upper()}</h1>", unsafe_allow_html=True)
    timer_function()

    if st.button("Back to Topic Selection"):
        st.session_state.screen = "topics"

# Main app logic (decides which screen to display)
def main():
    if 'screen' not in st.session_state:
        st.session_state.screen = "topics"

    if st.session_state.screen == "topics":
        topic_selection()
    elif st.session_state.screen == "timer":
        timer_screen()

# Run the app
main()
