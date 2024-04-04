from flask import Flask, request, jsonify
import os
import requests
import json
from pydub import AudioSegment
from flask_cors import CORS
import io
import time
from dotenv import load_dotenv
from model import get_is_in_danger
from flask_mail import Mail, Message


load_dotenv()

app = Flask(__name__)
CORS(app)

app.config["MAIL_SERVER"] = str(os.environ.get("MAIL_SERVER"))
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USERNAME"] = str(os.environ.get("MAIL_USERNAME"))
app.config["MAIL_PASSWORD"] = str(os.environ.get("MAIL_PASSWORD"))
mail = Mail(app)

API_URL = os.environ.get("API_URL")
headers = {"Authorization": "Bearer " + str(os.environ.get("TOKEN"))}


@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No audio file uploaded"}), 400

    audio_file = request.files["file"]
    if audio_file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    current_time_ms = str(int(time.time() * 1000))
    org_directory = "./audio/org/"
    gen_directory = "./audio/gen/"

    # Ensure the directories exist
    for directory in [org_directory, gen_directory]:
        if not os.path.exists(directory):
            os.makedirs(directory)

    # Save original audio file
    file_name = os.path.join(
        org_directory, current_time_ms + os.path.splitext(audio_file.filename)[1]
    )
    audio_file.save(file_name)

    # Convert to FLAC
    sound = AudioSegment.from_mp3(file_name)
    flac_file = os.path.join(gen_directory, current_time_ms + ".flac")
    sound.export(flac_file, format="flac")

    return output(flac_file)


@app.route("/convert", methods=["POST"])
def convert_blob_to_wav():
    if "audioFile" not in request.files:
        return jsonify({"error": "No voice blob uploaded"}), 400

    audioFile = request.files["audioFile"]
    if audioFile.filename == "":
        return jsonify({"error": "No selected blob"}), 400

    try:
        # Read the blob into an AudioSegment
        audio = AudioSegment.from_file(io.BytesIO(audioFile.read()))
        # Convert to flac format
        audiofile = io.BytesIO()
        audio.export(audiofile, format="flac")

        current_time_ms = str(int(time.time() * 1000))
        directory = "./audio/gen/"
        if not os.path.exists(directory):
            os.makedirs(directory)
        flac_file = os.path.join(directory, current_time_ms + ".flac")
        with open(flac_file, "wb") as file:
            file.write(audiofile.read())
        return output(flac_file)

    except Exception as e:
        return jsonify({"error": f"Conversion failed: {str(e)}"}), 500


def output(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    text = response.json()["text"]
    is_danger = get_is_in_danger(text)
    email_sent = False
    if is_danger:
        email_sent = send_email(text)
    obj = {"text": text, "is_danger": is_danger, "email_sent": email_sent}

    return jsonify(obj), 200


def send_email(text):
    recipient = "chanpreet3000@gmail.com"
    subject = "Emergency: Someone Needs Help!"
    body = (
        "Dear Friend,\n\n"
        "We've received a distressing message indicating that someone may be in danger. Here's what was communicated:\n\n"
        f"{text}\n\n"
        "Based on this message, we believe immediate action may be necessary to ensure their safety.\n\n"
        "Please take appropriate steps to reach out and provide assistance if possible.\n\n"
        "Best regards,\n"
        "Hindi-ASR Major Project Team"
    )
    msg = Message(subject, sender=app.config["MAIL_USERNAME"], recipients=[recipient])
    msg.body = body
    try:
        mail.send(msg)
        return True
    except Exception as e:
        print("Send Failure", e)
        return False


if __name__ == "__main__":
    app.run(port=5000, debug=True)
