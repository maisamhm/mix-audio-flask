from flask import Flask, request, send_file
import subprocess

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Microservicio Flask para mezclar audio está activo."

@app.route("/mix", methods=["POST"])
def mix_audio():
    voice = request.files["voice"]
    music = request.files["music"]

    voice.save("voice.mp3")
    music.save("music.mp3")

    command = [
        "ffmpeg",
        "-i", "voice.mp3",
        "-i", "music.mp3",
        "-filter_complex", "[1:a]volume=0.3[a1];[0:a][a1]amix=inputs=2:duration=first",
        "-y", "output.mp3"
    ]

    subprocess.run(command, check=True)

    return send_file("output.mp3", mimetype="audio/mpeg")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
