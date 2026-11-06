import cv2 as computervision2
import time
import numpy as np
import HandTrackingModule as handtracking
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Open the first webcam and set the picture size to 640 by 480.
camera = computervision2.VideoCapture(0)
camera.set(computervision2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(computervision2.CAP_PROP_FRAME_HEIGHT, 480)

# Ask the detector to look for a hand with at least 70% confidence.
detector = handtracking.handDetector(detectionCon=0.7)

# Get the speakers that Windows is using.
speakers = AudioUtilities.GetSpeakers()

# This lets us change the main volume on the computer.
interface = speakers.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volumeControl = cast(interface, POINTER(IAudioEndpointVolume))

# Windows gives us the lowest and highest volume in decibels.
volumeRange = volumeControl.GetVolumeRange()
lowestVolume = volumeRange[0]
highestVolume = volumeRange[1]

# Start with an empty volume bar until the camera sees a hand.
barTop = 400
volumePercent = 0
previousTime = time.time()

while True:
    # Read one picture from the webcam.
    success, picture = camera.read()
    if not success:
        print("Could not read the webcam.")
        break

    # Flip the picture so it feels like looking in a mirror.
    picture = computervision2.flip(picture, 1)

    # Find the hands, then get the points for the first hand.
    picture = detector.findHands(picture)
    points = detector.findPosition(picture, draw=False)

    if len(points) > 8:
        # Point 4 is the tip of the thumb. Point 8 is the tip of the index finger.
        # Each point holds three numbers: its number, its x position and its y position.
        thumbX, thumbY = points[4][1], points[4][2]
        fingerX, fingerY = points[8][1], points[8][2]

        # Find the spot halfway between the two fingertips.
        middleX = (thumbX + fingerX) // 2
        middleY = (thumbY + fingerY) // 2

        # Draw a pink dot on each fingertip and a line between them.
        pink = (255, 0, 255)
        computervision2.circle(picture, (thumbX, thumbY), 15, pink, computervision2.FILLED)
        computervision2.circle(picture, (fingerX, fingerY), 15, pink, computervision2.FILLED)
        computervision2.line(picture, (thumbX, thumbY), (fingerX, fingerY), pink, 3)

        # Measure the gap between the fingertips in pixels.
        gap = math.hypot(fingerX - thumbX, fingerY - thumbY)

        # A gap of 50 pixels or less gives the lowest volume.
        # Move the fingers farther apart to turn it up. At 300 pixels it reaches full volume.
        volume = np.interp(gap, [50, 300], [lowestVolume, highestVolume])
        volumeControl.SetMasterVolumeLevel(volume, None)
        print(int(gap), volume)

        # The bottom of the bar is at y = 400. Smaller y values are higher on the screen.
        barTop = np.interp(gap, [50, 300], [400, 150])
        volumePercent = np.interp(gap, [50, 300], [0, 100])

        # Make the middle dot green when the fingertips are close together.
        middleColor = pink
        if gap < 50:
            middleColor = (0, 255, 0)
        computervision2.circle(picture, (middleX, middleY), 15, middleColor, computervision2.FILLED)

    # Draw the outline of the volume bar, then fill it from the bottom.
    blue = (255, 0, 0)
    computervision2.rectangle(picture, (50, 150), (85, 400), blue, 3)
    computervision2.rectangle(picture, (50, int(barTop)), (85, 400), blue, computervision2.FILLED)

    # Write the volume percentage below the bar.
    computervision2.putText(
        picture, f"{int(volumePercent)} %", (40, 450),
        computervision2.FONT_HERSHEY_COMPLEX, 1, blue, 3
    )

    # Use the time between two pictures to work out the frames per second (FPS).
    currentTime = time.time()
    fps = 1 / (currentTime - previousTime)
    previousTime = currentTime

    computervision2.putText(
        picture, f"FPS: {int(fps)}", (40, 50),
        computervision2.FONT_HERSHEY_COMPLEX, 1, blue, 3
    )

    # Show the picture. Press q in the camera window to quit.
    computervision2.imshow("Hand Volume Control", picture)
    if computervision2.waitKey(1) & 0xFF == ord("q"):
        break

# Turn off the webcam and close the window.
camera.release()
computervision2.destroyAllWindows()
