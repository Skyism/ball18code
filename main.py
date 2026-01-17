"""
Basic webcam capture script for mouth detection system.
Displays live video feed from default webcam with keyboard quit functionality.
"""

import cv2
import mediapipe as mp
import numpy as np
import serial

# Mouth open threshold in pixels
MOUTH_OPEN_THRESHOLD = 20

# Distance calculation constants (calibrated values)
KNOWN_FACE_WIDTH_CM = 12  # Average face width in cm
FOCAL_LENGTH_PX = 673  # Focal length in pixels (calibrated at 12 inches)
CALIBRATION_DISTANCE_INCHES = 12  # Distance used for calibration

# Serial communication constants
SERIAL_PORT = '/dev/ttyUSB0'  # Default serial port (adjust for your system)
BAUD_RATE = 9600  # Standard baud rate for Arduino

def main():
    # Initialize MediaPipe Face Landmarker
    base_options = mp.tasks.BaseOptions(model_asset_path='face_landmarker.task')
    options = mp.tasks.vision.FaceLandmarkerOptions(
        base_options=base_options,
        running_mode=mp.tasks.vision.RunningMode.VIDEO,  # Video stream mode for lower latency
        num_faces=1,  # Single face detection
        min_face_detection_confidence=0.5,
        min_face_presence_confidence=0.5,
        min_tracking_confidence=0.5
    )

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

    # Create Face Landmarker instance
    with mp.tasks.vision.FaceLandmarker.create_from_options(options) as face_landmarker:
        # Main loop - capture and display frames
        frame_timestamp_ms = 0
        while True:
            # Read frame from webcam
            ret, frame = cap.read()

            # Check if frame was read successfully
            if not ret:
                print("Error: Failed to read frame from webcam")
                break

            # Convert frame from BGR to RGB for MediaPipe processing
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Create MediaPipe Image from RGB frame
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

            # Process the frame with Face Landmarker
            face_landmarker_result = face_landmarker.detect_for_video(mp_image, frame_timestamp_ms)
            frame_timestamp_ms += 33  # Approximate 30fps (33ms per frame)

            # Draw landmarks 13 and 14 if face is detected
            if face_landmarker_result.face_landmarks:
                # Get frame dimensions
                frame_height, frame_width = frame.shape[:2]

                # Get the first face's landmarks
                face_landmarks = face_landmarker_result.face_landmarks[0]

                # Extract landmarks 13 and 14 (lip landmarks)
                landmark_13 = face_landmarks[13]
                landmark_14 = face_landmarks[14]

                # Convert normalized coordinates to pixel coordinates
                x_13 = int(landmark_13.x * frame_width)
                y_13 = int(landmark_13.y * frame_height)
                x_14 = int(landmark_14.x * frame_width)
                y_14 = int(landmark_14.y * frame_height)

                # Calculate mouth center coordinates (average of landmarks 13 and 14)
                mouthX_px = (x_13 + x_14) / 2
                mouthY_px = (y_13 + y_14) / 2

                # Normalize coordinates to [-1, 1] range with screen center at (0, 0)
                screen_center_x = frame_width / 2
                screen_center_y = frame_height / 2
                mouthX = (mouthX_px - screen_center_x) / screen_center_x
                mouthY = (mouthY_px - screen_center_y) / screen_center_y

                # Calculate Euclidean distance between landmarks 13 and 14
                distance = np.sqrt((x_14 - x_13)**2 + (y_14 - y_13)**2)

                # Calculate face width using landmarks 234 (left face boundary) and 454 (right face boundary)
                landmark_234 = face_landmarks[234]
                landmark_454 = face_landmarks[454]

                # Convert normalized coordinates to pixel coordinates
                x_234 = int(landmark_234.x * frame_width)
                y_234 = int(landmark_234.y * frame_height)
                x_454 = int(landmark_454.x * frame_width)
                y_454 = int(landmark_454.y * frame_height)

                # Calculate face width in pixels
                face_width_px = np.sqrt((x_454 - x_234)**2 + (y_454 - y_234)**2)

                # Determine mouth state based on threshold
                mouth_state = "OPEN" if distance > MOUTH_OPEN_THRESHOLD else "CLOSED"

                # Send mouth state over serial if connection is active
                if ser is not None:
                    try:
                        # Send '1' for OPEN, '0' for CLOSED, followed by newline
                        state_byte = b'1\n' if mouth_state == "OPEN" else b'0\n'
                        ser.write(state_byte)
                    except serial.SerialException as e:
                        print(f"Warning: Serial write failed - {e}")
                        print("  Disabling serial output...")
                        ser = None

                # Set color based on state: green for CLOSED, red for OPEN
                state_color = (0, 255, 0) if mouth_state == "CLOSED" else (0, 0, 255)

                # Display distance on frame
                cv2.putText(frame, f'Distance: {distance:.0f} px', (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

                # Display mouth state with color-coding
                cv2.putText(frame, f'State: {mouth_state}', (10, 60),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, state_color, 2)

                # Display face width metric
                cv2.putText(frame, f'Face Width: {face_width_px:.0f} px', (10, 90),
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
                               (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, distance_color, 2)
                else:
                    cv2.putText(frame, 'Distance: N/A', (10, 120),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

                # Display normalized mouth coordinates
                cv2.putText(frame, f'Mouth: X={mouthX:.2f} Y={mouthY:.2f}', (10, 150),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

                # Draw circles at landmark positions with state color
                cv2.circle(frame, (x_13, y_13), 5, state_color, -1)
                cv2.circle(frame, (x_14, y_14), 5, state_color, -1)

                # Add labels next to landmarks
                cv2.putText(frame, '13', (x_13 + 10, y_13), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                cv2.putText(frame, '14', (x_14 + 10, y_14), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

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
    print("Cleanup complete")

if __name__ == "__main__":
    main()
