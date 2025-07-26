from flask import Flask, request, send_file, Response
import subprocess

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return '''
    <html>
        <head>
            <title>Mix Audio</title>
        </head>
        <body style="font-family:sans-serif;">
            <h2>🎙️ Sube tu voz y música</h2>
            <form method="POST" action="/mix" enctype="multipart/form-data">
                <p><b>Voz (MP3):</b> <input type="file" name="voice"></p>
                <p><b>Música de fondo (MP3):</b> <input type="file" name="music"></p>
                <input type="submit" value="🎧 Mezclar">
            </form>
        </body>
    </html>
    '''

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
    subprocess.run(command)

    return send_file(
        "output.mp3",
        as_attachment=True,
        download_name="mezcla.mp3",
        mimetype="audio/mpeg"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
