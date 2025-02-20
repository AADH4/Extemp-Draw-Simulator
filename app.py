import streamlit as st
import random
import time

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
                if st.button("Confirm Selection and Start Prep"):
                    st.session_state.screen = "timer"
                    st.session_state.start_time = time.time()
                    st.rerun()

def timer_screen():
    st.write(f"<h1 style='color: #008CBA; text-align: center;'>{st.session_state.selected_topic.upper()}</h1>", unsafe_allow_html=True)
    
    elapsed_time = int(time.time() - st.session_state.start_time)
    remaining_time = max(30 * 60 - elapsed_time, 0)
    
    minutes, seconds = divmod(remaining_time, 60)
    st.write(f"<h2 style='text-align: center; font-size: 48px;'>{minutes:02d}:{seconds:02d}</h2>", unsafe_allow_html=True)
    
    progress = 1 - (remaining_time / (30 * 60))
    st.progress(progress)
    
    if remaining_time <= 0:
        st.error("Time's up!")
        st.balloons()
    elif remaining_time == 5 * 60:
        st.warning("5 minutes remaining!")
    elif remaining_time == 10 * 60:
        st.info("10 minutes remaining!")
    
    if st.button("Back to Topic Selection"):
        st.session_state.screen = "topics"
        st.rerun()
    
    time.sleep(1)
    st.rerun()

def main():
    if 'screen' not in st.session_state:
        st.session_state.screen = "topics"

    if st.session_state.screen == "topics":
        topic_selection()
    elif st.session_state.screen == "timer":
        timer_screen()

if __name__ == "__main__":
    main()
