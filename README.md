# Hand Gesture Volume Control

I built a custom Python module, `HandTrackingModule.py`, to track hand movements with a webcam. In this project, I use it to control the volume on a Windows computer. Spreading my thumb and index finger raises the volume, and bringing them together lowers it.

## Project files

| File | What it does |
| --- | --- |
| `HandTrackingModule.py` | My reusable hand tracker. It uses MediaPipe to locate hand landmarks and returns their pixel coordinates. Run this file on its own to test tracking with the webcam. |
| `volume_control.py` | The main script. It uses the tracker to find the thumb and index fingertips, measures the gap between them, and uses Pycaw to set the Windows speaker volume. It draws the blue volume bar on the webcam image. |


## The hand-tracking module

A **landmark** is a point on the hand, such as a fingertip or a knuckle. My module uses MediaPipe’s pretrained hand model to locate these points. I wrote the code that passes each camera frame to the model, converts its results into pixel coordinates, and makes those coordinates available to the volume controller.

| Method | What it does |
| --- | --- |
| `findHands(img)` | Converts the camera frame from OpenCV’s BGR color order to RGB, runs the hand model, and optionally draws the hand outline. |
| `findPosition(img)` | Uses the latest detection to return the points for one hand as a list of `[point number, x, y]` values. It returns an empty list when no hand is visible. |

Keeping these steps in a separate file lets me test the tracker on its own or reuse it for another gesture.

## How a gesture changes the volume

The controller reads **point 4** (thumb tip) and **point 8** (index fingertip). It measures the straight-line distance between them in the camera image. In Python, that calculation is:

```python
gap = math.hypot(fingerX - thumbX, fingerY - thumbY)
```

I used two distances, **50 pixels** and **300 pixels**, as the lower and upper limits. NumPy’s `interp` function maps the gap to the speaker’s volume range in decibels (dB). Pycaw sends that value to Windows. The blue bar shows where the gesture falls within the chosen range.

| Fingertip gap | Blue bar | Volume sent to Windows |
| --- | --- | --- |
| 50 pixels or less | 0% | Device minimum |
| 175 pixels | 50% | Halfway between the minimum and maximum dB values |
| 300 pixels or more | 100% | Device maximum |

**Try this:** hold your fingers a fixed distance apart and move your hand toward the webcam. The gap takes up more pixels, so the volume can rise even though your fingers stayed in the same position relative to each other. For steadier control, keep your hand roughly the same distance from the camera.

## Set it up in VS Code

You need a Windows laptop or desktop, a webcam, and 64-bit Python 3.11 or 3.12.

1. Download both Python files into the same folder on your laptop. In the VS Code desktop app, choose **File → Open Folder** and open that folder.
2. Choose **Terminal → New Terminal** and select **PowerShell**. The prompt should show a local path such as `PS C:\Users\YourName\computer_vision>`. A path starting with `/workspaces/` means you are still in the Codespace. Run this project locally so it can use your webcam and speakers.
3. Check which Python versions are installed.

   ```powershell
   py -0p
   ```

4. Create an environment for the project. For Python 3.11, run the command below. For Python 3.12, use `py -3.12 -m venv .venv` instead.

   ```powershell
   py -3.11 -m venv .venv
   ```

5. Install the packages. You only need to do this once for this environment.

   ```powershell
   .\.venv\Scripts\python.exe -m pip install "mediapipe==0.10.21" "opencv-contrib-python==4.11.0.86" "numpy<2" "pycaw==20240210" comtypes
   ```

## Run the volume controller

From the same PowerShell terminal, run:

```powershell
.\.venv\Scripts\python.exe volume_control.py
```

Hold one hand in front of the webcam. A pink line joins your thumb and index finger. Slowly spread them and watch the blue bar rise. Bring them close together and the middle dot turns green. Keep your hand about the same distance from the camera while you try it.

Click the camera window and press **q** to quit.

To use the **▶ Run Python File** button in VS Code, press **Ctrl+Shift+P**, choose **Python: Select Interpreter**, and select the Python inside `.venv`. Then open `volume_control.py` and click ▶.


by **Aditya Mishra**.
