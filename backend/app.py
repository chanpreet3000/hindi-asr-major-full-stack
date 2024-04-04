from flask import Flask, request, jsonify 
import os 
import requests 
import json 
from pydub import AudioSegment 
from flask_cors import CORS 
import io 
import time
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__) 
CORS(app) 

API_URL = os.environ.get("API_URL")
headers = {"Authorization": "Bearer " + str(os.environ.get("TOKEN"))}

@app.route('/upload', methods=['POST']) 
def upload(): 
    if 'file' not in request.files: 
        return jsonify({'error': 'No audio file uploaded'}), 400 
     
    audio_file = request.files['file'] 
    if audio_file.filename == '': 
        return jsonify({'error': 'No selected file'}), 400 
     
    current_time_ms = str(int(time.time() * 1000))
    org_directory = './audio/org/'
    gen_directory = './audio/gen/'
    
    # Ensure the directories exist
    for directory in [org_directory, gen_directory]:
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    # Save original audio file
    file_name = os.path.join(org_directory, current_time_ms + os.path.splitext(audio_file.filename)[1])
    audio_file.save(file_name)
    
    # Convert to FLAC
    sound = AudioSegment.from_mp3(file_name)
    flac_file = os.path.join(gen_directory, current_time_ms + '.flac')
    sound.export(flac_file, format="flac")
    
    return output(flac_file)
 
@app.route('/convert', methods=['POST']) 
def convert_blob_to_wav(): 
    if 'audioFile' not in request.files: 
        return jsonify({'error': 'No voice blob uploaded'}), 400 
     
    audioFile = request.files['audioFile'] 
    if audioFile.filename == '': 
        return jsonify({'error': 'No selected blob'}), 400 
 
    try: 
        # Read the blob into an AudioSegment 
        audio = AudioSegment.from_file(io.BytesIO(audioFile.read())) 
        # Convert to flac format 
        audiofile = io.BytesIO() 
        audio.export(audiofile, format='flac')
    
        current_time_ms = str(int(time.time() * 1000))
        directory = './audio/gen/'
        if not os.path.exists(directory):
            os.makedirs(directory)
        flac_file = os.path.join(directory, current_time_ms + '.flac')
        with open(flac_file, 'wb') as file:
            file.write(audiofile.read())
        return output(flac_file)
 
    except Exception as e: 
        return jsonify({'error': f'Conversion failed: {str(e)}'}), 500 
 


def output(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    text = response.json()
    return jsonify({ 
        "data":text["text"],
    }),200 
 
if __name__ == '__main__': 
    app.run(port=5000, debug=True)