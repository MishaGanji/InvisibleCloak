<<<<<<< HEAD
# 🧥 Invisibility Cloak using Color Detection and Segmentation

A fun and magical project that makes you invisible — just like Harry Potter!  
Using OpenCV and Python, this project detects a specific colored cloak and replaces it with the background, creating an invisibility illusion.

## ✨ Demo

| Background Captures | Sample Image | Final Frame |
|----------------|---------------------|-------------|
| ![](static/1.png) | ![](static/2.png) | ![](static/3.png) |


## 🚀 Features

- Real-time color detection using OpenCV
- Background capture & segmentation
- Cloak masking and bitwise image manipulation
- Fully written in Python with a simple UI using Flask (optional)

## 🧠 How It Works

1. Capture background for a few seconds.
2. Detect the specific color of the cloak (e.g., red, blue, green).
3. Create a mask for the cloak and remove it from the frame.
4. Replace the cloak area with the static background.
5. Display the final result in real-time.

<!-- ## 📁 Project Structure

├── cloak.py # Main script for the invisibility effect ├── static/ # Static files (CSS, captured images if any) ├── templates/ # HTML templates for UI ├── app.py # Flask app (optional for GUI) └── README.md # This file! -->


## 🛠️ Requirements

- Python 3.x
- OpenCV
- NumPy
- Flask *(optional)*

Install all dependencies:

```bash
pip install opencv-python numpy flask
``` 

## ▶️How to Run

1. Clone the repository

```bash
git clone https://github.com/yourusername/invisible-cloak
cd invisible-cloak
```

2. Run the application

```bash
python app.py
```

3. Visit the app in your browser

http://localhost:5000/

=======
#Invisibe Cloak
🧙‍♂️ Harry Potter's Invisible Cloak
Bring the magic of Hogwarts to life with this Invisible Cloak project! Using Python, Flask, and OpenCV, this web application simulates Harry Potter’s invisible cloak effect with real-time webcam feed and color detection.

🚀 Features
🖥️ Real-time video feed using webcam

🎨 Select your cloak color (Red, Blue, Green, Yellow)

🧤 Make the cloak "disappear" using background subtraction and color segmentation

📸 Capture background for the invisibility effect

✅ Live camera status checks

📱 Mobile-friendly, responsive UI

📂 Project Structure

.
├── app.py                    # Flask backend
├── templates/
│   └── index.html            # Main webpage
├── static/
│   ├── style.css             # Custom styles
│   └── no_camera.jpg         # Shown when camera is not detected
└── README.md                 # This file


📦 Requirements
Python 3.x

Flask

OpenCV (cv2)

NumPy

jQuery (loaded via CDN)

Install the requirements using:


pip install flask opencv-python numpy

▶️ How to Run

Clone the repository


git clone https://github.com/yourusername/invisible-cloak

cd invisible-cloak

Run the application


python app.py

Visit the app in your browser


http://localhost:5000/

🎮 Usage Instructions

Ensure the webcam is connected.

Click “Check Camera” to confirm it’s working.

Make sure the frame is clear (no one in it).

Click “Capture Background” to save the empty scene.

Hold up a solid-colored cloth matching the selected color.

Watch yourself disappear like magic! 🧙

🔧 Troubleshooting

If you see “Camera not available”, make sure your webcam is connected and not in use by another app.

Some cameras might be indexed differently. You can try changing the cv2.VideoCapture() index (e.g., from 0 to 1).

For best results, use a bright solid color cloth and good lighting.
>>>>>>> cb2b689d29957d07842ef2cef79f712184f20ef0

