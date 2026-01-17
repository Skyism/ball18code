"""
Basic webcam capture script for mouth detection system.
Uses OpenCV Haar Cascade for face detection and region-based analysis for mouth state.
Displays live video feed from default webcam with keyboard quit functionality.
"""

import cv2
import numpy as np
import serial

# Mouth open threshold - vertical mouth region height in pixels
MOUTH_HEIGHT_THRESHOLD = 25  # Height threshold for detecting open mouth

# Distance calculation constants (calibrated values)
KNOWN_FACE_WIDTH_CM = 12  # Average face width in cm
FOCAL_LENGTH_PX = 673  # Focal length in pixels (calibrated at 12 inches)
CALIBRATION_DISTANCE_INCHES = 12  # Distance used for calibration

# Serial communication constants
SERIAL_PORT = '/dev/ttyUSB0'  # Default serial port (adjust for your system)
BAUD_RATE = 115200  # Standard baud rate for Arduino

def detect_mouth_region(gray_roi, frame_roi):
    """
    Detect mouth state by analyzing the mouth region of interest.
    Uses edge detection and contour analysis to determine if mouth is open.

    Returns: (is_open, mouth_height, mouth_center_x, mouth_center_y, mouth_width)
    """
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray_roi, (7, 7), 0)

    # Apply edge detection
    edges = cv2.Canny(blurred, 30, 100)

    # Find contours in the mouth region
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) == 0:
        # No mouth detected, return closed state with defaults
        h, w = gray_roi.shape
        return False, 0, w // 2, h // 2, w

    # Find the largest contour (likely the mouth)
    largest_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(largest_contour)

    # Calculate mouth center
    mouth_center_x = x + w // 2
    mouth_center_y = y + h // 2

    # Determine if mouth is open based on contour height
    is_open = h > MOUTH_HEIGHT_THRESHOLD

    return is_open, h, mouth_center_x, mouth_center_y, w

