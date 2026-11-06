# Hand Gesture Volume Control

I built a custom Python module, `HandTrackingModule.py`, to track hand movements with a webcam. In this project, I use it to control the volume on a Windows computer. I raise my middle finger to adjust the volume with my thumb and index finger, then fold my middle finger to lock the setting.

## What makes this volume controller different?

My first version mapped a fingertip gap of 50–300 pixels directly to volume. That meant I could turn the volume up just by moving my hand closer to the webcam, even if I held my fingers still. I made two changes:

- **Use palm width as a reference.** I divide the thumb-to-index gap by the width of my palm. A 60-pixel gap across a 100-pixel palm gives the same reading as a 90-pixel gap across a 150-pixel palm. This makes the control less sensitive to how far I sit from the webcam.
- **Choose when to adjust.** With my palm upright, I raise my middle finger to set the volume. When I reach the level I want, I fold that finger. The window shows **Volume locked**, and I can bring my thumb and index finger back together without turning the sound down.

## Project files

| File | What it does |
| --- | --- |
| `HandTrackingModule.py` | My reusable hand tracker. It uses MediaPipe to locate hand landmarks and returns their pixel coordinates. Run this file on its own to test tracking with the webcam. |
| `volume_control.py` | The main script. It compares fingertip spread with palm width, checks the middle-finger gesture, and uses Pycaw to set the Windows speaker volume. The webcam window shows the volume bar and whether the control is locked. |
| `README.md` | Explains how the gesture controls volume and how to install, run, and troubleshoot the project. |

## The hand-tracking module

A **landmark** is a point on the hand, such as a fingertip or a knuckle. My module uses MediaPipe’s pretrained hand model to locate these points. I wrote the code that passes each camera frame to the model, converts its results into pixel coordinates, and makes those coordinates available to the volume controller.

| Method | What it does |
| --- | --- |
| `findHands(img)` | Converts the camera frame from OpenCV’s BGR color order to RGB, runs the hand model, and optionally draws the hand outline. |
| `findPosition(img)` | Uses the latest detection to return the points for one hand as a list of `[point number, x, y]` values. It returns an empty list when no hand is visible. |

I later reused this same module in my two-hand finger counter. Each project has its own gesture rules, but both read the hand points in the same way. you can check the project at : https://github.com/aditya162006/Two-Hand-Finger-Counter

## How a gesture changes the volume

I measure two distances in each frame: the gap between the thumb and index fingertips (points 4 and 8), and the width of the palm between the base of the index finger and the base of the pinky (points 5 and 17).

```python
fingerSpread = gap / palmWidth
```

| Finger spread while adjusting | Blue bar | Windows volume setting |
| --- | --- | --- |
| 0.20 or less | 0% | Device minimum |
| 0.85 | 50% | Midpoint of the device’s decibel range |
| 1.50 or more | 100% | Device maximum |

NumPy maps the spread to the device’s volume range, and Pycaw sends the setting to Windows. With the palm upright, the controller checks whether the middle fingertip (point 12) is above its middle joint (point 10). Folding that finger locks the last setting.

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

1. Face your palm toward the webcam with your fingers pointing up. Raise your middle finger until the window shows **Adjusting volume**.
2. Spread your thumb and index finger to turn the volume up. Bring them together to turn it down.
3. Fold your middle finger. When **Volume locked** appears, you can move your thumb without changing the setting. Raise the middle finger again to resume.

Click the camera window and press **q** to quit.

To use the **▶ Run Python File** button in VS Code, press **Ctrl+Shift+P**, choose **Python: Select Interpreter**, and select the Python inside `.venv`. Then open `volume_control.py` and click ▶.

 by **Aditya Mishra**.

