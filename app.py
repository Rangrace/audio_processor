from flask import Flask, render_template, request, send_file
from openai import OpenAI
import datetime
from files.assistant import Assistant
from files.prompts import pharmacy_prompt
from files.db import transfer_to_db

app = Flask(__name__)

values_assistant_creation = {
    "name": "Pharmacy",
    "prompt": pharmacy_prompt,
    "tools": [{"type": "code_interpreter"}],
    "model": "gpt-4o",
    "temperature": 0.4
}

# create a client
client = OpenAI()

# create an assistant
assistant = Assistant(values_assistant_creation, client).create_assistant()

# create a thread
thread = client.beta.threads.create()


def moderate(content, client):
    """Moderate the assistant content before presented to the user"""

    response = client.moderations.create(input=content)
    output = response.results[0]
    return output.flagged


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route('/write', methods=['GET', 'POST'])
def write():
    """Write mode"""

    # If request.method was POST
    if request.method == 'POST':
        # Get user content
        user_content = request.form['user_content']

        # Get date
        date = datetime.date.today()

        # Send to db
        transfer_to_db({"date": date, "user_content": user_content})

        # Add a message to thread
        message = client.beta.threads.messages.create(thread_id=thread.id, role="user", content=user_content)

        # Run thread with assistant
        run = client.beta.threads.runs.create_and_poll(thread_id=thread.id, assistant_id=assistant.id)

        # Get response
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        ai_response = messages.data[0].content[0].text.value

        # Moderate
        result = moderate(ai_response, client)

        if not result:
            return render_template('write.html', response=ai_response)

    # If request.method was GET
    else:
        return render_template('write.html')


@app.route('/talk', methods=['GET', 'POST'])
def talk():
    """Talk mode"""

    # If it was a POST request
    if request.method == 'POST':
        # Get the audio from request.files
        audio_file = request.files['audio']

        # Save the audio to a wav file
        audio_file.save("user_speech.wav")

        # Get a transcription of the user message
        with open("user_speech.wav", "rb") as f:
            transcription = client.audio.transcriptions.create(model="whisper-1", file=f).text

        # Get date
        date = datetime.date.today()

        # Send to db
        transfer_to_db({"date": date, "user_content": transcription})

        # Add a message to thread
        message = client.beta.threads.messages.create(thread_id=thread.id, role="user", content=transcription)

        # Run thread with assistant
        run = client.beta.threads.runs.create_and_poll(thread_id=thread.id, assistant_id=assistant.id)

        # Get response
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        ai_response = messages.data[0].content[0].text.value

        # Moderate
        result = moderate(ai_response, client)

        # Get the AI response as speech and save it in a wav file
        if not result:
            response = client.audio.speech.create(
                model="tts-1",
                voice="nova",
                response_format="wav",
                speed=1,
                input=ai_response
            )

            response.stream_to_file("assistant.wav")

            # Send the file back to the frontend
            return send_file("assistant.wav", mimetype='audio/wav')

    # If request.method was GET
    else:
        return render_template('talk.html')


if __name__ == '__main__':
    app.run(debug=True)
