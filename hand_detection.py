import numpy as np
import cv2 as cv
"""
gebruikte site: https://medium.com/analytics-vidhya/hand-detection-and-finger-counting-using-opencv-python-5b594704eb08 
"""

def skin_mask(img):
    hsvim = cv.cvtColor(img, cv.COLOR_BGR2HSV) # kleur omzetten naar hsv
    lower = np.array([0, 48, 80], dtype="uint8")
    upper = np.array([20, 255, 255], dtype="uint8")
    skinRegionHSV = cv.inRange(hsvim, lower, upper) # lijst maken, elementsgewijs upper en lowerbound gebruiken
    blurred = cv.blur(skinRegionHSV, (2, 2)) # tuple geeft intensiteit blur aan
    ret, thresh = cv.threshold(blurred, 0, 255, cv.THRESH_BINARY)
    #cv.imshow("thresh", thresh)
    return thresh


def get_cnthull(mask_img): # maakt rand rond hand
    contours, hierarchy = cv.findContours(mask_img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    contours = max(contours, key=lambda x: cv.contourArea(x))
    hull = cv.convexHull(contours)
    return contours, hull


def get_defects(contours):
    hull = cv.convexHull(contours, returnPoints=False)
    defects = cv.convexityDefects(contours, hull)
    return defects

if __name__ == "__main__": # main functie maken
    cap = cv.VideoCapture(0)  # '0' om webcam te gebruiken
    while True: # break bij het indrukken van q, zie einde while
        _, img = cap.read()
        try:
            mask_img = skin_mask(img)
            contours, hull = get_cnthull(mask_img)
            cv.drawContours(img, [contours], -1, (255, 255, 0), 2)
            cv.drawContours(img, [hull], -1, (0, 255, 255), 2)
            defects = get_defects(contours)
            if defects is not None:
                cnt = 0
                for i in range(defects.shape[0]):  # hoek berekenen
                    s, e, f, d = defects[i][0]
                    start = tuple(contours[s][0])
                    end = tuple(contours[e][0])
                    far = tuple(contours[f][0])
                    a = np.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2) # lengtes berekenen
                    b = np.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
                    c = np.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
                    angle = np.arccos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))  # cosinusregel
                    if angle <= np.pi / 2:  # hoeken die minder dan 90 graden zijn als vingers beschouwen
                        cnt += 1
                        cv.circle(img, far, 4, [0, 0, 255], -1) # vingers aanduiden met een vol punt
                if cnt > 0:
                    cnt = cnt + 1
                cv.putText(img, str(cnt), (0, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv.LINE_AA)
            cv.imshow("beeld", img) # beeld laten zien
        except:
            pass
        if cv.waitKey(1) == ord('q'): # uit while True raken
            break
    cap.release() # alles sluiten
    cv.destroyAllWindows()