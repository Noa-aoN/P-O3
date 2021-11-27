import cv2


def init_camera(source=1):

    cap = cv2.VideoCapture(source, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    return cap


def opencv_to_pygame(img):
    img = cv2.flip(img, 1, img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img
