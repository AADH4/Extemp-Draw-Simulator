import streamlit as st
import time
import random
from streamlit_custom_notification_box import custom_notification_box

# Initialize session state variables
if 'screen' not in st.session_state:
    st.session_state.screen = "input"
if 'topics' not in st.session_state:
    st.session_state.topics = []
if 'selected_topics' not in st.session_state:
    st.session_state.selected_topics = []
if 'selected_topic' not in st.session_state:
    st.session_state.selected_topic = ""
if 'start_time' not in st.session_state:
    st.session_state.start_time = 0
if 'last_update' not in st.session_state:
    st.session_state.last_update = 0
if 'warnings_shown' not in st.session_state:
    st.session_state.warnings_shown = set()

def input_screen():
    st.title("Extemp Topic Input")
    topics_input = st.text_area("Enter your topics, one per line:")
    if st.button("Submit Topics"):
        st.session_state.topics = [topic.strip() for topic in topics_input.split('\n') if topic.strip()]
        st.session_state.screen = "selection"
        st.rerun()

def selection_screen():
    st.title("Topic Selection")
    if not st.session_state.selected_topics:
        st.session_state.selected_topics = random.sample(st.session_state.topics, min(3, len(st.session_state.topics)))
    
    st.write("Please select one of the following topics:")
    selected_topic = st.selectbox("Choose your topic:", st.session_state.selected_topics)
    
    if st.button("Confirm Selection"):
        st.session_state.selected_topic = selected_topic
        st.session_state.screen = "confirmation"
        st.rerun()

def confirmation_screen():
    st.title("Confirmation")
    st.write(f"You have selected: {st.session_state.selected_topic}")
    st.write("Are you ready to begin your prep time?")
    if st.button("Start Prep"):
        st.session_state.start_time = time.time()
        st.session_state.screen = "timer"
        st.rerun()

def timer_screen():
    st.write(f"<h1 style='color: #008CBA; text-align: center;'>{st.session_state.selected_topic.upper()}</h1>", unsafe_allow_html=True)
    
    current_time = time.time()
    elapsed_time = int(current_time - st.session_state.start_time)
    remaining_time = max(30 * 60 - elapsed_time, 0)
    
    minutes, seconds = divmod(remaining_time, 60)
    st.write(f"<h2 style='text-align: center; font-size: 48px;'>{minutes:02d}:{seconds:02d}</h2>", unsafe_allow_html=True)
    
    progress = 1 - (remaining_time / (30 * 60))
    st.progress(progress)
    
    warnings = {
        600: "10 minutes remaining!",
        300: "5 minutes remaining!",
        0: "Time's up!"
    }
    
    for warn_time, message in warnings.items():
        if remaining_time <= warn_time and warn_time not in st.session_state.warnings_shown:
            st.session_state.warnings_shown.add(warn_time)
            st.markdown(f"<div class='warning-box'>{message}</div>", unsafe_allow_html=True)
            
            styles = {
                'material-icons': {'color': 'orange'},
                'text-icon-link-close-container': {'box-shadow': '#ff9800 0px 4px'},
                'notification-text': {'font-size': '18px'},
            }
            
            try:
                custom_notification_box(
                    icon='warning',
                    textDisplay=message,
                    styles=styles,
                    key=f"warning_{warn_time}"
                )
            except Exception as e:
                st.error(f"Error in custom_notification_box: {str(e)}")
                st.warning(message)
            
            st.audio("https://www.soundjay.com/buttons/sounds/button-3.mp3", auto_play=True)
    
    if remaining_time <= 0 and 'balloons_shown' not in st.session_state:
        st.balloons()
        st.session_state.balloons_shown = True
    
    if st.button("Reset and Start Over"):
        for key in ['screen', 'topics', 'selected_topics', 'selected_topic', 'start_time', 'last_update', 'warnings_shown', 'balloons_shown']:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()
    
    time.sleep(1)
    st.rerun()

# Add custom styling for warnings
st.markdown("""
<style>
.warning-box {
    background-color: #FFA500;
    color: white;
    padding: 10px;
    border-radius: 5px;
    font-size: 18px;
    text-align: center;
    margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

# Main app logic
if st.session_state.screen == "input":
    input_screen()
elif st.session_state.screen == "selection":
    selection_screen()
elif st.session_state.screen == "confirmation":
    confirmation_screen()
elif st.session_state.screen == "timer":
    timer_screen()
