import cv2
from gaze_tracking import GazeTracking
from imutils.video import VideoStream
import imutils
import argparse
import time

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
args = vars(ap.parse_args())

gaze = GazeTracking()

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
	vs = VideoStream(src=0).start()
# otherwise, grab a reference to the video file
else:
	vs = cv2.VideoCapture(args["video"])
# allow the camera or video file to warm up
time.sleep(2.0)

count = 0

while True:

	t = time.time()

	frame = vs.read()

	frame = frame[1] if args.get("video", False) else frame
	
	if frame is None:
		break

	gaze.refresh(frame)

	frame = gaze.annotated_frame()
	text = ""

	#if gaze.is_blinking():
	#	text = "Blinking"
	if gaze.is_right():
		text = "DIREITA"
	elif gaze.is_left():
		text = "ESQUERDA"
	elif gaze.is_center():
		text = "FRENTE"
	else:
		text = "DEVIOU"

	cv2.putText(frame, text, (850, 60), cv2.FONT_HERSHEY_DUPLEX, 1.4, (147, 58, 31), 2)


	#left_pupil = gaze.pupil_left_coords()
	#right_pupil = gaze.pupil_right_coords()
	#cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.5, (147, 58, 31), 1)
	#cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.5, (147, 58, 31), 1)


	cv2.imwrite("/home/gabriel/Documentos/blur_face/frame%d.jpg" % count, frame)
	count += 1

	print("Time to process the frame = {}".format(time.time() - t))
	

# close all windows
cv2.destroyAllWindows()