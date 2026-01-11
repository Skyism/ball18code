"""
Basic webcam capture script for mouth detection system.
Displays live video feed from default webcam with keyboard quit functionality.
"""

import cv2
import mediapipe as mp
import numpy as np

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
