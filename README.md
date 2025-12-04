# Tracking within Images

## ArUco Markers

ArUco markers are binary square fiducial markers that can be easily detected by computer vision systems. Each marker contains a unique ID and is designed to be robust to lighting changes, distortion, and partial occlusion. ArUco markers are widely used in robotics, augmented reality, and camera calibration due to their fast detection and high reliability.

In this project, predefined ArUco marker PDFs are provided for printing and use. The script uses a webcam feed to detect these markers in real time and draw bounding boxes and IDs around them.

#### Files for Use in Assets Folder
- aruco_markers_0.pdf
- aruco_markers_1.pdf

#### Run Script
```bash
python src/aruco_markers.py
```

To change camera, change the python script number:
cap = cv2.VideoCapture(0)

Press 'q' to close the pop-up window


## Object Tracking

Object tracking is the process of locating a specific object in a sequence of video frames and following its movement over time. It is a key technique in computer vision, used in applications like video surveillance, robotics, augmented reality, and activity recognition.

This project allows users to interactively select an object to track from the first frame of a video. Several tracking algorithms from OpenCV are supported, each offering a trade-off between speed and accuracy:
- **BOOSTING**
- **CSRT**
- **KCF**
- **MIL**
- **MOSSE**
- **MEDIANFLOW**
- **TLD**

After selecting an object, the tracker continuously updates the object's position as it moves through the video. Users are prompted in the terminal to choose both the tracking algorithm and whether to view the tracking live or save the output to an `.mp4` file.

#### Files for Use in Assets Folder
- plane_short.mp4


#### Run Script
```bash
python src/object_tracking.py
```

After running, a pop-up window will appear. Use your mouse to select the object to track.


## Optical Flow

Optical flow is a computer vision technique used to estimate the motion of objects between consecutive frames in a video. It works by analyzing how pixel intensities shift over time, enabling applications like motion tracking, object segmentation, video compression, and scene understanding.

There are two main approaches demonstrated in this project:
- **Lucas-Kanade (Sparse) Optical Flow**: Tracks a limited number of strong feature points across frames. It's efficient and useful for following specific moving objects or corners within a scene.
- **Farneback (Dense) Optical Flow**: Calculates motion vectors for every pixel in the frame, producing a full motion field. This method is useful for visualizing global motion and flow patterns across the entire image.

Both implementations prompt the user to choose whether to display the result on screen or save the output to an `.mp4` video file.

#### Files for Use in Assets Folder
- alligator_short.mp4

### Lucas-Kanade (Sparse) Optical Flow

This script tracks sparse points using the Lucas-Kanade method.


#### Run Script
```bash
python src/optical_flow_lk.py
```

### Farneback (Dense) Optical Flow

This script visualizes dense optical flow across the entire frame using the Farneback method.

#### Run Script
```bash
python src/optical_flow_f.py
```