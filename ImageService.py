import cv2
import matplotlib.pyplot as plt

class ImageService:
    def __init__(self):
        self.cascPath = "/usr/local/lib/python3.9/site-packages/cv2/data/haarcascade_frontalface_default.xml"
        self.eyePath = "/usr/local/lib/python3.9/site-packages/cv2/data/haarcascade_eye.xml"
        self.smilePath = "/usr/local/lib/python3.9/site-packages/cv2/data/haarcascade_smile.xml"
        self.faceCascade = cv2.CascadeClassifier(self.cascPath)
        self.eyeCascade = cv2.CascadeClassifier(self.eyePath)
        self.smileCascade = cv2.CascadeClassifier(self.smilePath)

    def load_image(self, imagePath):
        img_bgr = cv2.imread(imagePath)
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        return img_rgb

    def spot_and_draw_faces(self, image):
        faces = self.faceCascade.detectMultiScale(
            image,
            scaleFactor=1.1,
            minNeighbors=5,
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        # For each face
        for (x, y, w, h) in faces:
            # Draw rectangle around the face
            cv2.rectangle(image, (x, y), (x+w, y+h), (255,255,255), 2)
        return faces

    def draw_image(self, image, with_faces=False):
        if with_faces:
            self.spot_and_draw_faces(image)
        plt.imshow(image)

        plt.axis('off')
        plt.show()