import json

from playsound import playsound

from pathlib import Path
import openai

with open('cred/additional_keys.json', 'r') as file:
    keys = json.load(file)

# Access the keys
gpt_key = keys['gpt_key']

openai.api_key = gpt_key

from openai import OpenAI

client = OpenAI(api_key=openai.api_key)


def voice_to_speech(text):
    speech_file_path = Path(__file__).parent / "speech.mp3"
    voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
    voice = 'nova' # change to nova onyx for similar to mine
    response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=text,
        speed=1)
    response.stream_to_file(speech_file_path)
    playsound(speech_file_path, block=True)

if __name__ == '__main__':
    voice_to_speech(''' ''')