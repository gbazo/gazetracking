"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""

import cv2
import imutils
from gaze_tracking import GazeTracking

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

estado_atv = 0
estado_desv = 0

while True:
    # We get a new frame from the webcam
    _, frame = webcam.read()

    #frame = imutils.resize(frame, width=800)

    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)

    frame = gaze.annotated_frame()
    text = ""

    #if gaze.is_blinking():
    #    text = "Blinking"
    if gaze.is_center() or gaze.is_down():
        text = "Atividade"
        estado_atv += 1
    else:
        text = "Desviou olhar"
        estado_desv +=1

    cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.2, (147, 58, 31), 2)

    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()
    #cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.5, (147, 58, 31), 1)
    #cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.5, (147, 58, 31), 1)

    cv2.imshow("Demo", frame)

    if cv2.waitKey(1) == 27:
        break


print("Tempo em atividade (s): ", round(estado_atv/30))
print("Tempo em desvio de olhar (s): ", round(estado_desv/30))

cv2.destroyAllWindows()