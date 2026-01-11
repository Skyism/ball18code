"""
Basic webcam capture script for mouth detection system.
Displays live video feed from default webcam with keyboard quit functionality.
"""

import cv2

def main():
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

    # Main loop - capture and display frames
    while True:
        # Read frame from webcam
        ret, frame = cap.read()

        # Check if frame was read successfully
        if not ret:
            print("Error: Failed to read frame from webcam")
            break

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
