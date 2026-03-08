from ultralytics import YOLO
import cv2
import numpy as np
import sqlite3
from datetime import datetime
import math
import os

model = YOLO("yolov8n.pt")

ANIMAL_CLASSES = ["cow", "sheep", "horse", "elephant"]
DANGER_CLASSES = ["person", "car"]

latitude = 30.3753
longitude = 69.3451

if not os.path.exists("snapshots"):
    os.makedirs("snapshots")

def log_alert(alert_type):
    conn = sqlite3.connect("alerts.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            time TEXT,
            latitude REAL,
            longitude REAL
        )
    """)

    cursor.execute("INSERT INTO alerts (type, time, latitude, longitude) VALUES (?, ?, ?, ?)",
                   (alert_type,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    latitude,
                    longitude))

    conn.commit()
    conn.close()

def calculate_distance(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def detect_herd(frame):
    results = model(frame)
    animal_centers = []
    danger_flag = False
    herd_flag = False

    for r in results:
        boxes = r.boxes
        for box in boxes:
            cls = model.names[int(box.cls)]
            conf = float(box.conf)

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            center = ((x1+x2)//2, (y1+y2)//2)

            if cls in ANIMAL_CLASSES:
                animal_centers.append(center)
                cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)
                cv2.putText(frame, f"{cls} {conf:.2f}", (x1,y1-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

            elif cls in DANGER_CLASSES:
                danger_flag = True
                cv2.rectangle(frame, (x1,y1), (x2,y2), (0,0,255), 2)
                cv2.putText(frame, f"{cls} {conf:.2f}", (x1,y1-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)

    # Herd clustering (distance based)
    for i in range(len(animal_centers)):
        for j in range(i+1, len(animal_centers)):
            if calculate_distance(animal_centers[i], animal_centers[j]) < 150:
                herd_flag = True

    if herd_flag and len(animal_centers) >= 3:
        log_alert("Herd Detected")
        cv2.putText(frame, "HERD DETECTED!", (50,50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)

    if danger_flag:
        log_alert("Danger Detected")
        cv2.putText(frame, "DANGER ALERT!", (50,100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
        cv2.imwrite(f"snapshots/danger_{datetime.now().timestamp()}.jpg", frame)

    return frame