# face_recog.py

import face_recognition
import cv2
import camera
import os
import numpy as np
import time
import pickle


class FaceRecog():
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.camera = camera.VideoCamera()
        self.known_face_encodings = []

        self.known_face_names = []
        dirname = 'knowns'

        # Load sample pictures and learn how to recognize it.

        files = os.listdir(dirname)
        for filename in files:
            name, ext = os.path.splitext(filename)
            if ext == '.jpg':
                self.known_face_names.append(name)
                pathname = os.path.join(dirname, filename)
                img = face_recognition.load_image_file(pathname)
                face_encoding = face_recognition.face_encodings(img)[0]
                self.known_face_encodings.append(face_encoding)

        # Initialize some variables
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.process_this_frame = True
        self.face_cascade = cv2.CascadeClassifier('opencv_data/haarcascade_frontface.xml')

    def __del__(self):
        del self.camera

    def get_frame_raw(self):
        # Grab a single frame of video
        frame = self.camera.get_frame()
        return frame

    def get_frame(self):
        # Grab a single frame of video
        frame = self.camera.get_frame()

        # Resize frame of video to 1/4 size for faster face recognition processing
        #small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        #small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        #rgb_small_frame = small_frame[:, :, ::-1]
        rgb_small_frame = frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if self.process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            self.face_locations = face_recognition.face_locations(rgb_small_frame)
            self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

            self.face_names = []
            for face_encoding in self.face_encodings:
                # See if the face is a match for the known face(s)
                distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                min_value = min(distances)

                # tolerance: How much distance between faces to consider it a match. Lower is more strict.
                # 1.2 is typical best performance.
                name = "Unknown"
                if min_value < 1.2:
                    index = np.argmin(distances)
                    name = self.known_face_names[index]

                self.face_names.append(name)

        self.process_this_frame = not self.process_this_frame

        # Display the results
        for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            #top *= 2
            #right *= 2
            #bottom *= 2
            #left *= 2

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 1)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        return frame

    def get_jpg_bytes(self):
        frame = self.get_frame()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpg = cv2.imencode('.jpg', frame)
        return jpg.tobytes()

    def save_frame_to_image(self,pframe):
        # 전달 받은 frame을 저장 한다. frame = self.get_frame_raw()
        cv2.imwrite('images/findImage.jpg', pframe)

    def detect_any_person(self):
        # 카메라 각도 Angle of View (diagonal) : 69.1 degree
        # 사진의 오른쪽 위치
        # face_cascade = cv2.CascadeClassifier('opencv_data/haarcascade_frontface.xml')
        frame = self.get_frame_raw()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        target_angle = 0
        target_height = 0
        if len(faces) > 0:
            print("{} , {}".format(640 * 0.5, (x + w / 2)))
            print("{} , {}".format(480 * 0.5, (y + h / 2)))
            for (x, y, w, h) in faces:
                if (640 * 0.5 < (x + w / 2)):
                    target_angle = (34 / 320 * ((x + w / 2) - 480))
                if (self.camera.video_center_y * 0.5 < (y + h / 2)):
                    target_height = (0.5 / 240 * (480 - (y + h / 2)))

        return target_angle, target_height


    def drone_target_dest(self, pface_loc):
        if len(pface_loc) <= 0:
            return 0,0

        # 필요 변수 선언
        target_angle = 0
        target_height = 0
        p_index = 0
        result_loc = []

        for (x, y, w, h) in  pface_loc:
            target_x = y - h                                # 대상의 x좌표
            target_y = w - x                                # 대상의 y좌표
            target_angle = (34 / 320 * (target_x - 320))    # 픽셀의 비율에 따른 전환 각도 계산
            target_height = (0.5 / 240 * ( 240 - target_y)) # 픽셀의 비율에 따른 높낮이 계산
            result_loc.append([target_angle, target_height])
            p_index += 1

        #print(result_loc)
        #  여려명을 찾을경우 각도가 가장 적은 인원을 Target으로 함.
        result_loc.sort(key=lambda x:x[0])
        #print(result_loc)
        target_angle, target_height = result_loc[0]
        return round(target_angle,0), round(target_height,2)







def detect_person_detail(pface_recog, p_loopcount):
    #카메라 객체 활성화
    #face_recog = FaceRecog()
    # 찾는 사람 확인
    print(face_recog.known_face_names)

    # Return 변수 선언 및 반복 회수 변수 선언 및 초기화
    isFound = False
    lcount = 0

    #수행 시간 측정을 위한 변수
    start_time = time.time()

    # loop회수 만큼 반복 하면서 사진을 읽어 해당 사람을 찾는 while문
    while lcount < p_loopcount:

        lcount = lcount + 1

        # 카메라에서 frame 을 분석 하여 사람을 찾음.
        frame = pface_recog.get_frame()

        # show the frame
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # 인식된 얼굴 이 있다면
        if len(pface_recog.face_locations) > 0:
            isFound = True
            print('[LOG] 찾은 좌표 : ', pface_recog.face_locations)        # 찾은 좌표 출력
            pface_recog.save_frame_to_image(frame)   # 찾은 사진 저장

            #URL = 'http://localhost/checktrue'
            #data = {'data1': 'True'}
            #res = requests.post(URL, data=data)
            #res.request

            check = 'true'
            with open('check.ck', 'wb') as file:
                pickle.dump(check, file)
            
            break
        else:
            check = 'false'
            with open('check.ck', 'wb') as file:
                pickle.dump(check, file)

            # targetctl = face_recog.detect_person
            # print(targetctl)
            # face_recog.process_this_frame= False

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

    # do a bit of cleanup
    cv2.destroyAllWindows()
    # 검색시간 출력
    print('[LOG] 검색 시간(s) : ',time.time() - start_time, ' seconds')
    rtnLoc = face_recog.drone_target_dest(pface_recog.face_locations)

    return isFound, rtnLoc



if __name__ == '__main__':
    #URL = 'http://localhost/checkfalse'
    #data = {'data1': 'False'}
    #res = requests.post(URL, data=data)
    #res.request
    check = 'false'
    with open('check.ck', 'wb') as file:
        pickle.dump(check, file)

    face_recog = FaceRecog()
    isFound, drone_target_dest = detect_person_detail(face_recog, 60000 )   # 60회 -> 약 8초
    if isFound:
        print('[LOG] 사람을 찾았습니다.',isFound,'  드론 위치 조정 => ', drone_target_dest)
    else:
        print('[LOG] 사람이 없습니다.')

