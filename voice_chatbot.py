import io
import os
import json
import openai
import base64
from google.cloud import texttospeech, speech
from config import openai_key

# Set your Google Cloud and OpenAI API keys
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credentials.json'
openai.api_key = openai_key

tts_client = texttospeech.TextToSpeechClient()
stt_client = speech.SpeechClient()

def synthesize_text(text):
    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = tts_client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)
    return response.audio_content

def transcribe_audio(audio):
    config = speech.RecognitionConfig(encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16, sample_rate_hertz=16000, language_code="en-US")
    response = stt_client.recognize(config=config, audio=speech.RecognitionAudio(content=audio))
    return response.results[0].alternatives[0].transcript if response.results else ""

def chat_gpt4(prompt):
    response = openai.Completion.create(engine="text-davinci-002", prompt=prompt, max_tokens=100, n=1, stop=None, temperature=0.8)
    return response.choices[0].text.strip()

def process_voice_input(voice_data_base64):
    audio_bytes = base64.b64decode(voice_data_base64)
    text_input = transcribe_audio(audio_bytes)
    chat_response = chat_gpt4(text_input)
    audio_response = synthesize_text(chat_response)
    
    return base64.b64encode(audio_response).decode('utf-8')