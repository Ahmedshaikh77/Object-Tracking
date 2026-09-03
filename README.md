# Object Tracking and Optical Flow with OpenCV

Seven standalone Python demonstrations of interactive object tracking, sparse and dense optical flow, and ArUco marker detection. Start with the bundled videos; webcam examples are optional. These are visual experiments, not a benchmarked tracking system or a calibrated measurement tool.

## Start with a bundled video

Run commands from the repository root, the directory containing `src/`, `assets/`, and `requirements.txt`. The scripts use paths relative to your current working directory, not their own location.

### 1. Prepare a desktop Python environment

Use a Python version with wheels for the pinned packages, such as Python 3.11, and an interactive desktop session. [NumPy 2.2.4 requires Python 3.10 or newer](https://pypi.org/project/numpy/2.2.4/); that minimum does not guarantee support for every newer interpreter or platform.

On macOS/Linux, with Python 3.11 installed:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install numpy==2.2.4 opencv-contrib-python==4.11.0.86
```

On Windows PowerShell, the equivalent environment setup is:

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install numpy==2.2.4 opencv-contrib-python==4.11.0.86
```

**Existing dependency-file caveat:** `requirements.txt` lists both `opencv-python==4.11.0.86` and `opencv-contrib-python==4.11.0.86`, plus NumPy. Both OpenCV distributions provide the same `cv2` module. The [OpenCV package maintainers recommend installing only one](https://pypi.org/project/opencv-contrib-python/4.11.0.86/). The commands above deliberately select the full desktop **contrib** package at the repository's existing version; they do not modify `requirements.txt`. Do not additionally install the main or headless wheel into this environment. The tracker script needs `cv2.legacy`, and the interactive examples need OpenCV window support.

Check the imports without opening a camera or window:

```bash
python -c "import cv2, numpy; print('OpenCV:', cv2.__version__, 'NumPy:', numpy.__version__)"
python -c "import cv2; print(cv2.legacy.TrackerCSRT_create); print(cv2.aruco.ArucoDetector); print(cv2.aruco.estimatePoseSingleMarkers)"
```

The versions should report `4.11.0` and `2.2.4`. The second command checks representative APIs, not camera access, codecs, or tracking quality. See [troubleshooting](docs/USAGE.md#troubleshooting) if it fails.

### 2. Run dense optical flow

```bash
python src/optical_flow_f.py
```

Enter `1` at the terminal prompt. The script reads `assets/alligator_short.mp4` and opens a color-coded motion-field window. Focus that window and press **Esc** to stop, or let the clip finish. It does not use your webcam or download a model.

Enter `2` instead to write `dense_optical_flow_output.mp4` in the repository root. Existing output at that path can be overwritten. File mode does not show a preview or poll for an Esc key; allow processing to finish. Codec support depends on your OpenCV build.

### 3. Try an object bounding box

```bash
python src/object_tracking.py
```

Enter `1` for the **CSRT tracker**, then `1` again for **screen output**. On the first frame of `assets/plane_short.mp4`, drag a rectangle around the object and press **Enter** or **Space**. A green box follows successful tracker updates; a failure message appears when an update fails. Press **Esc** in the playback window to exit. Selecting file output still requires the initial graphical rectangle selection.

## Choose an example

All commands below run from the repository root. There are no command-line options for video paths, cameras, outputs, or calibration; customization currently requires an explicit source edit.

| Script | Input as committed | Readiness and behavior |
| --- | --- | --- |
| [object_tracking.py](src/object_tracking.py) | Bundled `assets/plane_short.mp4` | Interactive rectangle selection; seven legacy tracker choices; screen or file output. |
| [optical_flow_f.py](src/optical_flow_f.py) | Bundled `assets/alligator_short.mp4` | Dense Farneback flow; screen or file output; simplest no-camera example. |
| [optical_flow_lk.py](src/optical_flow_lk.py) | Bundled `assets/alligator_short.mp4` | Sparse Lucas-Kanade flow from a fixed feature-detection rectangle; screen or file output. |
| [optical_flow_lk_blob.py](src/optical_flow_lk_blob.py) | Webcam index `0` | Draw feature-selection regions on a captured first frame; screen output only. |
| [aruco_markers.py](src/aruco_markers.py) | Webcam index `0` | Detects `DICT_4X4_50` markers; shows IDs and continually overwrites `frame.jpg`. |
| [aruco_markers_advanced.py](src/aruco_markers_advanced.py) | Webcam index `0` | Experimental marker diagnostics and pose axes; dummy calibration; overwrites `frame.jpg`. |
| [aruco_markers_AR.py](src/aruco_markers_AR.py) | Webcam index `0` | Experimental pose-based overlays for marker IDs `8` and `9`; dummy calibration; no saved output. |

The four webcam scripts need a working camera and OS camera permission. The two pose examples need real camera calibration and a correctly measured marker size before their geometry can be treated as a measurement. No calibration file or calibration workflow is supplied. None of the seven scripts loads an external model or references a missing dataset; the bundled-video scripts have complete input paths as committed.

## Included assets and outputs

- [plane_short.mp4](assets/plane_short.mp4): input for object tracking.
- [alligator_short.mp4](assets/alligator_short.mp4): input for both video optical-flow scripts.
- [aruco_markers_0.pdf](assets/aruco_markers_0.pdf) and [aruco_markers_1.pdf](assets/aruco_markers_1.pdf): supplied marker printouts; the Python scripts do not read these PDFs. Verify the detected IDs before trying the AR overlays; PDF filenames are not an AR ID specification.

Generated output paths are `assets/plane_short_<TRACKER>_tracked.mp4`, `optical_flow_output.mp4`, `dense_optical_flow_output.mp4`, and `frame.jpg`. These files may overwrite earlier runs. Webcam snapshots can include people or private surroundings; inspect them before sharing and keep generated captures out of contributions by default.

## Scope and documentation

There is no supplied ground-truth annotation, accuracy evaluation, runtime comparison, automatic object re-detection, or automated runtime test suite. A displayed box, feature track, or pose axis is a visualization, not proof of accuracy or real-time performance. The current sparse-flow and marker-diagnostic limitations are documented without changing their implementation.

- [Script-by-script usage and troubleshooting](docs/USAGE.md): prompts, controls, outputs, hard-coded settings, and known limitations.
- [Contributing](CONTRIBUTING.md): safe checks, useful bug reports, and changes that need separate validation.
