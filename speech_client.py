import requests
import streamlit as st
import speech_recognition as sr
from pathlib import Path
from openai import OpenAI
import pygame

def call_chat_completion(text, api_key):
    server_url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer"
    }
    data = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Task: As an assistant and answer the question."
                    },
                    {
                        "type": "text",
                        "text": text
                    }
                ]
            }
        ],
        "max_tokens": 3000
    }
    response = requests.post(server_url, headers=headers, json=data)
    res = response.json()
    content = res["choices"][0]["message"]["content"]
    return content

pygame.mixer.init()

st.title('Your Voice Assistant')

if st.button("Start Speech Recognition"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        st.write("Processing...")
        
    try:
        text = recognizer.recognize_google(audio)
        st.write("You said:", text)
        # Provide your OpenAI API key here
        scores = call_chat_completion(text, "YOUR_OPEN_AI_KEY")
        client = OpenAI(api_key="YOUR_OPEN_AI_KEY")
        speech_file_path = Path(__file__).parent / "speech.mp3"
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=scores
        )
        response.stream_to_file(speech_file_path)
        st.write("Your Assistant:")
        st.write(scores)
        
        # Play the generated speech
        
        pygame.mixer.music.load(speech_file_path)
        pygame.mixer.music.play()

    except sr.UnknownValueError:
        st.write("Sorry, could not understand audio.")
    except sr.RequestError as e:
        st.write("Could not request results; {0}".format(e))
