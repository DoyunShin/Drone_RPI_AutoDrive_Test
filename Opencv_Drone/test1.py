import face_recognition
import cv2
import camera
import os
import numpy as np
import face_recog

face_recog1 = face_recog.FaceRecog()

print(face_recog1.known_face_names)

face_recog1.isEnabled_recog = False
face_recog1.save_frame_to_image()




