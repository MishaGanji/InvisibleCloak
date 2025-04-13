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

├── app.py                    # Flask backend
├── templates/
│   └── index.html            # Main webpage
├── static/
│   ├── style.css             # Custom styles
│   └── no_camera.jpg         # Shown when camera is not detected
└── README.md           

📦 Requirements

Python 3.x
Flask
OpenCV (cv2)
NumPy
jQuery (loaded via CDN)

Install the requirements using: pip install flask opencv-python numpy

▶️ How to Run

1. Clone the repository
git clone https://github.com/yourusername/invisible-cloak
cd invisible-cloak

2. Run the application
python app.py

3. Visit the app in your browser
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

