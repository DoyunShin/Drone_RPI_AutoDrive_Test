import face_recognition
import camera
import cv2


def findperson():
    # 비교대상 사진 load
    sangjun_image = face_recognition.load_image_file("SangJun.jpg")
    # obama_image = face_recognition.load_image_file

    # 카메라 활성화 및 사진 저장
    piCamera = camera.VideoCamera()
    cv2.imwrite('unknown.jpg', piCamera.get_frame())
    cv2.destroyAllWindows()

    # 찍은 사진을 face_recognition에 load
    unknown_image = face_recognition.load_image_file("unknown.jpg")

    # Get the face encodings for each face in each image file
    # Since there could be more than one face in each image, it returns a list of encodings.
    # But since I know each image only has one face, I only care about the first encoding in each image, so I grab index 0.
    try:
        sangjun_face_encoding = face_recognition.face_encodings(sangjun_image)[0]
        # obama_face_encoding = face_recognition.face_encodings(obama_image)[0] 필요시 추가
        unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
    except IndexError:
        print("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")
        return False

    known_faces = [
        sangjun_face_encoding
        # obama_face_encoding 필요시 추가
    ]

    # results is an array of True/False telling if the unknown face matched anyone in the known_faces array
    results = face_recognition.compare_faces(known_faces, unknown_face_encoding)
    #results2 = face_recognition.

    print("Is the unknown face a picture of Sangjun? {}".format(results[0]))
    # print("Is the unknown face a picture of Obama? {}".format(results[1]))  필요시 추가
    # print("Is the unknown face a new person that we've never seen before? {}".format(not True in results))
    return results[0]


if __name__ == '__main__':
    isfound = findperson()
    print("인식확인 여부 => {}".format(isfound))