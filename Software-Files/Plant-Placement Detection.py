import cv2
import numpy as np
import os
import time
import math

os.system('cls')

# Check if the video file exists
v_f_path = r"C:\Users\udhay\OneDrive\Desktop\PalletClip.wmv"
if os.path.exists(v_f_path):
    print(f"The video file '{v_f_path}' exists.")
else:
    print(f"The video file '{v_f_path}' does not exist.")

#store capture frames
cap = cv2.VideoCapture(r"C:\Users\udhay\OneDrive\Desktop\PalletClip.wmv")

roi_x, roi_y, roi_w, roi_h = 25, 25, 55, 55

p=0
n=0
q=0
while True:
    # Read a frame from the video
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to create a binary image
    _, binary = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)

    # Find contours in the binary image
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #roi = frame[0: 100, 0: 100]

    # Filter contours based on area 
    min_circle_area = 100
    dark_circles = [cnt for cnt in contours if cv2.contourArea(cnt) > min_circle_area]

    # Draw bounding boxes or circles around the dark circles
    for cnt in dark_circles:
        (x, y), radius = cv2.minEnclosingCircle(cnt)
        center = (int(x), int(y))
        radius = int(radius)
        area = math.pi * radius * radius
        if roi_x <= center[0] <= roi_x + roi_w and roi_y <= center[1] <= roi_y + roi_h:

            # Print screen coordinates of the circle within the ROI
            print(f"Circle at coordinates ({center[0]}, {center[1]}) with area {area} in the ROI")

            # Draw the circle on the frame
            cv2.circle(frame, center, radius, (0, 255, 0), 2)  # Green circle

    # Draw the ROI rectangle on the frame
    cv2.rectangle(frame, (roi_x, roi_y), (roi_x + roi_w, roi_y + roi_h), (0, 0, 255), 2)  # Red rectangle

    if ret:
    # Display the original frame with identified dark circles
        cv2.imshow('Dark Circles Detection', frame)
        #cv2.imshow('ROI', binary)
    else:
        break

    # Increment the ROI y-coordinate for the next iteration
    #roi_y += 10  # You can adjust the step size as needed

    time.sleep(0.5)
    roi_y = 135 + p
    p=p+110
    if n == 4:
        roi_x, roi_y, roi_w, roi_h = 25, 25, 55, 55
        roi_x = 135+q
        q=q+110
        p=0
        n=0
    else:
        n=n+1
    
    

    #the pause duration between each frame
    key = cv2.waitKey(30)
    # "z" key = 122
    if key == 122:
        break

# Release the video capture object and close windows
cap.release()
cv2.destroyAllWindows()
