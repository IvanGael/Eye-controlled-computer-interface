import cv2
import numpy as np
import pyautogui

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Set the dimensions of the screen
screen_width, screen_height = pyautogui.size()

# Set up haarcascade_eye.xml eye detector model 
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# To use local haarcascade_eye.xml file
# eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

# Parameters for click and scroll actions
click_threshold = 30  
scroll_threshold = 50 
prev_x, prev_y = 0, 0
scrolling = False

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect eyes in the frame
    eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)

    # If eyes are detected, find the center of the first detected eye
    if len(eyes) > 0:
        (ex, ey, ew, eh) = eyes[0]
        eye_center = (ex + ew // 2, ey + eh // 2)

        # Scale eye coordinates to screen resolution
        x = int(eye_center[0] * screen_width / cap.get(3))
        y = int(eye_center[1] * screen_height / cap.get(4))

        # Move the cursor
        pyautogui.moveTo(x, y)

        # Check for click action
        if abs(x - prev_x) < click_threshold and abs(y - prev_y) < click_threshold:
            pyautogui.click()

        # Check for scroll action
        if abs(x - prev_x) > scroll_threshold or abs(y - prev_y) > scroll_threshold:
            if not scrolling:
                scrolling = True
                pyautogui.mouseDown(button='middle')  
            pyautogui.moveRel(x - prev_x, y - prev_y)
        else:
            scrolling = False
            pyautogui.mouseUp(button='middle')

        # Update previous position
        prev_x, prev_y = x, y

    # Display the frame
    cv2.imshow('Gaze Tracking', frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the OpenCV window
cap.release()
cv2.destroyAllWindows()
