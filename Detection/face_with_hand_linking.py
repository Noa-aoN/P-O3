from Detection.gestures_mediapipe import hand_position
from Detection.mediapipe_pose import linkfacewithhand
from Style import font, font_small, WHITE, BLACK, GREEN, RED
from cv2 import rectangle


def face_gest_crop(img, game, facecoords, handcoords):
    h, w, c = img.shape
    leftdist = abs(facecoords[0][0] - handcoords[2] * w)
    rightdist = abs(facecoords[0][0] + facecoords[0][2] - handcoords[2] * w)
    player = game.get_current_player()
    if leftdist > rightdist:
        hands = handcoords[2] * w + 150
        if hands > w:
            hands = w
        img = img[:, facecoords[0][0]:int(hands)]
    else:
        hands = handcoords[2] * w - 150
        if hands - 150 < 0:
            hands = 0
        img = img[:, int(hands):facecoords[0][0] + facecoords[0][2]]

    facecoords = game.library.searchplayer(player.name, img)
    landmarklist = game.landmarkgetter(img)
    if landmarklist:
        handcoords = hand_position(landmarklist[0])
    return img, facecoords, handcoords


def get_landmark_list(image, game, screen, landmarklist):
    current_player = game.get_current_player()
    if facecoords := game.library.searchplayer(current_player.name, image):
        x, y, w, h = facecoords[0]
        detect_text = 'Player Recognized'
        rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 7)
    else:
        detect_text = 'Player Not Found'

    detect_surf = font_small.render(detect_text, False, RED)
    screen.blit(detect_surf, detect_surf.get_rect(topleft=(45 + 290 * current_player.number, 400)))

    templandmarklist = []
    for landmark in landmarklist:
        handcoords = hand_position(landmark)
        if facecoords and handcoords:
            if game.with_linking:
                img, facecoords, handcoords = face_gest_crop(image, game, facecoords, handcoords)
                valid = False
                if facecoords:
                    img, valid = linkfacewithhand(img, facecoords[0], handcoords)
                if valid:
                    templandmarklist.append(landmark)
            else:
                templandmarklist.append(landmark)
    return templandmarklist, image