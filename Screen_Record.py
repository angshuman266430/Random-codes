import cv2
import numpy as np
import pyautogui
import time

# Get the screen size
screen_size = (screen_width, screen_height) = pyautogui.size()

# Define the codec and create a VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*"XVID")
output_file = "screen_record.avi"
out = cv2.VideoWriter(output_file, fourcc, 10.5, screen_size)

# Set the time for recording (in seconds)
record_time = 60

# Record the screen
start_time = time.time()
while time.time() - start_time < record_time:
    # Capture the current screen
    img = pyautogui.screenshot()

    # Convert the image to a numpy array
    frame = np.array(img)

    # Convert the image from RGB to BGR (OpenCV format)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # Write the frame to the output file
    out.write(frame)

    # Display the recording screen
    cv2.imshow("Screen Recording", frame)

    # Stop recording when the 'q' key is pressed
    if cv2.waitKey(1) == ord("q"):
        break

# Release the VideoWriter object and close the display window
out.release()
cv2.destroyAllWindows()
