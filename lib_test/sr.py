import speech_recognition as sr

# Function to transcribe audio to text
def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()
    audio_data = sr.AudioFile(audio_file)

    with audio_data as source:
        audio_text = recognizer.record(source)

    try:
        recognized_text = recognizer.recognize_google(audio_text)
        return recognized_text
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand what you said."
    except sr.RequestError:
        return "Sorry, I'm having trouble processing your request right now."

transcribed_text = transcribe_audio('audio.wav')
print("Transcribed text:", transcribed_text)
