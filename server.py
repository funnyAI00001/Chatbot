from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from voice_chatbot import process_voice_input

app = Flask(__name__)
CORS(app)

@app.route('/process_voice_input', methods=['POST'])
# @cross_origin()
def handle_process_voice_input():
    voice_data_base64 = request.json['audio_data']
    response_audio_base64 = process_voice_input(voice_data_base64)
    return jsonify({'audio_data': response_audio_base64})

if __name__ == '__main__':
    app.run(debug = True)