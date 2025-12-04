"""
DENSE OPTICAL FLOW (FARNEBACK METHOD)

This script computes dense optical flow using the Farneback method on a video file.
It visualizes the motion field as color-coded vectors and either displays it on screen or saves it to a new video file.
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
    print("1: Display dense optical flow on screen")
    print("2: Save output to video file")
    choice = input("Enter 1 or 2: ").strip()
    return 'screen' if choice == '1' else 'file'


def setup_video_writer(output_file_name, frame_size, fps):
    """
    Sets up a video writer with fallback if H264 is unavailable.

    Args:
        output_file_name (str): Output video file path.
        frame_size (tuple): (width, height) of the video frames.
        fps (float): Frame rate of the input video.

    Returns:
        cv2.VideoWriter: Configured writer object for saving video.
    """
    fourcc = cv2.VideoWriter_fourcc(*'avc1')  # Try H264
    out = cv2.VideoWriter(output_file_name, fourcc, fps, frame_size)

    if not out.isOpened():
        print("H264 codec not available, falling back to MP4V.")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_file_name, fourcc, fps, frame_size)

    return out


def compute_dense_optical_flow(cap, prvs, output_mode, out_writer=None):
    """
    Computes dense optical flow using Farneback method and visualizes motion vectors.

    Args:
        cap (cv2.VideoCapture): OpenCV video capture object.
        prvs (numpy.ndarray): First grayscale frame.
        output_mode (str): 'screen' to display the result, or 'file' to save the video.
        out_writer (cv2.VideoWriter, optional): Writer object for saving output video.
    """
    while cap.isOpened():
        # Read next frame from video
        ret, frame2 = cap.read()
        if not ret:
            break

        # Convert frame to grayscale
        next_frame = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

        # Compute dense optical flow using Farneback method
        flow = cv2.calcOpticalFlowFarneback(prvs, next_frame,
                                            None, 0.5, 3, 15, 3, 5, 1.2, 0)

        # Create HSV image to visualize flow
        hsv = np.zeros_like(frame2)
        hsv[..., 1] = 255  # Set saturation

        # Convert flow vectors to polar coordinates
        mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        hsv[..., 0] = ang * 180 / np.pi / 2          # Hue encodes direction
        hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)  # Value encodes magnitude

        flow_color = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)  # Convert HSV to BGR for display/save

        # Show or save the frame depending on user choice
        if output_mode == 'screen':
            cv2.imshow('Dense Optical Flow', flow_color)
            if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
                break
        elif output_mode == 'file' and out_writer:
            out_writer.write(flow_color)

        # Update previous frame
        prvs = next_frame.copy()

    # Release resources
    cap.release()
    if out_writer:
        out_writer.release()
    cv2.destroyAllWindows()


def main():
    """
    Main function to orchestrate dense optical flow processing.
    Handles user interaction and coordinates loading, processing, and output.
    """
    video_input_file_name = "./assets/alligator_short.mp4"
    output_file_name = "dense_optical_flow_output.mp4"

    # Check if input file exists
    if not os.path.exists(video_input_file_name):
        print(f"Video file '{video_input_file_name}' not found.")
        sys.exit()

    # Ask user whether to show on screen or save to file
    output_mode = get_user_output_choice()

    # Open video and get properties
    cap = cv2.VideoCapture(video_input_file_name)
    if not cap.isOpened():
        print("Failed to open video.")
        sys.exit()

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_size = (frame_width, frame_height)

    # Read the first frame
    ret, frame1 = cap.read()
    if not ret:
        print("Error: Could not read the first frame.")
        cap.release()
        sys.exit()

    # Convert first frame to grayscale
    prvs = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

    # Set up output writer if saving to file
    writer = None
    if output_mode == 'file':
        writer = setup_video_writer(output_file_name, frame_size, fps)

    # Run dense optical flow processing
    compute_dense_optical_flow(cap, prvs, output_mode, writer)

    # Report result
    if output_mode == 'file':
        print(f"Dense optical flow video saved as: {output_file_name}")


if __name__ == "__main__":
    main()
