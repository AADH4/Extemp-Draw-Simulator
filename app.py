import streamlit as st
import time
from streamlit_custom_notification_box import custom_notification_box

def timer_screen():
    st.write(f"<h1 style='color: #008CBA; text-align: center;'>{st.session_state.selected_topic.upper()}</h1>", unsafe_allow_html=True)
    
    elapsed_time = int(time.time() - st.session_state.start_time)
    remaining_time = max(30 * 60 - elapsed_time, 0)
    
    minutes, seconds = divmod(remaining_time, 60)
    st.write(f"<h2 style='text-align: center; font-size: 48px;'>{minutes:02d}:{seconds:02d}</h2>", unsafe_allow_html=True)
    
    progress = 1 - (remaining_time / (30 * 60))
    st.progress(progress)
    
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
    
    # Define warning messages and times
    warnings = {
        600: "10 minutes remaining!",
        300: "5 minutes remaining!",
        0: "Time's up!"
    }
    
    # Check for warnings
    for warn_time, message in warnings.items():
        if remaining_time == warn_time:
            st.markdown(f"<div class='warning-box'>{message}</div>", unsafe_allow_html=True)
            
            # Add custom notification box
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
            
            # Play notification sound
            st.audio("https://www.soundjay.com/buttons/sounds/button-3.mp3", auto_play=True)
    
    if remaining_time <= 0:
        st.balloons()
    
    if st.button("Reset and Start Over"):
        st.session_state.form_submitted = False
        st.session_state.topic_selected = False
        st.session_state.screen = "topics"
        st.rerun()
    
    time.sleep(1)
    st.rerun()
