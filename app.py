import streamlit as st
import random

# JavaScript Timer Embed
timer_html = """
<html>
    <head>
        <script>
            var timeLeft = 30 * 60;  // 30 minutes in seconds
            var timer;
            var timerRunning = false;
            function startTimer() {
                if (!timerRunning) {
                    timerRunning = true;
                    timer = setInterval(function() {
                        var minutes = Math.floor(timeLeft / 60);
                        var seconds = timeLeft % 60;
                        document.getElementById("timerDisplay").innerHTML = minutes + ":" + (seconds < 10 ? "0" : "") + seconds;
                        if (timeLeft <= 0) {
                            clearInterval(timer);
                            alert("Time's up!");
                            timerRunning = false;
                        } else {
                            timeLeft--;
                        }
                    }, 1000);
                }
            }
            function resetTimer() {
                clearInterval(timer);
                timeLeft = 30 * 60;
                document.getElementById("timerDisplay").innerHTML = "30:00";
                timerRunning = false;
            }
            function stopTimer() {
                clearInterval(timer);
                timerRunning = false;
            }
        </script>
    </head>
    <body>
        <div style="text-align: center; font-size: 40px; color: #FF6347;">
            <div id="timerDisplay">30:00</div>
            <br>
            <button onclick="startTimer()">Start Timer</button>
            <button onclick="stopTimer()">Stop Timer</button>
            <button onclick="resetTimer()">Reset Timer</button>
        </div>
    </body>
</html>
"""

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

# Function to handle the timer screen
def timer_screen():
    # Display the chosen topic in big letters
    st.write(f"<h1 style='color: #008CBA; text-align: center;'>{st.session_state.selected_topic.upper()}</h1>", unsafe_allow_html=True)
    
    # Embed the JavaScript timer
    st.markdown(timer_html, unsafe_allow_html=True)

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
