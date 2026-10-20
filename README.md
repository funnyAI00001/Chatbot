# Chatbot

A voice chatbot that runs in the browser. You click a button, say something, and it talks back. Your speech goes to Google Cloud Speech-to-Text, the text goes to OpenAI for a reply, and the reply comes back as audio from Google Cloud Text-to-Speech.

I built this as a personal project to try out a full voice loop (speech in, AI reply, speech out) with a small, simple stack. It's for anyone who wants a minimal example of wiring these services together, or a starting point for their own voice assistant.

## How it works

```
Browser (index.html)
  │  records your voice with MediaRecorder
  │  sends it as base64 to POST /process_voice_input
  ▼
Flask server (server.py)
  ▼
voice_chatbot.py
  1. Google Cloud Speech-to-Text  →  your words as text
  2. OpenAI completion            →  reply text
  3. Google Cloud Text-to-Speech  →  reply as MP3
  ▼
Browser plays your recording and the spoken reply
```

## Built with

- **Python 3** and **Flask** (with flask-cors) for the backend
- **OpenAI API** for the chatbot replies
- **Google Cloud Speech-to-Text** and **Text-to-Speech** (GCP)
- **HTML, JavaScript and Bootstrap** for the frontend, with the browser MediaRecorder API for recording

## Project structure

```
.
├── index.html          # Frontend page with Start/Stop recording buttons and audio players
├── server.py           # Flask app, exposes POST /process_voice_input
├── voice_chatbot.py    # Speech-to-text, OpenAI call, text-to-speech
├── css/                # Bootstrap and custom styles
├── fonts/trade-winds/  # Title font (SIL Open Font License)
├── images/             # Page images
├── update/             # Screenshots
├── back.png            # Background image
└── LICENSE
```

## Getting started

### What you need

- Python 3.8 or newer
- An OpenAI API key
- A Google Cloud project with the **Speech-to-Text** and **Text-to-Speech** APIs turned on, plus a service account key file (JSON)

### 1. Clone the repo

```bash
git clone https://github.com/funnyAI00001/Chatbot.git
cd Chatbot
```

### 2. Install dependencies

```bash
python -m venv venv
source venv/bin/activate      # on Windows: venv\Scripts\activate
pip install flask flask-cors "openai<1.0" google-cloud-speech google-cloud-texttospeech
```

The code uses the older OpenAI Python SDK (`openai.Completion`), so it needs a version below 1.0 for now. Moving to the current SDK is on the roadmap below.

### 3. Add your keys

These files are in `.gitignore` and should never be committed.

Create `config.py` in the project root:

```python
openai_key = "your-openai-api-key"
```

Put your Google Cloud service account key in the project root as `credentials.json`.

### 4. Run the server

```bash
python server.py
```

Flask starts on `http://localhost:5000`.

### 5. Open the page

Open `index.html` in your browser (or serve the folder with `python -m http.server 8000` and go to `http://localhost:8000`). Allow microphone access, click **Start Recording**, talk, then click **Stop Recording**. Your recording and the bot's spoken reply show up in the two audio players.

## API

### `POST /process_voice_input`

Request:

```json
{ "audio_data": "<base64-encoded audio>" }
```

Response:

```json
{ "audio_data": "<base64-encoded MP3 of the reply>" }
```

## Known issues

- The OpenAI model it calls (`text-davinci-002`) has been retired, so replies will fail until the code moves to a current model.
- Browsers usually record in WebM/Opus, but the speech-to-text config expects 16 kHz LINEAR16 audio. That mismatch can cause empty transcripts.
- The server URL is hardcoded to `http://localhost:5000` in `index.html`.
- There's no error handling yet, so a failed API call just breaks the request.

## Roadmap

- [ ] Move to the current OpenAI Python SDK and a chat model
- [ ] Fix the audio format mismatch (record or convert to a format Speech-to-Text accepts)
- [ ] Keep conversation history so the bot remembers earlier turns
- [ ] Show the transcript and reply as text alongside the audio
- [ ] Add error handling and loading states in the UI
- [ ] Move keys to environment variables and add `config.example.py` and `requirements.txt`
- [ ] Make the server URL configurable
- [ ] Add tests for the server and the speech pipeline
- [ ] Add a simple deploy setup (Docker)

## License

MIT. See [LICENSE](LICENSE).
