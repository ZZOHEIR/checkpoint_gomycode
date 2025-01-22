import os
import nltk
import pandas as pd
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import streamlit as st
import speech_recognition as sr

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Initialize the recognizer
r = sr.Recognizer()

# Function to recognize speech from microphone

def transcribe_speech(audio_data, api_choice):
    try:
        if api_choice == "Google":
            text = r.recognize_google(audio_data)
        elif api_choice == "Wit.ai":
            text = r.recognize_wit(audio_data, key="YOUR_WIT.AI_API_KEY")
        elif api_choice == "IBM":
            text = r.recognize_ibm(audio_data, username="YOUR_IBM_USERNAME", ibm_password="YOUR_IBM_PASSWORD")
        elif api_choice == "Microsoft":
            text = r.recognize_bing(audio_data, key="YOUR_MICROSOFT_KEY")
        elif api_choice == "Sphinx":
            text = r.recognize_sphinx(audio_data)
        return text
    except sr.UnknownValueError:
        st.write("Speech was not understood")
    except sr.RequestError as e:
        st.write(f"Error with the API request; {e}")
    return ""

def recognize_speech_from_mic(api_choice):
    global is_recording, is_paused
    with sr.Microphone() as source:
        st.write("Say something!")
        r.adjust_for_ambient_noise(source)
        audio_data = r.record(source, duration=15)
        st.write("Recognizing...")
        text = transcribe_speech(audio_data, api_choice)
        if text:
            st.write("You said: " + text)
            with open("transcribed_text.txt", "a") as f:
                f.write(text + "\n")
# Function to preprocess text data
def preprocess_text(text):
    sentences = sent_tokenize(text)
    words = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word.lower() not in stop_words]
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    return sentences, words


def main():
    st.title("Text Processing and Speech Recognition Chatbot - API selection")
    st.write('Some API need a Key password to work, please check the documentation of the API you want to use')
    st.write('Install PocketSphinx: You need to ensure that PocketSphinx and its dependencies are installed : # pip install pocketsphinx')
    user_input_type = st.radio("Choose API:", ("Google", "Wit.ai", "IBM", "Microsoft", "Sphinx"))
    # User Input for Chatbot
    
    if st.button("Record") :
        transcript = recognize_speech_from_mic(user_input_type)
        if transcript:
            response = preprocess_text(transcript)
            return response
                

if __name__ == "__main__":
    main()


