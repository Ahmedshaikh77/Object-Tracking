"""
SPARSE OPTICAL FLOW (LUCAS-KANADE METHOD)

This script demonstrates how to compute sparse optical flow using the Lucas-Kanade method.
It includes the following features:
- Detecting good feature points to track within a defined region of interest (ROI).
- Computing the optical flow for these points between consecutive frames.
- Visualizing the motion vectors on the frames.
- Allowing the user to choose between displaying output on screen or saving to file.
"""

import cv2
import numpy as np
import sys
import os


def get_user_output_choice():
    """
    Prompt the user to choose between displaying the output or saving it to a file.

    Returns:
        str: 'screen' or 'file' depending on user choice.
    """
    print("Choose output mode:")
    print("1: Display optical flow output on screen")
    print("2: Save output to file")
    choice = input("Enter 1 or 2: ").strip()
    return 'screen' if choice == '1' else 'file'


def detect_features(gray_frame):
    """
    Detects good feature points to track within a defined ROI using Shi-Tomasi corner detection.

    Args:
        gray_frame (numpy array): Grayscale image of the video frame.

    Returns:
        numpy array: Array of detected feature points to track.
    """
    # Create a mask with the same size as the frame (all zeros initially)
    mask = np.zeros_like(gray_frame)

    # Define the region of interest (ROI) where we want to detect features
    # (x, y, w, h) defines a rectangular area inside the frame
    x, y, w, h = 200, 150, 400, 100
    mask[y:y + h, x:x + w] = 255  # White ROI where detection is allowed

    # Detect strong corners using Shi-Tomasi method within the ROI
    p0 = cv2.goodFeaturesToTrack(gray_frame, maxCorners=100, qualityLevel=0.3, minDistance=7, mask=mask)
    return p0


def compute_optical_flow(cap, p0, gray_old, output_mode, out_writer=None):
    """
    Computes and visualizes sparse optical flow using Lucas-Kanade method.

    Args:
        cap (cv2.VideoCapture): OpenCV video capture object.
        p0 (numpy array): Initial feature points to track.
        gray_old (numpy array): Grayscale version of the first video frame.
        output_mode (str): 'screen' to display or 'file' to save.
        out_writer (cv2.VideoWriter, optional): Writer object if saving to file.
    """
    # Parameters for Lucas-Kanade optical flow calculation
    lk_params = dict(winSize=(15, 15),  # Size of search window at each pyramid level
                     maxLevel=2,       # Max pyramid levels
                     criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))  # Termination criteria

    while cap.isOpened():
        # Read the next frame from the video
        ret, frame = cap.read()
        if not ret:
            break  # End of video

        # Convert current frame to grayscale
        gray_new = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Calculate optical flow using the Lucas-Kanade method
        p1, st, err = cv2.calcOpticalFlowPyrLK(gray_old, gray_new, p0, None, **lk_params)

        # Draw motion vectors for successfully tracked points
        for new, old in zip(p1[st == 1], p0[st == 1]):
            a, b = new.ravel()
            c, d = old.ravel()
            cv2.line(frame, (int(a), int(b)), (int(c), int(d)), (0, 255, 0), 2)  # Draw motion line
            cv2.circle(frame, (int(a), int(b)), 5, (0, 0, 255), -1)             # Draw current feature point

        # Show or save the resulting frame depending on the selected mode
        if output_mode == 'screen':
            cv2.imshow('Optical Flow', frame)
            if cv2.waitKey(1) & 0xFF == 27:  # Press ESC to exit early
                break
        elif output_mode == 'file' and out_writer:
            out_writer.write(frame)

        # Prepare for next iteration: update old frame and old points
        gray_old = gray_new.copy()
        p0 = p1.reshape(-1, 1, 2)

    # Release resources after processing is done
    cap.release()
    if out_writer:
        out_writer.release()
    cv2.destroyAllWindows()


def setup_video_writer(output_file_name, frame_size, fps):
    """
    Sets up a video writer with fallback if H264 is unavailable.

    Args:
        output_file_name (str): Output video file path.
        frame_size (tuple): (width, height) of video.
        fps (float): Frame rate of the video.

    Returns:
        cv2.VideoWriter: Configured writer object for saving video.
    """
    # Try using H264 codec first
    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    out = cv2.VideoWriter(output_file_name, fourcc, fps, frame_size)

    # If H264 is not available, fall back to MP4V
    if not out.isOpened():
        print("H264 codec not available, falling back to MP4V.")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_file_name, fourcc, fps, frame_size)
    
    return out


def main():
    """
    Main function to run the sparse optical flow workflow.
    Handles user interaction and coordinates all processing steps.
    """
    video_input_file_name = "./assets/alligator_short.mp4"
    output_file_name = "optical_flow_output.mp4"

    # Check that the video file exists before proceeding
    if not os.path.exists(video_input_file_name):
        print(f"Video file '{video_input_file_name}' not found.")
        sys.exit()

    # Prompt the user for output mode (screen or file)
    output_mode = get_user_output_choice()

    # Open video file for reading
    cap = cv2.VideoCapture(video_input_file_name)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_size = (frame_width, frame_height)

    # Read the first frame to initialize tracking
    ret, old_frame = cap.read()
    if not ret:
        print("Error: Could not read video file.")
        cap.release()
        sys.exit()

    # Convert first frame to grayscale for feature detection
    gray_old = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)

    # Detect feature points in a predefined ROI
    p0 = detect_features(gray_old)
    if p0 is None:
        print("No feature points detected. Exiting.")
        cap.release()
        sys.exit()

    # Set up writer if user chose to save the output
    writer = None
    if output_mode == 'file':
        writer = setup_video_writer(output_file_name, frame_size, fps)

    # Run optical flow computation and display/save results
    compute_optical_flow(cap, p0, gray_old, output_mode, writer)

    # Notify user if saving was successful
    if output_mode == 'file':
        print(f"Optical flow video saved as: {output_file_name}")


if __name__ == "__main__":
    main()
