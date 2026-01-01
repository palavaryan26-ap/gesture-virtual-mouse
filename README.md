# Hand Gesture–Controlled Virtual Mouse Using Computer Vision

A real-time **virtual mouse system** that allows users to control their computer cursor using **hand gestures captured via a laptop camera**.  
This project demonstrates practical use of **computer vision, AI, and human–computer interaction (HCI)** without requiring any external hardware.

---

## Features

- Cursor movement using **index finger**
- Left click using **thumb + index finger pinch**
- Right click using **thumb + middle finger pinch**
- Scroll using **finger vertical movement**
- Real-time webcam-based hand tracking
- Smooth and accurate gesture detection
- Safe exit using keyboard (`Q` key)

---

## Tech Stack

- **Python 3.11**
- **OpenCV** – camera input and frame processing
- **MediaPipe Hands** – hand landmark detection
- **PyAutoGUI** – mouse automation
- **NumPy** – calculations and smoothing

---

## How It Works

1. Webcam captures live video frames  
2. MediaPipe detects 21 hand landmarks  
3. Finger positions are tracked in real time  
4. Gestures are recognized using distance and motion logic  
5. Mouse actions are executed using PyAutoGUI  

**Pipeline:**

---

## Installation

### Prerequisites
- Windows OS
- Python **3.11**
- Laptop with a working camera

### Install Required Libraries
```bash
py -3.11 -m pip install opencv-python mediapipe pyautogui

---

If you want, I can now:
- Shorten this for **hackathon submission**
- Rewrite it for **recruiters**
- Add **screenshots / demo GIF**
- Turn this project into a **resume bullet**

Just tell me.

