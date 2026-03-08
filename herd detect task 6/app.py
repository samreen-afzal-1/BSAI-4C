from flask import Flask, render_template, request, redirect, url_for, Response, jsonify
import cv2
import os
import sqlite3
from herd import detect_herd

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload_video():
    file = request.files['video']

    if file.filename == '':
        return redirect(url_for('index'))

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    return redirect(url_for('process_video', filename=file.filename))

@app.route('/process/<filename>')
def process_video(filename):
    return Response(generate_frames(filename),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def generate_frames(filename):
    video_path = os.path.join(UPLOAD_FOLDER, filename)
    cap = cv2.VideoCapture(video_path)

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        frame = detect_herd(frame)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

@app.route('/alerts')
def get_alerts():
    conn = sqlite3.connect("alerts.db")
    cursor = conn.cursor()
    cursor.execute("SELECT type, latitude, longitude FROM alerts ORDER BY id DESC LIMIT 1")
    data = cursor.fetchone()
    conn.close()

    if data:
        return jsonify({
            "type": data[0],
            "lat": data[1],
            "lon": data[2]
        })
    return jsonify({})

if __name__ == "__main__":
    app.run(debug=True)