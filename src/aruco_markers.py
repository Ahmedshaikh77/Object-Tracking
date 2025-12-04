"""
ARUCO MARKER DETECTION WITH OPENCV

- This script detects ArUco markers.
- It uses OpenCV’s aruco module to identify and draw markers in real time.
"""

import cv2
import cv2.aruco as aruco

"""
SETUP:
Initialize the laptop camera and configure ArUco detection parameters.
"""

# Initialize webcam (0 is usually the built-in webcam)
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise Exception("Could not open webcam")

# Select ArUco marker dictionary and detector parameters
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters()
detector = aruco.ArucoDetector(aruco_dict, parameters)


def capture_frame():
    """
    Captures a frame from the webcam.
    Returns:
        frame (numpy array): BGR image frame.
    """
    ret, frame = cap.read()
    if not ret:
        raise Exception("Failed to capture image from webcam")
    return frame


def detect_markers(frame):
    """
    Detects ArUco markers in the frame and draws marker boxes and IDs.
    Args:
        frame (numpy array): BGR image frame from the camera.
    Returns:
        annotated_frame (numpy array): Frame with detected markers drawn.
        ids (list): List of detected marker IDs.
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, _ = detector.detectMarkers(gray)
    
    if ids is not None:
        aruco.drawDetectedMarkers(frame, corners, ids)
    
    return frame, ids


def run_aruco_detection():
    """
    Continuously captures frames and detects ArUco markers.
    Shows result in a window and saves the most recent frame to disk.
    """
    print("ArUco Marker Detection Running... Press 'q' to exit.")
    while True:
        frame = capture_frame()
        annotated_frame, ids = detect_markers(frame)

        if ids is not None:
            print(f"Detected Marker IDs: {ids.flatten()}")

        # Show the frame in a window
        cv2.imshow("ArUco Marker Detection", annotated_frame)

        # Save the frame to file
        cv2.imwrite("frame.jpg", annotated_frame)

        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Cleanup
    cap.release()
    cv2.destroyAllWindows()


def test_functions():
    """
    Tests the ArUco detection pipeline by capturing a single frame and saving annotated output.
    """
    try:
        print("Capturing frame...")
        frame = capture_frame()

        print("Detecting markers...")
        annotated, ids = detect_markers(frame)

        print(f"Detected Marker IDs: {ids.flatten() if ids is not None else 'None'}")

        print("Saving frame as 'frame.jpg'...")
        cv2.imwrite("frame.jpg", annotated)

        # Show the frame
        cv2.imshow("Test Frame", annotated)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        print("Test successful!")

    except Exception as e:
        print(f"An error occurred: {e}")
        cap.release()
        cv2.destroyAllWindows()

# Uncomment the line below to test functions manually
# test_functions()

# Uncomment the line below to run detection continuously
run_aruco_detection()
