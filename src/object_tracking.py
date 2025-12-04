"""
OBJECT TRACKING WITH OPENCV

- This script tracks a specified object in a video using OpenCV's object tracking algorithms.
- It initializes a tracker, processes video frames, and either displays the output or saves it to a video file.
"""

import cv2
import sys
import os

def get_user_choices():
    """
    Prompt user to select an object tracking algorithm and output mode.

    Returns:
        tuple:
            - tracker_type (str): The selected tracker type.
            - output_mode (str): 'screen' or 'file' depending on user selection.
    """
    tracker_types = ['BOOSTING', 'CSRT', 'KCF', 'MEDIANFLOW', 'MIL', 'MOSSE', 'TLD']

    print("Select an object tracking algorithm:")
    for i, name in enumerate(tracker_types):
        print(f"{i}: {name}")
    
    try:
        tracker_choice = int(input("Enter the number corresponding to the tracker you want to use: "))
        tracker_type = tracker_types[tracker_choice]
    except (IndexError, ValueError):
        print("Invalid input. Defaulting to CSRT.")
        tracker_type = 'CSRT'

    print("\nSelect output mode:")
    print("1: Display output on screen")
    print("2: Save output to file")
    
    output_choice = input("Enter your choice (1 or 2): ").strip()
    output_mode = 'screen' if output_choice == '1' else 'file'

    return tracker_type, output_mode

def initialize_tracker(tracker_type):
    """
    Initializes the selected OpenCV object tracker.

    Args:
        tracker_type (str): Name of the tracker algorithm.

    Returns:
        tracker: OpenCV object tracker instance.
    """
    if tracker_type == 'BOOSTING':
        return cv2.legacy.TrackerBoosting_create()
    elif tracker_type == 'CSRT':
        return cv2.legacy.TrackerCSRT_create()
    elif tracker_type == 'KCF':
        return cv2.legacy.TrackerKCF_create()
    elif tracker_type == 'MEDIANFLOW':
        return cv2.legacy.TrackerMedianFlow_create()
    elif tracker_type == 'MIL':
        return cv2.legacy.TrackerMIL_create()
    elif tracker_type == 'MOSSE':
        return cv2.legacy.TrackerMOSSE_create()
    elif tracker_type == 'TLD':
        return cv2.legacy.TrackerTLD_create()
    else:
        raise ValueError(f"Unsupported tracker type: {tracker_type}")

def setup_video_writer(filename, width, height, fps):
    """
    Sets up a video writer using H264 codec, falling back to MP4V if needed.

    Args:
        filename (str): Path to the output video file.
        width (int): Width of the video frames.
        height (int): Height of the video frames.
        fps (float): Frame rate of the video.

    Returns:
        cv2.VideoWriter: Initialized video writer object.
    """
    fourcc = cv2.VideoWriter_fourcc(*'avc1')  # H264
    writer = cv2.VideoWriter(filename, fourcc, fps, (width, height))
    if not writer.isOpened():
        print("H264 codec not available, falling back to MP4V codec.")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter(filename, fourcc, fps, (width, height))
    return writer

def select_roi(frame):
    """
    Opens a window to let the user manually select the object to track.

    Args:
        frame (ndarray): First frame of the video for selecting ROI.

    Returns:
        tuple: Bounding box coordinates (x, y, w, h).
    """
    print("Draw the object to track, then press ENTER or SPACE.")
    bbox = cv2.selectROI("Select Object", frame, fromCenter=False, showCrosshair=True)
    cv2.destroyWindow("Select Object")
    return bbox

def track_object(video_cap, tracker, bbox, output_mode, video_writer=None):
    """
    Performs the object tracking loop.

    Args:
        video_cap (cv2.VideoCapture): Video capture object.
        tracker: Initialized object tracker.
        bbox (tuple): Initial bounding box (x, y, w, h).
        output_mode (str): 'screen' to display or 'file' to save.
        video_writer (cv2.VideoWriter, optional): Writer object if saving to file.
    """
    while True:
        ok, frame = video_cap.read()
        if not ok:
            break

        success, bbox = tracker.update(frame)
        if success:
            x, y, w, h = [int(v) for v in bbox]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        else:
            cv2.putText(frame, "Tracking failure detected", (80, 140),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

        if output_mode == 'screen':
            cv2.imshow("Tracking", frame)
            if cv2.waitKey(1) & 0xFF == 27:  # ESC
                break
        elif output_mode == 'file' and video_writer is not None:
            video_writer.write(frame)

    video_cap.release()
    if video_writer:
        video_writer.release()
    cv2.destroyAllWindows()

def main():
    """
    Main function to orchestrate the tracking workflow.
    """
    video_input_file_name = "./assets/plane_short.mp4"

    if not os.path.exists(video_input_file_name):
        print(f"Video file '{video_input_file_name}' not found.")
        sys.exit()

    tracker_type, output_mode = get_user_choices()

    # Create output filename if needed
    base_name, _ = os.path.splitext(video_input_file_name)
    video_output_file_name = f"{base_name}_{tracker_type}_tracked.mp4"

    video_cap = cv2.VideoCapture(video_input_file_name)
    if not video_cap.isOpened():
        print("Error opening video file")
        sys.exit()

    ok, frame = video_cap.read()
    if not ok:
        print("Failed to read video")
        sys.exit()

    bbox = select_roi(frame)
    tracker = initialize_tracker(tracker_type)
    tracker.init(frame, bbox)

    frame_width = int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = video_cap.get(cv2.CAP_PROP_FPS)

    video_writer = None
    if output_mode == 'file':
        video_writer = setup_video_writer(video_output_file_name, frame_width, frame_height, fps)

    track_object(video_cap, tracker, bbox, output_mode, video_writer)

    if output_mode == 'file':
        print(f"Tracking complete. Video saved as: {video_output_file_name}")

if __name__ == "__main__":
    main()
