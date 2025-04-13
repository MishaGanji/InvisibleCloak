from flask import Flask, render_template, Response, jsonify
import cv2
import numpy as np
import time
import webbrowser
from threading import Timer
import os

app = Flask(__name__)

# Define color ranges in HSV
color_ranges = {
    "red": [(np.array([0, 120, 70]), np.array([10, 255, 255])),
            (np.array([170, 120, 70]), np.array([180, 255, 255]))],
    "blue": [(np.array([100, 80, 50]), np.array([130, 255, 255]))],
    "green": [(np.array([40, 40, 40]), np.array([80, 255, 255]))],
    "yellow": [(np.array([20, 100, 100]), np.array([30, 255, 255]))],
}

# Global variables
selected_color = "red"  # Default color
background = None
cap = None

def create_no_camera_image():
    """Create a placeholder image for when camera is not available"""
    if not os.path.exists('static'):
        os.makedirs('static')
    
    no_cam_img = np.zeros((480, 640, 3), dtype=np.uint8)
    no_cam_img[:] = (50, 50, 50)  # Dark gray background
    
    cv2.putText(no_cam_img, "Camera not available", 
              (120, 220), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(no_cam_img, "Please check your webcam connection", 
              (80, 260), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    cv2.imwrite('static/no_camera.jpg', no_cam_img)

def init_camera():
    global cap
    try:
        if cap is not None:
            cap.release()
        
        cap = cv2.VideoCapture(0)  # Try the default camera first
        
        if not cap.isOpened():
            print("Error: Could not open default camera")
            # Try alternative camera index
            cap = cv2.VideoCapture(1)
            if not cap.isOpened():
                return False
            
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        time.sleep(1)  # Allow camera to initialize
        
        return cap.isOpened()
    except Exception as e:
        print(f"Camera initialization error: {str(e)}")
        return False

@app.route('/')
def index():
    return render_template('index.html', colors=list(color_ranges.keys()))

@app.route('/video')
def video():
    return Response(generate_frames(), 
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/set_color/<color>')
def set_color(color):
    global selected_color
    if color in color_ranges:
        selected_color = color
        return jsonify({"status": "success", "color": color})
    return jsonify({"status": "error", "message": "Invalid color"}), 400

@app.route('/capture_background')
def capture_background_route():
    global background, cap
    
    if cap is None or not cap.isOpened():
        if not init_camera():
            return jsonify({"status": "error", "message": "Camera not available"})
    
    # Capture background
    for _ in range(5):  # Skip a few frames to stabilize
        ret, _ = cap.read()
    
    ret, frame = cap.read()
    if ret:
        background = np.flip(frame, axis=1)  # Mirror effect
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "error", "message": "Failed to capture frame"})

@app.route('/check_camera')
def check_camera():
    global cap
    try:
        if cap is None:
            success = init_camera()
        else:
            success = cap.isOpened() and cap.read()[0]
        
        return jsonify({"status": "success" if success else "error", 
                        "camera": "connected" if success else "disconnected"})
    except Exception as e:
        print(f"Error checking camera: {str(e)}")
        return jsonify({"status": "error", "message": str(e)})

def generate_frames():
    global background, cap, selected_color

    # Initialize camera if needed
    if cap is None or not cap.isOpened():
        if not init_camera():
            try:
                with open('static/no_camera.jpg', 'rb') as f:
                    no_cam_data = f.read()
                while True:
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + no_cam_data + b'\r\n')
                    time.sleep(1)
            except Exception as e:
                print(f"Error serving no_camera image: {e}")
                return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = np.flip(frame, axis=1)  # Mirror effect
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask = None
        for lower, upper in color_ranges[selected_color]:
            current_mask = cv2.inRange(hsv, lower, upper)
            mask = current_mask if mask is None else mask + current_mask

        # Improve mask
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        mask = cv2.dilate(mask, np.ones((3, 3), np.uint8), iterations=1)

        inverse_mask = cv2.bitwise_not(mask)

        if background is not None:
            res1 = cv2.bitwise_and(background, background, mask=mask)
            res2 = cv2.bitwise_and(frame, frame, mask=inverse_mask)
            final_output = cv2.addWeighted(res1, 1, res2, 1, 0)
        else:
            final_output = frame

        ret, buffer = cv2.imencode('.jpg', final_output)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    # global background, cap, selected_color
    
    
    # Initialize camera if needed
    if cap is None or not cap.isOpened():
        if not init_camera():
            # Serve no camera image
            try:
                with open('static/no_camera.jpg', 'rb') as f:
                    no_cam_data = f.read()
                while True:
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + no_cam_data + b'\r\n')
                    time.sleep(1)
            except Exception as e:
                print(f"Error serving no_camera image: {e}")
                return
    
    while True:
        # Check camera connection
        if not cap.isOpened():
            if not init_camera():
                break
        
        # Read frame
        ret, frame = cap.read()
        if not ret:
            print("Failed to read frame")
            if not init_camera():  # Try to reinitialize camera
                break
            continue
        
        # Mirror the frame
        frame = np.flip(frame, axis=1)
        
        # If background not captured, show original frame with message
        if background is None:
            cv2.putText(frame, "Please click 'Capture Background'", 
                      (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            _, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
            continue
        
        # Process frame for invisibility effect
        try:
            # Convert frame to HSV
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            # Create mask for selected color
            full_mask = None
            for lower, upper in color_ranges[selected_color]:
                mask = cv2.inRange(hsv, lower, upper)
                if full_mask is None:
                    full_mask = mask
                else:
                    full_mask = cv2.bitwise_or(full_mask, mask)
            
            # Clean the mask
            kernel = np.ones((5, 5), np.uint8)
            full_mask = cv2.morphologyEx(full_mask, cv2.MORPH_OPEN, kernel, iterations=2)
            full_mask = cv2.morphologyEx(full_mask, cv2.MORPH_DILATE, kernel, iterations=1)
            
            # Get inverse of the mask
            inverse_mask = cv2.bitwise_not(full_mask)
            
            # Apply masks to current frame and background
            res1 = cv2.bitwise_and(frame, frame, mask=inverse_mask)
            res2 = cv2.bitwise_and(background, background, mask=full_mask)
            
            # Combine results
            final = cv2.addWeighted(res1, 1, res2, 1, 0)
            
            # Add text overlay
            cv2.putText(final, f"Cloak Color: {selected_color.capitalize()}", 
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
        except Exception as e:
            print(f"Error processing frame: {str(e)}")
            final = frame  # Use original frame if processing fails
        
        # Convert to JPEG and yield
        _, buffer = cv2.imencode('.jpg', final)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == '__main__':
    # Create the no camera image
    create_no_camera_image()
    
    # Open browser after a short delay
    Timer(1, open_browser).start()
    
    # Run the Flask app
    app.run(debug=True, threaded=True, use_reloader=False)