# Script guide

[Back to README](../README.md) · [Contributing](../CONTRIBUTING.md)

Complete the [environment setup](../README.md#1-prepare-a-desktop-python-environment) first. All commands here assume the repository root is the working directory. None of the scripts parses command-line arguments, and none downloads model weights or data. Camera index `0`, input paths, calibration constants, and output names are fixed in the source.

## Object tracking

Source: [src/object_tracking.py](../src/object_tracking.py)

```bash
python src/object_tracking.py
```

Input: `assets/plane_short.mp4`. This is a manually initialized single-object tracker, not an object detector.

1. Choose a tracker in the terminal: `0` BOOSTING, `1` CSRT, `2` KCF, `3` MEDIANFLOW, `4` MIL, `5` MOSSE, or `6` TLD. All constructors are called through `cv2.legacy`. The script defaults to CSRT for nonnumeric or out-of-range input; use the displayed nonnegative choices rather than Python's accepted negative indices.
2. Choose `1` for screen output or `2` for file output. Any response other than exactly `1` selects file output, including a blank or mistyped response.
3. Drag a nonempty box in **Select Object**, then press **Enter** or **Space**. There is no explicit guard for a cancelled/zero-size selection or failed tracker initialization; restart with a valid box if initialization fails.
4. Screen output shows the tracker result in **Tracking**. Press **Esc** with the window focused, or wait for the end of the clip.

File output is `assets/plane_short_<TRACKER>_tracked.mp4`, for example `assets/plane_short_CSRT_tracked.mp4`. It still opens the initial selection window, then writes subsequent frames without a playback window or keyboard exit check. The first frame initializes the tracker and is not written as an output frame. A failed update draws a message; it does not trigger detection or reinitialization.

To use a different video, change `video_input_file_name` in `main()` in a separate code change. The output name is derived from that input path, so its parent directory must be writable. There is no webcam-switching prompt or `--video` argument.

## Dense optical flow

Source: [src/optical_flow_f.py](../src/optical_flow_f.py)

```bash
python src/optical_flow_f.py
```

Input: `assets/alligator_short.mp4`. Choose `1` to display **Dense Optical Flow** or `2` to save `dense_optical_flow_output.mp4` in the working directory. Every response other than `1` chooses file output. **Esc** exits screen mode; file mode runs to the end of the clip without an Esc check.

The implementation calculates Farneback flow between consecutive grayscale frames. Hue represents direction and brightness is the flow magnitude normalized separately for each frame. The colors are not absolute speed measurements or a consistent cross-frame magnitude scale, and motion can come from the camera as well as the subject. The first frame initializes the calculation; subsequent frames form the output.

Change `video_input_file_name` and `output_file_name` in `main()` only when intentionally customizing the code. No interactive region selection is required.

## Sparse optical flow from a video

Source: [src/optical_flow_lk.py](../src/optical_flow_lk.py)

```bash
python src/optical_flow_lk.py
```

Input: `assets/alligator_short.mp4`. Choose `1` to display **Optical Flow** or `2` to save `optical_flow_output.mp4` in the working directory. Every response other than `1` chooses file output. **Esc** exits screen mode only.

`detect_features()` uses Shi-Tomasi corners inside the fixed first-frame rectangle `(x, y, width, height) = (200, 150, 400, 100)`. There is no mouse-selection window. It requests at most 100 corners, with quality level `0.3` and minimum distance `7`. Lucas-Kanade updates are shown as red points with green displacement lines.

The rectangle is only a mask for initial feature selection, not a constraint keeping later tracks inside that region. A different video may need a different rectangle. If no initial features are found, the script prints a message and exits. During tracking, it uses the status mask for drawing but passes all returned points into the next iteration; it does not guard against `None` flow results or replenish lost points. These are implementation limitations, not installation problems. No tracking accuracy is established by the overlay.

## Sparse optical flow from drawn webcam regions

Source: [src/optical_flow_lk_blob.py](../src/optical_flow_lk_blob.py)

```bash
python src/optical_flow_lk_blob.py
```

Input: webcam index `0`. This script does not read `alligator_short.mp4`, despite sharing an optical-flow method with the video example. It displays results only; there is no output-mode prompt or video writer.

1. In **Draw Blobs - ESC=Done, Enter=Finish Blob**, hold the left mouse button and drag to outline a region on the captured first frame. Release the mouse button.
2. Press **Enter** to add that region. At least three sampled points are needed. Releasing the mouse alone does not commit a region. Repeat to add more regions.
3. Press **Esc** to finish selection. Any current region not committed with Enter is excluded.
4. If features are found, **Detected Features** previews blue points. Press **any key** in that window to start tracking; keep the camera and scene reasonably still during selection to avoid a large first-frame jump.
5. Press **Esc** in **Webcam Optical Flow** to quit.

Corners are selected within the filled user regions with a maximum of 500, quality level `0.01`, and minimum distance `3`. These regions are feature masks, not semantic object segmentations. Successfully tracked points are retained, but the script does not reseed features or stop cleanly when all tracks disappear; an empty point set can cause a later OpenCV error. Restart and select a textured region if needed. Changing camera index requires editing `VideoCapture(0)` in `main()`.

## Basic ArUco detection

Source: [src/aruco_markers.py](../src/aruco_markers.py)

```bash
python src/aruco_markers.py
```

Input: webcam index `0`; dictionary: `DICT_4X4_50`. Present a matching marker to the camera. The script draws marker outlines and IDs in **ArUco Marker Detection**, prints detected IDs, and saves the latest annotated frame as `frame.jpg` in the working directory **on every loop iteration**, even when no marker is detected. Press **q** in the window to stop.

The two supplied PDFs can be opened or printed independently; they are not input files consumed by the script. Check the marker dictionary and IDs rather than assuming them from a filename. Basic detection does not require camera calibration and does not estimate pose.

The script opens the camera and starts its loop at module import time. Do not import it as a harmless API check or unit test. Its `test_functions()` helper is a manual camera/window check, not an automated test suite; merely uncommenting it does not disable the continuous run call below it.

## Advanced ArUco diagnostics

Source: [src/aruco_markers_advanced.py](../src/aruco_markers_advanced.py)

```bash
python src/aruco_markers_advanced.py
```

Input: webcam index `0`; dictionary: `DICT_4X4_50`. It draws marker outlines, axes, and numeric annotations, prints diagnostics, and repeatedly overwrites the same `frame.jpg` used by the basic example. Press **q** to quit. This module also opens the camera and enters its loop at import time.

Treat this as an uncalibrated visualization until its placeholders are replaced in a separately validated code change:

- Intrinsics are hard-coded as `[[800, 0, 320], [0, 800, 240], [0, 0, 1]]`, with zero distortion. The script neither loads calibration nor sets a matching camera capture resolution.
- Pose estimation assumes a marker side length of `0.05` meters. Printed size and camera calibration must agree with these values for meaningful pose geometry.
- Orientation is the image-plane angle of one marker edge, not a full 3D attitude measurement.
- The value labeled perspective distortion is a deviation of pixel side lengths, although the terminal text appends a degree symbol. The `> 10` occlusion test is an arbitrary heuristic, not validated occlusion detection.
- Printed corners are cast to `np.int8`, which cannot represent ordinary image-coordinate ranges without wrapping. The displayed `tvec` accesses only its first component, not the full translation or camera distance.

No real calibration data or calibration utility is included. The source uses `aruco.estimatePoseSingleMarkers`, which exists in the documented 4.11 API but is deprecated in favor of `solvePnP`; this documentation does not migrate the implementation. See the [OpenCV 4.11 ArUco API](https://docs.opencv.org/4.11.0/d9/d6a/group__aruco.html).

## ArUco augmented-reality overlays

Source: [src/aruco_markers_AR.py](../src/aruco_markers_AR.py)

```bash
python src/aruco_markers_AR.py
```

Input: webcam index `0`; dictionary: `DICT_4X4_50`. In **3D Object on ArUco Marker**, ID **8** gets a hovering, rotating wireframe pyramid, and ID **9** gets a wireframe cube. Other detected IDs receive axes, not these objects. Press **q** to quit. There is no screenshot or video-saving path in this script.

The geometry is generated from NumPy arrays in the code; no external 3D model is missing or required. The pyramid animation is time-based rather than a measured motion. `get_camera_calibration()` returns the same dummy intrinsics and zero distortion as the advanced example, and pose estimation assumes a `0.05`-meter marker. These overlays are illustrative, not calibrated AR. Before expecting particular overlays from the supplied printouts, use the basic detector to confirm whether IDs 8 or 9 are present. The code has no marker-generation or calibration command.

## Troubleshooting

### Verification scope

A setup smoke check on macOS arm64 with Python 3.12.13, NumPy 2.2.4, and `opencv-contrib-python` 4.11.0.86 confirmed imports, construction of all seven source-referenced legacy trackers, availability of the three ArUco APIs used here, and first-frame decoding of both bundled clips. This check did not run the interactive scripts, access a webcam, validate video output, or measure tracking quality. Other operating systems and Python versions were not exercised.

### Missing modules, `cv2.legacy`, or ArUco methods

Run the README import checks using the same activated environment as the script. `python -m pip list` and `python -m pip show opencv-contrib-python opencv-python opencv-contrib-python-headless opencv-python-headless` reveal which distributions are installed; missing-package warnings for the three unselected variants are expected. Multiple OpenCV wheels sharing `cv2` are a known conflict. Start a fresh environment with only the documented contrib pin rather than repeatedly installing different wheels on top of one another.

The code expects `cv2.aruco.DetectorParameters()`, `ArucoDetector`, `estimatePoseSingleMarkers`, and the seven `cv2.legacy.Tracker*_create()` methods used in `initialize_tracker()`. An older/newer or main-only OpenCV build may expose different APIs. Do not silently substitute a different algorithm or claim an API migration is covered by these instructions. No dependencies have been changed here.

### Input video not found or cannot be opened

Run from the root, not from `src/`: `python src/optical_flow_f.py` is the intended form. Confirm the matching file exists under `assets/`. If the file exists but opening/first-frame reading fails, check that the clip is intact and your OpenCV build can decode it. Passing an extra path on the command line has no effect because there is no argument parser.

### No camera or no usable frame

The webcam scripts all use index `0`, which is not guaranteed to be the camera you want. Check operating-system camera permission for the terminal/interpreter, close other camera applications, and verify the device locally. A different index is an explicit source customization, not a supplied command-line option. Avoid running the camera examples in a remote/headless session.

### No window, unresponsive keys, or GUI backend errors

Use a desktop OpenCV wheel and a graphical session. Focus the OpenCV window for **q**, **Esc**, Enter, or Space; terminal focus alone will not deliver those events. File mode in object tracking is not headless: rectangle selection still opens a window. Even the file-only flow paths finish with `destroyAllWindows()`, so a headless-wheel workflow is not established by these scripts.

### No features, drifting tracks, or optical-flow errors

For video sparse flow, inspect the fixed first-frame feature rectangle. For blob flow, commit a drawn region with Enter before finishing and choose a textured region. Neither sparse-flow implementation replenishes features after initialization; the video implementation also lacks guards for invalid flow results. Restarting can recover an experiment, but robust lost-feature handling requires a code change. A moving camera, occlusion, blur, or weak texture can make the visual result misleading.

### Saved video is missing, empty, or unplayable

All three video-output scripts try H.264 (`avc1`) first and fall back to `mp4v`. They do not verify that the fallback writer opens successfully, and their final saved-message is not a validation of the file. Check write permission, output size, actual playback, and your codec/backend support. Frame size and FPS come from the input clip metadata; the code does not validate those properties. Do not assume a successful exit proves a valid recording.

Output names are fixed or derived from the input; back up wanted recordings before another run. File mode has no window-key exit check. An emergency terminal interruption may leave a recording incomplete because the scripts do not wrap resource cleanup in `try/finally`.

### Markers detect but pose or AR looks wrong

Verify the `DICT_4X4_50` dictionary and the detected ID. AR objects appear only for IDs 8 and 9. The two pose examples use placeholder calibration and a fixed physical side length; printing at a different size or using different camera intrinsics makes pose geometry unreliable. No quantity labeled distortion, occlusion, translation, or depth in these examples should be treated as a calibrated measurement.