def main():
    # Load Haar Cascade classifier for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Verify classifier loaded successfully
    if face_cascade.empty():
        print("Error: Could not load face cascade classifier")
        return

    # Initialize video capture from default webcam (index 0)
    cap = cv2.VideoCapture(0)

    # Check if camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open webcam")
        print("Please check that:")
        print("  1. Your webcam is connected")
        print("  2. No other application is using the webcam")
        print("  3. You have granted camera permissions to Terminal/Python")
        return

    print("Webcam opened successfully")
    print("Press 'q' to quit")

    # Initialize serial connection (optional feature)
    ser = None
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Serial connection established on {SERIAL_PORT}")
    except serial.SerialException as e:
        print(f"Warning: Could not open serial port {SERIAL_PORT}")
        print(f"  Error: {e}")
        print("  Common port names to try:")
        print("    Linux/Mac: /dev/ttyUSB0, /dev/ttyACM0, /dev/ttyUSB1")
        print("    Windows: COM3, COM4, COM5")
        print("  Continuing without serial output...")

    # Main loop - capture and display frames
    while True:
        # Read frame from webcam
        ret, frame = cap.read()

        # Check if frame was read successfully
        if not ret:
            print("Error: Failed to read frame from webcam")
            break

        # Get frame dimensions
        frame_height, frame_width = frame.shape[:2]

        # Convert to grayscale for Haar Cascade detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Process first detected face
        if len(faces) > 0:
            # Get the first face
            (x, y, w, h) = faces[0]

            # Calculate face width in pixels (using bounding box width)
            face_width_px = w

            # Draw rectangle around face
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            # Define mouth region of interest (ROI) - lower third of face
            mouth_roi_y = y + int(h * 0.6)  # Start at 60% down the face
            mouth_roi_h = int(h * 0.35)      # Take 35% of face height
            mouth_roi_x = x + int(w * 0.2)   # Inset from sides
            mouth_roi_w = int(w * 0.6)       # Center 60% of face width

            # Extract mouth ROI from grayscale and color frames
            gray_mouth_roi = gray[mouth_roi_y:mouth_roi_y+mouth_roi_h, mouth_roi_x:mouth_roi_x+mouth_roi_w]
            frame_mouth_roi = frame[mouth_roi_y:mouth_roi_y+mouth_roi_h, mouth_roi_x:mouth_roi_x+mouth_roi_w]

            # Detect mouth state
            is_mouth_open, mouth_h, rel_mx, rel_my, mouth_w = detect_mouth_region(gray_mouth_roi, frame_mouth_roi)

            # Calculate mouth center in full frame coordinates
            mouthX_px = mouth_roi_x + rel_mx
            mouthY_px = mouth_roi_y + rel_my

            # Determine mouth state
            mouth_state = "OPEN" if is_mouth_open else "CLOSED"
            state_color = (0, 0, 255) if is_mouth_open else (0, 255, 0)  # Red for OPEN, Green for CLOSED

            # Draw mouth region rectangle
            cv2.rectangle(frame, (mouth_roi_x, mouth_roi_y),
                         (mouth_roi_x+mouth_roi_w, mouth_roi_y+mouth_roi_h),
                         state_color, 2)

            # Draw circle at mouth center
            cv2.circle(frame, (int(mouthX_px), int(mouthY_px)), 5, state_color, -1)

            # Normalize coordinates to [-1, 1] range with screen center at (0, 0)
            screen_center_x = frame_width / 2
            screen_center_y = frame_height / 2
            mouthX = (mouthX_px - screen_center_x) / screen_center_x
            mouthY = (mouthY_px - screen_center_y) / screen_center_y

            # Send mouth state over serial if connection is active
            if ser is not None:
                try:
                    # Send format: isMouthOpen:OPEN;dx:0.12;dy:-0.34\n
                    message = f'isMouthOpen:{mouth_state};dx:{mouthX:.2f};dy:{mouthY:.2f}\n'
                    ser.write(message.encode('utf-8'))
                except serial.SerialException as e:
                    print(f"Warning: Serial write failed - {e}")
                    print("  Disabling serial output...")
                    ser = None

            # Display mouth state with color-coding
            cv2.putText(frame, f'State: {mouth_state}', (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, state_color, 2)

            # Display face width metric
            cv2.putText(frame, f'Face Width: {face_width_px:.0f} px', (10, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            # Calculate actual distance from camera using pinhole camera model
            # Formula: distance = (known_width × focal_length) / perceived_width
            if face_width_px > 0:  # Avoid division by zero
                distance_inches = (FOCAL_LENGTH_PX * CALIBRATION_DISTANCE_INCHES) / face_width_px

                # Determine distance indicator based on calculated distance
                if distance_inches < 10:
                    distance_indicator = "TOO CLOSE"
                    distance_color = (0, 0, 255)  # Red
                elif distance_inches <= 15:
                    distance_indicator = "OPTIMAL"
                    distance_color = (0, 255, 0)  # Green
                else:
                    distance_indicator = "TOO FAR"
                    distance_color = (0, 165, 255)  # Orange

                # Display calculated distance in inches
                cv2.putText(frame, f'Distance: {distance_inches:.1f} inches ({distance_indicator})',
                           (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, distance_color, 2)
            else:
                cv2.putText(frame, 'Distance: N/A', (10, 90),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            # Display normalized mouth coordinates
            cv2.putText(frame, f'Mouth: X={mouthX:.2f} Y={mouthY:.2f}', (10, 120),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            # Display mouth height for debugging
            cv2.putText(frame, f'Mouth Height: {mouth_h:.0f} px', (10, 150),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        else:
            # No face detected
            cv2.putText(frame, 'No face detected', (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Display the frame in a window
        cv2.imshow('Mouth Detection', frame)

        # Wait for 'q' key press (1ms delay)
        # The & 0xFF mask ensures compatibility across platforms
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Quit signal received")
            break

    # Cleanup: release camera and close all windows
    cap.release()
    cv2.destroyAllWindows()
    if ser is not None:
        ser.close()
    print("Cleanup complete")

if __name__ == "__main__":
    main()
