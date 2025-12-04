"""
ARUCO MARKER DETECTION WITH OPENCV

- This script detects ArUco markers.
- It uses OpenCV’s aruco module to identify and draw markers in real time.
"""

import cv2
import cv2.aruco as aruco
import numpy as np
import math

# Initialize webcam (0 is usually the built-in webcam)
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise Exception("Could not open webcam")

# Select ArUco marker dictionary and detector parameters
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters()
detector = aruco.ArucoDetector(aruco_dict, parameters)

# Dummy camera calibration values (these should be replaced with real ones if available)
camera_matrix = np.array([[800, 0, 320],
                          [0, 800, 240],
                          [0, 0, 1]], dtype=float)
dist_coeffs = np.zeros((5, 1))  # Assuming no lens distortion


def capture_frame():
    ret, frame = cap.read()
    if not ret:
        raise Exception("Failed to capture image from webcam")
    return frame


def draw_info(frame, text, pos):
    cv2.putText(frame, text, pos, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)


def analyze_marker(corner, frame, rvec, tvec):
    pts = corner[0]

    # Corners
    corners_int = np.int32(pts)
    
    # Center
    center_x = int(np.mean(pts[:, 0]))
    center_y = int(np.mean(pts[:, 1]))

    # Orientation angle
    dx = pts[1][0] - pts[0][0]
    dy = pts[1][1] - pts[0][1]
    angle = math.degrees(math.atan2(dy, dx))

    # Side lengths (pixel size)
    side_lengths = [np.linalg.norm(pts[i] - pts[(i + 1) % 4]) for i in range(4)]
    pixel_size = np.mean(side_lengths)

    # Perspective distortion: max deviation from mean side length
    distortion = max([abs(length - pixel_size) for length in side_lengths])

    # Occlusion detection: a basic check using distortion threshold
    occluded = distortion > 10  # arbitrary threshold

    # Output to terminal
    print(f"  Corners: {np.int8(pts)}")
    print(f"  Center: ({center_x}, {center_y})")
    print(f"  Orientation: {angle:.1f}°")
    print(f"  Pixel Size (avg side length): {pixel_size:.1f}")
    print(f"  Perspective Distortion (max deviation): {distortion:.1f}°")
    print(f"  Occlusion Detected: {occluded}")
    print(f"  Translation (tvec): {tvec[0][0]}")

    # Output to screen
    draw_info(frame, f"Center: ({center_x}, {center_y})", (center_x - 50, center_y - 60))
    draw_info(frame, f"Angle: {angle:.1f} deg", (center_x - 50, center_y - 45))
    draw_info(frame, f"Size: {pixel_size:.1f}", (center_x - 50, center_y - 30))
    draw_info(frame, f"Distort: {distortion:.1f}", (center_x - 50, center_y - 15))
    draw_info(frame, f"Occluded: {occluded}", (center_x - 50, center_y))
    draw_info(frame, f"tvec: {tvec[0][0]}", (center_x - 50, center_y + 15))


def detect_markers(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, _ = detector.detectMarkers(gray)

    if ids is not None:
        aruco.drawDetectedMarkers(frame, corners, ids)

        # Estimate pose for each marker
        rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(corners, 0.05, camera_matrix, dist_coeffs)

        for i, corner in enumerate(corners):
            cv2.drawFrameAxes(frame, camera_matrix, dist_coeffs, rvecs[i], tvecs[i], 0.03)
            analyze_marker(corner, frame, rvecs[i], tvecs[i])

    return frame, ids


def run_aruco_detection():
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


run_aruco_detection()
