from openai import OpenAI
import wave
import sys
import pyaudio
from pydub import AudioSegment
from pydub.playback import play
from system_prompts import pharmacy


class Situation:
    """
    This class is meant to be instantiated with different state/system_content depending on what situation the user
    wants to practice.
    If for instance the user wants to practice going to the pharmacy, then this class should be
    instantiated with the relevant system content for that.
    This class also holds all the necessary methods and the main loop.
    """

    def __init__(self, system_content):
        # The system content or "state"
        self.system_content = system_content
        # The instance of OpenAI
        self.client = OpenAI()
        # The chat history, it gives the llm model a "memory" of what has been said
        self.chat_history = [{"role": "system", "content": self.system_content}]
        # The models used
        self.models = {"tts": "tts-1", "stt": "whisper-1", "llm": "gpt-4o"}
        # The response settings passed to the llm model
        self.response_settings = {"max_tokens": 300, "temperature": 0.2}

    @staticmethod
    def record_audio():
        """Record the user voice and save it in a wav file"""

        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1 if sys.platform == 'darwin' else 2
        RATE = 44100
        RECORD_SECONDS = 6

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
        """Get a transcript of the user's voice message"""

        with open("user.wav", "rb") as f:
            transcription = self.client.audio.transcriptions.create(
                model=self.models.get("stt"),
                file=f
            )
            return transcription.text

    def get_response_from_llm(self):
        """Send the transcript from the previous step into the llm and receive a response"""

        response = self.client.chat.completions.create(
            model=self.models.get("llm"),
            messages=self.chat_history,
            max_tokens=self.response_settings.get("max_tokens"),
            temperature=self.response_settings.get("temperature"),
        )
        return response

    def moderation(self, content):

        response = self.client.moderations.create(input=content)

        output = response.results[0]

        return output.flagged

    def create_speach_from_assistant_response(self, content) -> None:
        """Create a voice message from the llm response"""

        response = self.client.audio.speech.create(
            model=self.models.get("tts"),
            voice="nova",
            response_format="wav",
            speed=1,
            input=content
        )

        response.stream_to_file("assistant.wav")

    @staticmethod
    def play_assistant_response() -> None:
        """Play the llm response"""

        sound = AudioSegment.from_wav('assistant.wav')
        play(sound)

    def run(self):
        """The main loop. It plays as long as 'Finished' is not uttered by the user"""

        first_message = "Welcome! How can i help you?"
        self.create_speach_from_assistant_response(first_message)
        self.play_assistant_response()
        self.chat_history.append({"role": "assistant", "content": first_message})

        while True:
            # Get audio input from user
            self.record_audio()

            # Get the transcription of the user audio input
            user_content = self.get_transcript_of_user_voice()

            # Compose the user message
            user_message = {"role": "user", "content": user_content}

            # Add the user message to the chat history
            self.chat_history.append(user_message)

            # Get a text response from the model
            response = self.get_response_from_llm()

            # Moderation filter
            result = self.moderation(response.choices[0].message.content)

            # Compose the assistant message
            assistant_message = {"role": "assistant", "content": response.choices[0].message.content}

            # Add the assistant message to the chat history
            self.chat_history.append(assistant_message)

            # Create speach from the assistant response
            self.create_speach_from_assistant_response(response.choices[0].message.content)

            # Play the response
            self.play_assistant_response()


i = Situation(pharmacy)
i.run()
