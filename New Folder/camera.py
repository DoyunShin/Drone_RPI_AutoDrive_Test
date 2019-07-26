# camera.py

import cv2

class VideoCamera(object):
    def __init__(self):
        # 내 PC 카메라 사용
        self.video = cv2.VideoCapture(0)
        # self.video.set(3, 640)
        # self.video.set(4, 480)

        # 파일에서 영상을 사용 시
        #self.video = cv2.VideoCapture('abc.mp4')
        
        # URL 스트리밍에서 가져올시 - PI zero
        #self.video = cv2.VideoCapture('http://192.168.0.23:8090/?action=stream')

        # 비디오 size
        self.video_width = self.video.get(3)
        self.video_height = self.video.get(4)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        # Grab a single frame of video
        ret, frame = self.video.read()
        return frame


if __name__ == '__main__':
    cam = VideoCamera()
    print(cam.video_height," x ",cam.video_width)
    print()
    while True:
        frame = cam.get_frame()

        # show the frame
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

    # do a bit of cleanup
    cv2.destroyAllWindows()
    print('finish')
