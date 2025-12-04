"""
ARUCO MARKER DETECTION WITH OPENCV

- This script detects ArUco markers.
- It uses OpenCV’s aruco module to identify and draw markers in real time.
"""

import cv2
import cv2.aruco as aruco
import numpy as np
import time

def initialize_camera():
    """Initializes the webcam and checks for availability."""
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise Exception("Could not open webcam")
    return cap

def setup_aruco_detector():
    """Sets up the ArUco marker detector and dictionary."""
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
    parameters = aruco.DetectorParameters()
    detector = aruco.ArucoDetector(aruco_dict, parameters)
    return detector

def get_camera_calibration():
    """Provides dummy camera calibration parameters."""
    camera_matrix = np.array([[800, 0, 320],
                              [0, 800, 240],
                              [0, 0, 1]], dtype=float)
    dist_coeffs = np.zeros((5, 1))  # Assuming no distortion
    return camera_matrix, dist_coeffs

def draw_pyramid(frame, rvec, tvec, camera_matrix, dist_coeffs):
    """Draws a regular pyramid hovering above the detected marker.

    The pyramid base is offset above the marker plane by `hover` meters so
    the object appears to float. Units are meters and should match the
    `markerLength` used in pose estimation.
    """
    size = 0.03  # Base size in meters
    h = size * 1.5  # Height of the pyramid
    hover_max = 0.08  # maximum vertical offset above the marker plane (meters)

    # Oscillate hover between 0 and hover_max using a sine wave so the
    # pyramid bobs up and down. `freq` is cycles per second.
    freq = 0.5  # Hz (one full up-and-down every 2 seconds)
    t = time.time()
    # sine varies -1..1, map to 0..1 then scale by hover_max
    hover_current = (0.5 * (1.0 + np.sin(2.0 * np.pi * freq * t))) * hover_max

    # Define 3D points for pyramid base and tip. We add `hover_current` to Z
    # so the whole pyramid is lifted above the marker plane (which is at Z=0).
    base = np.float32([[-size, -size, hover_current],
                       [ size, -size, hover_current],
                       [ size,  size, hover_current],
                       [-size,  size, hover_current]])
    tip = np.float32([[0, 0, hover_current + h]])
    pts3d = np.vstack((base, tip))

    # --- Spin the pyramid around the marker's local Z axis ---
    # Compute a time-based rotation angle (radians). Adjust `deg_per_sec`
    # to change spin speed. The rotation is applied in the marker coordinate
    # system (so origin is marker center).
    deg_per_sec = 45.0  # degrees per second
    angle_rad = (time.time() * deg_per_sec % 360) * (np.pi / 180.0)
    c = np.cos(angle_rad)
    s = np.sin(angle_rad)
    R2 = np.array([[c, -s], [s, c]], dtype=np.float32)

    # Rotate only the X,Y columns; Z remains unchanged
    pts3d_rot = pts3d.copy()
    pts3d_rot[:, :2] = pts3d[:, :2].dot(R2.T)

    # Project 3D points to image plane
    pts2d, _ = cv2.projectPoints(pts3d_rot, rvec, tvec, camera_matrix, dist_coeffs)
    pts2d = np.int32(pts2d).reshape(-1, 2)

    # Draw pyramid edges
    for i in range(4):
        cv2.line(frame, pts2d[i], pts2d[(i+1)%4], (0, 255, 255), 2)
        cv2.line(frame, pts2d[i], pts2d[4], (0, 255, 255), 2)

def draw_cube(frame, rvec, tvec, camera_matrix, dist_coeffs):
    """Draws a cube on the detected marker."""
    size = 0.1  # Cube size larger than marker
    half = size / 2.0

    # Define 3D points of the cube
    pts3d = np.float32([
        [-half, -half, 0], [half, -half, 0], [half, half, 0], [-half, half, 0],
        [-half, -half, size], [half, -half, size], [half, half, size], [-half, half, size]
    ])

    # Project 3D points to image plane
    pts2d, _ = cv2.projectPoints(pts3d, rvec, tvec, camera_matrix, dist_coeffs)
    pts2d = np.int32(pts2d).reshape(-1, 2)

    # Draw cube edges
    for i in range(4):
        cv2.line(frame, pts2d[i], pts2d[(i+1)%4], (255, 0, 255), 2)       # Bottom face
        cv2.line(frame, pts2d[i+4], pts2d[((i+1)%4)+4], (255, 0, 255), 2) # Top face
        cv2.line(frame, pts2d[i], pts2d[i+4], (255, 0, 255), 2)           # Vertical edges

def detect_and_draw_markers(frame, detector, camera_matrix, dist_coeffs):
    """Detects ArUco markers and draws corresponding 3D objects."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, _ = detector.detectMarkers(gray)

    if ids is not None:
        rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(corners, 0.05, camera_matrix, dist_coeffs)
        for i, marker_id in enumerate(ids.flatten()):
            rvec = rvecs[i]
            tvec = tvecs[i]
            cv2.drawFrameAxes(frame, camera_matrix, dist_coeffs, rvec, tvec, 0.03)

            if marker_id == 8:
                draw_pyramid(frame, rvec, tvec, camera_matrix, dist_coeffs)
            elif marker_id == 9:
                draw_cube(frame, rvec, tvec, camera_matrix, dist_coeffs)

def main():
    """Main loop to run ArUco marker detection and object rendering."""
    print("Press 'q' to quit")
    cap = initialize_camera()
    detector = setup_aruco_detector()
    camera_matrix, dist_coeffs = get_camera_calibration()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        detect_and_draw_markers(frame, detector, camera_matrix, dist_coeffs)
        cv2.imshow("3D Object on ArUco Marker", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()