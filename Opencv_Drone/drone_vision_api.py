import os
import io

def google_detect_faces(path):
    """Detects faces in an image."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()
    with io.open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)


    response = client.face_detection(image=image)
    faces = response.face_annotations

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',  'LIKELY', 'VERY_LIKELY')
    print('Found {} face{}'.format(len(faces), '' if len(faces) == 1 else 's'))
    print('Faces:')
    for face in faces:
        print('anger: {}'.format(likelihood_name[face.anger_likelihood]))
        print('joy: {}'.format(likelihood_name[face.joy_likelihood]))
        print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))
        vertices = (['({},{})'.format(vertex.x, vertex.y)
                     for vertex in face.bounding_poly.vertices])
        print('face bounds: {}'.format(','.join(vertices)))



def run():
    cpath="C:/Users/SASHIN/PycharmProjects/Test01/pic1.jpg"
    google_detect_faces(cpath)

if __name__ == "__main__":
    run()