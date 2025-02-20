import streamlit as st
import random
import time

# Function to handle topic selection
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
                st.session_state.start_time = time.time()  # Set start time
                st.experimental_rerun()

# Function to handle the timer screen
def timer_screen():
    # Display the chosen topic in big letters
    st.write(f"<h1 style='color: #008CBA; text-align: center;'>{st.session_state.selected_topic.upper()}</h1>", unsafe_allow_html=True)
    
    # Calculate remaining time
    elapsed_time = int(time.time() - st.session_state.start_time)
    remaining_time = max(30 * 60 - elapsed_time, 0)  # 30 minutes in seconds
    
    # Display timer
    minutes, seconds = divmod(remaining_time, 60)
    st.write(f"<h2 style='text-align: center; font-size: 48px;'>{minutes:02d}:{seconds:02d}</h2>", unsafe_allow_html=True)
    
    # Progress bar
    progress = 1 - (remaining_time / (30 * 60))
    st.progress(progress)
    
    # Check if time's up
    if remaining_time <= 0:
        st.error("Time's up!")
    
    # Button to go back to topic selection
    if st.button("Back to Topic Selection"):
        st.session_state.screen = "topics"  # Go back to topic selection screen
        st.experimental_rerun()
    
    # Rerun the app every second to update the timer
    time.sleep(1)
    st.experimental_rerun()

# Main app logic (decides which screen to display)
def main():
    if 'screen' not in st.session_state:
        st.session_state.screen = "topics"  # Initial screen is topic selection

    if st.session_state.screen == "topics":
        topic_selection()
    elif st.session_state.screen == "timer":
        timer_screen()

# Run the app
if __name__ == "__main__":
    main()
