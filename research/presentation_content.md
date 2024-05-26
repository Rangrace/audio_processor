Slide 1: 
Title: (bot name) Voicely - Revolutionizing Medical Audio Assistance with sts(speech to speech) Bots
Subtitle: Highly sensitive speech recognition assistance for Patients with Special Needs
Presented by: [Grace, Christian]

Slide 2 

Market Research and Persona: ( a msg to Christian: Persona is a way to bool down to the right painpoint. )

perSona: Emma's Daily Challenges

Emma's Story:

Emma Johansson, a 68-year-old stroke survivor, lives alone in Stockholm. She struggles with reading and writing, \n
and her speech impairment makes communication difficult. Every visit to the pharmacy is a challenge. She often has to repeat 
herself multiple times, feeling embarrassed and attracting unwanted attention from staff and customers. One day, after a particularly 
frustrating experience where she couldn’t make herself understood, she decided that she should avoiding going to public service places. 

C
S3 Painpoint:

Difficulties faced by patients with conditions like stroke or disabilities and illiterate individuals in accessing medical services.

Slide 4: Solution Overview
Title: Our Innovative Tech Solution
Content:

## High SpeechRecognition-Sensitivity Audio Bot
Understands and processes speech from patients with unique speech patterns, vocabulary and accents.
Tailored responses based on medical history and condition with embedded big data.
## Key Features (it can be another slide alone)
    - (Here we list libs and give a logic map of how libs work with each other based on the ppt I sent u and the file " intefgration.txt")

    - Scenario-focused interactions (pharmacy, hospital booking, elderly care).This makes tailored LLMs finetunning later. 
    - Real-time connection with medical databases using personal identifiers ( This bot should be able to read Medical record real-time and remove it for privacy.)
    - Ensured data privacy (no data storage post-conversation or sent to OpenAI, instead we send in incryted data after "cleaning" to LLMs). 

* We dont use Langchain or whole package of OpenAI, instead we processes data with scripts and have seperate embedded data from OpenAI and only send in 
current relavent data chunks and query to OpenAI or LLMs. We have control and transparency throughout the whole process. 


Slide 5: Technical Architecture

Components of the System:

1, PyAudio and Pydub for audio handling
2. Speech-to-Text (STT) methods like SR to understand and Convert audio
    with SR, DNNs is used to analyse smallest units of sound in frame (sound units, different from video frame)
            - RNN is used to predict the mostly like word from the audio input. 
            - LLMs is used to understand context 
            * Three mothods together, output the text. 

3,
we use spaCy for NLU(Natural Language understanding)
    #spaCy can handle large volumes of text quickly. 
    #Processes and understands the text to extract intents. 
    #can understand the sentiment (positive, negative, or neutral) of user.

4 LLms and embedded databases to Generate answers. 
    # Integration with medical databases,perssonal number, medical record, contacts and name is incryted for GDPR. This is why we work with our own seperate database. 

5 Text-to-Speech (TTS) models
    # There are many vals, for instance Google Text-to-Speech (gTTS) library, calls through goofle API. 

Workflow Overview:
Record -> Transcribe -> Process -> Respond -> Synthesize -> Play

6: Key selling points:
Title: Key Features

## High Sensitivity to Speech Variations:
Tailored to understand unclear speech post-stroke.

## Medical Scenario Focus:
Pharmacy, hospital booking, elderly care, etc.

## Real-Time Data Integration:
Real-time fetching relevant medical data.

## Privacy and Security:
Encryted data sent to LLms and no data storage after the conversation.

7  Benefits

For Patients:
    #Tailored Medical Assistance:
        Receive personalized, high-quality support based on individual medical history and needs.
    #Social comfort:
        Enjoy private, self-controlled communication, avoiding social discomfort and preserving confidence and dignity.
For Healthcare Providers:

    Cost Efficiency:
    Reduce labor costs by automating routine inquiries and basic support tasks.

8 future Features:

Title: Future Development: 

# Expansion to More Scenarios:
Emergency services, mental health support, etc.

# Enhanced Personalization and optimize real-time reading time(process)


# Continuous Learning:
Adapting to new speech patterns and accents and challenge in terms of speech recognition

