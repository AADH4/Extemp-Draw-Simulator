import streamlit as st
import time
from streamlit_custom_notification_box import custom_notification_box

# Initialize session state variables
if 'selected_topic' not in st.session_state:
    st.session_state.selected_topic = ""  # Or some other appropriate default value
if 'start_time' not in st.session_state:
    st.session_state.start_time = 0
if 'last_update' not in st.session_state:
    st.session_state.last_update = 0
if 'warnings_shown' not in st.session_state:
    st.session_state.warnings_shown = set()


def timer_screen():
    if 'selected_topic' in st.session_state:
        st.write(f"<h1 style='color: #008CBA; text-align: center;'>{st.session_state.selected_topic.upper()}</h1>", unsafe_allow_html=True)
    else:
        st.write("<h1 style='color: #008CBA; text-align: center;'>No Topic Selected</h1>", unsafe_allow_html=True)
    
    current_time = time.time()
    elapsed_time = int(current_time - st.session_state.start_time)
    remaining_time = max(30 * 60 - elapsed_time, 0)
    
    # Update every second instead of constantly
    if current_time - st.session_state.last_update >= 1:
        st.session_state.last_update = current_time
        
        minutes, seconds = divmod(remaining_time, 60)
        time_display = st.empty()
        time_display.write(f"<h2 style='text-align: center; font-size: 48px;'>{minutes:02d}:{seconds:02d}</h2>", unsafe_allow_html=True)
        
        progress = 1 - (remaining_time / (30 * 60))
        progress_bar = st.empty()
        progress_bar.progress(progress)
        
        # Check for warnings
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
                custom_notification_box(
                    icon='warning',
                    textDisplay=message,
                    styles=styles,
                    key=f"warning_{warn_time}"
                )
                
                st.audio("https://www.soundjay.com/buttons/sounds/button-3.mp3", auto_play=True)
        
        if remaining_time <= 0 and 'balloons_shown' not in st.session_state:
            st.balloons()
            st.session_state.balloons_shown = True
    
    if st.button("Reset and Start Over"):
        for key in ['form_submitted', 'topic_selected', 'warnings_shown', 'balloons_shown', 'last_update', 'selected_topic','start_time']:
            if key in st.session_state:
                del st.session_state[key]
        st.session_state.screen = "topics"
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

timer_screen()
