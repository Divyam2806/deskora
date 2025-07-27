from gtts import gTTS
import os
from playsound import playsound
import tempfile

def speak(text: str):
    # Convert text to speech using gTTS
    tts = gTTS(text=text, lang='en')

    # Save to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        filename = fp.name
    tts.save(filename)

    # Play the audio
    playsound(filename)

    # Clean up the temp file
    os.remove(filename)
