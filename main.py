from openai import OpenAI
import wave
import sys
import pyaudio
from pydub import AudioSegment
from pydub.playback import play
from system_prompts import pharmacy


class Situation:
    def __init__(self, system_content):
        self.system_content = system_content
        self.client = OpenAI()
        self.chat_history = [{"role": "system", "content": self.system_content}]
        self.models = {"tts": "tts-1", "stt": "whisper-1", "llm": "gpt-4-turbo"}
        self.response_settings = {"max_tokens": 100, "temperature": 0.4}

    @staticmethod
    def record_audio():
        # record
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1 if sys.platform == 'darwin' else 2
        RATE = 44100
        RECORD_SECONDS = 5

        with wave.open('user.wav', 'wb') as wf:
            p = pyaudio.PyAudio()
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)

            stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True)

            print('Recording...')
            for _ in range(0, RATE // CHUNK * RECORD_SECONDS):
                wf.writeframes(stream.read(CHUNK))
            print('Done')

            stream.close()
            p.terminate()

    def get_transcript_of_user_voice(self):
        with open("user.wav", "rb") as f:
            transcription = self.client.audio.transcriptions.create(
                model=self.models.get("stt"),
                file=f
            )
            return transcription.text

    def get_response_from_llm(self):
        response = self.client.chat.completions.create(
            model=self.models.get("llm"),
            messages=self.chat_history,
            max_tokens=self.response_settings.get("max_tokens"),
            temperature=self.response_settings.get("temperature"),
        )
        return response

    def create_speach_from_assistant_response(self, response) -> None:
        response = self.client.audio.speech.create(
            model=self.models.get("tts"),
            voice="alloy",
            response_format="wav",
            speed=1,
            input=response.choices[0].message.content
        )

        response.stream_to_file("assistant.wav")

    @staticmethod
    def play_assistant_response() -> None:
        sound = AudioSegment.from_wav('assistant.wav')
        play(sound)

    def run(self):
        print("It's your turn")

        user_content = ""
        while user_content != "Finished.":
            # Get audio input from user
            self.record_audio()

            # Get the transcription of the user audio input
            user_content = self.get_transcript_of_user_voice()

            if user_content != "Finished":

                # Compose the user message
                user_message = {"role": "user", "content": user_content}

                # Add the user message to the chat history
                self.chat_history.append(user_message)

                # Get a text response from the model
                response = self.get_response_from_llm()

                # Compose the assistant message
                assistant_message = {"role": "assistant", "content": response.choices[0].message.content}

                # Add the assistant message to the chat history
                self.chat_history.append(assistant_message)

                # Create speach from the assistant response
                self.create_speach_from_assistant_response(response)

                # Play the response
                self.play_assistant_response()


i = Situation(pharmacy)
i.run()
