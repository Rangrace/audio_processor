from openai import OpenAI
import pygame
import sounddevice as sd
from scipy.io.wavfile import write
from system_prompts import pharmacy


class Situation:
    def __init__(self, system_content):
        self.system_content = system_content
        self.client = OpenAI()
        self.chat_history = [{"role": "system", "content": self.system_content}]
        self.models = {"tts": "tts-1", "stt": "whisper-1", "llm": "gpt-4-turbo"}
        self.response_settings = {"max_tokens": 100, "temperature": 0.4}

    @staticmethod
    def record_audio(seconds, fs, channels):
        recording = sd.rec(int(seconds * fs), samplerate=fs, channels=channels)
        sd.wait()
        write("output.wav", fs, recording)

    def get_transcript_of_user_voice(self):
        with open("output.wav", "rb") as f:
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
            response_format="mp3",
            speed=1,
            input=response.choices[0].message.content
        )

        response.stream_to_file("output.mp3")

    @staticmethod
    def play_assistant_response() -> None:
        pygame.init()
        pygame.mixer.init()
        with open("output.mp3") as f:
            pygame.mixer.music.load(f)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

    def run(self):
        print("It's your turn")

        while True:
            # Get audio input from user
            self.record_audio(3, 44100, 2)

            # Get the transcription of the user audio input
            user_content = self.get_transcript_of_user_voice()

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
