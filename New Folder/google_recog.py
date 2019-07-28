#!/usr/bin/env python

import cv2

from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw, ImageFont
import pickle

likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                   'LIKELY', 'VERY_LIKELY')

def detect_face(face_file, max_results=4):
    client = vision.ImageAnnotatorClient()

    content = face_file.read()
    image = types.Image(content=content)

    return client.face_detection(image=image, max_results=max_results).face_annotations

def highlight_image(image, faces, labels, output_filename):
    im = Image.open(image)
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype("arial.ttf", 15)
    # Sepecify the font-family and the font-size
    for face in faces:
        box = [(vertex.x, vertex.y)
               for vertex in face.bounding_poly.vertices]
        draw.line(box + [box[0]], width=5, fill='#00ff00')
        # Place the confidence value/score of the detected faces above the
        # detection box in the output image
        draw.text(((face.bounding_poly.vertices)[0].x,
                   (face.bounding_poly.vertices)[0].y - 70),
                  'anger: {}'.format(likelihood_name[face.anger_likelihood]),(0,0,255), font)

        draw.text(((face.bounding_poly.vertices)[0].x,
                   (face.bounding_poly.vertices)[0].y - 50),
                  'joy: {}'.format(likelihood_name[face.joy_likelihood]),(0,0,255), font)

        draw.text(((face.bounding_poly.vertices)[0].x,
                   (face.bounding_poly.vertices)[0].y - 30),
                  str(format(face.detection_confidence * 100, '.3f')) + ' %',(0,0,255), font)

    linecnt = 0
    # Sepecify the font-family and the font-size
    for label in labels:
        draw.text((20, 20 + linecnt*20),
                  label.description + ' : ' + str(format(label.score*100, '.3f')) + ' %', (0, 0, 255), font)
        linecnt += 1

    im.save(output_filename)


# [START gAPI_call_main]
def gAPI_call_main(input_filename, output_filename, max_results):
    with open(input_filename, 'rb') as image:
        faces = detect_face(image, max_results)

        print('Found {} face{}'.format(
            len(faces), '' if len(faces) == 1 else 's'))

        print('Writing to file {}'.format(output_filename))
        # Reset the file pointer, so we can read the file again

        # 라벨 검색
        #labels = detect_labels(image)
        client1 = vision.ImageAnnotatorClient()
        image.seek(0)
        content1 = image.read()
        image1 = types.Image(content=content1)

        # Performs label detection on the image file
        response = client1.label_detection(image=image1)
        labels = response.label_annotations
        print('detect_labels')
        image.seek(0)

        highlight_image(image, faces, labels, output_filename)
        print('highlight_image')
# [END gAPI_call_main]



if __name__ == '__main__':
    gAPI_call_main('images/findImage_org.jpg', 'images/findImage_google.jpg', 4)

    # 사진 보여주기 - 불필요시 주석처리.
    check = 'true'
    with open('status.ck', 'wb') as file:
        pickle.dump(check, file)

    image = cv2.imread("images/findImage_google.jpg", cv2.IMREAD_ANYCOLOR)
    cv2.imshow("Moon", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
