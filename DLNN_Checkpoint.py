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
def recognize_speech_from_mic():
    with sr.Microphone() as source:
        st.write("Say something!")
        r.adjust_for_ambient_noise(source)
        audio_data = r.record(source, duration=10)
        st.write("Recognizing...")
        try:
            text = r.recognize_google(audio_data, language='en-US')
            st.write("You said: " + text)
            return text
        except sr.UnknownValueError:
            st.write("Google Web Speech could not understand audio")
            return ""
        except sr.RequestError as e:
            st.write(f"Could not request results from Google Web Speech service; {e}")
            return ""

# Function to preprocess text data
def preprocess_text(text):
    sentences = sent_tokenize(text)
    words = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word.lower() not in stop_words]
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    return sentences, words

# Streamlit app
def main():
    st.title("Text Processing and Speech Recognition Chatbot")
        
    # Text Data Input
    file_path = st.text_input("Enter the file path to load text:")
    if file_path:
        with open(file_path, 'r') as file:
            text = file.read()
        sentences, words = preprocess_text(text)
        st.write("Sentences:", sentences)
        st.write("Words:", words)
        df = pd.DataFrame(sentences, columns=["sentences"])
        st.write(df.head())
    
    # User Input for Chatbot
    user_input_type = st.radio("Choose input type:", ("Text Input", "Speech Input"))
    
    if user_input_type == "Text Input":
        user_input = st.text_input("You:")
        if user_input:
            response = preprocess_text(user_input)
            st.write("You:", user_input)
            st.markdown('---------------------------------')
            st.write("Writing Text:", response)
    
    elif user_input_type == "Speech Input":
        st.write("Click to start recording:")
        st.markdown('---------------------------------')
        st.write("You can try with this sentences : I am working on integrating speech recognition with a Streamlit app, adding text processing with NLTK, and a simple chatbot response")
        if st.button("Record"):
            transcript = recognize_speech_from_mic()
            if transcript:
                response = preprocess_text(transcript)
                st.write("Transcribed Text:", response)
                

if __name__ == "__main__":
    main()
