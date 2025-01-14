import streamlit as st
import speech_recognition as sr
from textblob import TextBlob  # For sentiment analysis
import pyttsx3  # For text-to-speech

def main():
    # Page configuration
    st.set_page_config(page_title="Voice Feedback System", layout="centered")

    # Custom CSS for styling
    st.markdown(
        """
        <style>
        body {
            font-family: 'Arial', sans-serif;
        }
        .header {
            background-color: #007acc;
            padding: 20px;
            color: white;
            text-align: center;
            font-size: 24px;
            border-radius: 10px;
        }
        .box {
            background-color: #f7f7f7;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
        }
        .btn {
            background-color: #007acc;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
        }
        .btn:hover {
            background-color: #005fa3;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Header
    st.markdown('<div class="header">Voice Feedback System</div>', unsafe_allow_html=True)

    # Main layout
    st.markdown("<div class='box' style='text-align: center;'>", unsafe_allow_html=True)
    st.markdown("### Voice Input")

    if st.button("🎤 Speak"):
        user_input = speech_to_text()
        if user_input:
            sentiment = analyze_text(user_input)

            # Formulate Response
            if sentiment == "POSITIVE":
                response = "Thank you for your positive feedback! I appreciate it."
            elif sentiment == "NEGATIVE":
                response = "I'm sorry to hear that. How can I help you further?"
            else:
                response = "Thank you for sharing your thoughts."

            text_to_speech(response)  # Speak the response
            st.write("Model Response:", response)
        else:
            st.error("No input detected. Please try speaking again.")
    st.markdown("</div>", unsafe_allow_html=True)


def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)
            st.info("Processing...")
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            st.error("Could not understand your voice. Please try again.")
        except sr.RequestError as e:
            st.error(f"Could not request results from Google Speech Recognition service; {e}")
        return None


from textblob import TextBlob


def analyze_text(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity

    if polarity > 0.2:  # Positive threshold
        return "POSITIVE"
    elif polarity < -0.2:  # Negative threshold
        return "NEGATIVE"
    else:
        return "NEUTRAL"


def text_to_speech(response):
    engine = pyttsx3.init()
    engine.say(response)
    engine.runAndWait()


if __name__ == "__main__":
    main()