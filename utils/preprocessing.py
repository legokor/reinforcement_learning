import cv2
import imutils

def scale_frame(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = frame[24:, :]  # Drop upper part of frame  (heath bar, etc.)
    frame = imutils.resize(frame, width=160)  # Scale frane
    return frame
