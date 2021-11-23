import cv2

import numpy as np
import time

from Deck import Card, SUITS, RANKS

FONT = cv2.FONT_HERSHEY_PLAIN

MAX_CARD_AREA = 400000
MIN_CARD_AREA = 10000

RANK_DIFF_MAX = 3000
SUIT_DIFF_MAX = 1500

RANK_WIDTH = 70
RANK_HEIGHT = 100

SUIT_WIDTH = 100
SUIT_HEIGHT = 100

URL = "http://192.168.43.1:8080/shot.jpg"

SUITS_IMG = [cv2.imread(f"Images/Moulds/{suit}.jpg", cv2.IMREAD_GRAYSCALE) for suit in SUITS]
RANKS_IMG = [cv2.imread(f"Images/MyMoulds/{rank}.jpg", cv2.IMREAD_GRAYSCALE) for rank in RANKS]

TEMPLATE_SUITS_IMG = cv2.imread("ReferenceSuits.jpg", cv2.IMREAD_GRAYSCALE)
TEMPLATE_RANKS_IMG = cv2.imread("ReferenceRanks.jpg", cv2.IMREAD_GRAYSCALE)


def empty(_):
    pass


cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters", 600, 120)
cv2.createTrackbar("Contour", "Parameters", 140, 255, empty)
cv2.createTrackbar("Thresh Card", "Parameters", 190, 255, empty)


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = (te - ts) * 1000
        else:
            print('%r  %2.2f ms' % (method.__name__, (te - ts) * 1000))
        return result

    return timed


def binary_threshold(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)

    # img_w, img_h = np.shape(image)[:2]
    # bkg_level = gray[int(img_h / 100)][int(img_w / 2)]
    thresh_level = cv2.getTrackbarPos("Contour", "Parameters")  # + bkg_level
    retval, thresh = cv2.threshold(blur, thresh_level, 255, cv2.THRESH_BINARY)

    return thresh


def detect_cards(thresh):
    card_cnts_pts = []
    cnts, hiers = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Card when: min < area < max, no parents, four corners

    for i, contour in enumerate(cnts):
        area = cv2.contourArea(contour)
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.01 * peri, True)

        if MIN_CARD_AREA < area < MAX_CARD_AREA and hiers[0][i][3] == -1 and len(approx) == 4:
            pts = np.float32(approx)
            card_cnts_pts.append((contour, pts))

    return card_cnts_pts


def create_card(contour, pts, image):
    average = np.sum(pts, axis=0) / len(pts)
    center = (int(average[0][0]), int(average[0][1]))

    # Warp card into 285x435 flattened image using perspective transform
    x, y, w, h = cv2.boundingRect(contour)
    warp = transform(image, pts, w, h)

    corner_zoom = warp[2:110, 2:45]

    thresh_level = cv2.getTrackbarPos("Thresh Card", "Parameters")
    retval, corner_thresh = cv2.threshold(corner_zoom, thresh_level, 255, cv2.THRESH_BINARY)

    rank_img = corner_thresh[4:66, 0:50]
    suit_img = corner_thresh[62:110, 0:48]

    """if rank_img.all() == 0 and suit_img.all() == 0:
        return Card(contour, pts, w, h, center, 14, 14), Card(contour, pts, w, h, center, 14, 14)"""

    disp_rank = rank_img.copy()

    # Inverting!
    rank_cnts, hier = cv2.findContours(np.invert(rank_img), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    rank_cnts = sorted(rank_cnts, key=cv2.contourArea, reverse=True)
    rank_cnts = list(filter(lambda cnt: cv2.contourArea(cnt) > 350, rank_cnts))

    rank = -1
    suit = -1
    t_rank = -1
    t_suit = -1

    if len(rank_cnts) > 0:
        x1, y1, w1, h1 = cv2.boundingRect(rank_cnts[0])
        rank_img = rank_img[y1:y1 + h1, x1:x1 + w1]
        cv2.rectangle(disp_rank, (x1, y1), (x1 + w1, y1 + h1), (0, 0, 0), 2)
        rank_img = cv2.resize(rank_img, (RANK_WIDTH, RANK_HEIGHT), 0, 0)
        rank = find_match(rank_img, RANKS_IMG, RANK_DIFF_MAX)
        t_rank = template_matching(rank_img, "template rank", 14, TEMPLATE_RANKS_IMG.copy())

    suit_cnts, hier = cv2.findContours(np.invert(suit_img), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    suit_cnts = sorted(suit_cnts, key=cv2.contourArea, reverse=True)

    disp_suit = suit_img.copy()

    if len(suit_cnts) > 0:
        x1, y1, w1, h1 = cv2.boundingRect(suit_cnts[0])
        suit_img = suit_img[y1:y1 + h1, x1:x1 + w1]
        cv2.rectangle(disp_suit, (x1, y1), (x1 + w1, y1 + h1), (0, 0, 0), 2)
        suit_img = cv2.resize(suit_img, (SUIT_WIDTH, SUIT_HEIGHT), 0, 0)
        suit = find_match(suit_img, SUITS_IMG, SUIT_DIFF_MAX)
        t_suit = template_matching(suit_img, "template suit", 4, TEMPLATE_SUITS_IMG.copy())

    cv2.imshow("Rank / Suit", cv2.vconcat([disp_rank, disp_suit]))
    # cv2.imshow("Suit Cut", suit_img)
    # cv2.imshow("Rank Cut", rank_img)

    mould_card = Card(contour, pts, w, h, center, rank, suit)
    tm_card = Card(contour, pts, w, h, center, t_rank, t_suit)

    return mould_card, tm_card


def transform(image, pts, w, h):
    """Flattens an image of a card into a top-down 200x300 perspective.
    Returns the flattened, re-sized, grayed image.
    See www.pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/"""

    s = np.sum(pts, axis=2)
    tl = pts[np.argmin(s)]
    br = pts[np.argmax(s)]

    diff = np.diff(pts, axis=-1)
    tr = pts[np.argmin(diff)]
    bl = pts[np.argmax(diff)]

    # Need to create an array listing points in order of
    # [top left, top right, bottom right, bottom left]
    # before doing the perspective transform

    if w <= 0.8 * h:  # If card is vertically oriented
        temp_rect = np.array([tl, tr, br, bl], dtype="float32")

    elif w >= 1.2 * h:  # If card is horizontally oriented
        temp_rect = np.array([bl, tl, tr, br], dtype="float32")

    # If the card is 'diamond' oriented, a different algorithm
    # has to be used to identify which point is top left, top right
    # bottom left, and bottom right.

    else:  # If card is diamond oriented
        # If furthest left point is higher than furthest right point,
        # card is tilted to the left.
        temp_rect = np.zeros((4, 2), dtype="float32")
        if pts[1][0][1] <= pts[3][0][1]:
            # If card is titled to the left, approxPolyDP returns points
            # in this order: top right, top left, bottom left, bottom right
            temp_rect[0] = pts[1][0]  # Top left
            temp_rect[1] = pts[0][0]  # Top right
            temp_rect[2] = pts[3][0]  # Bottom right
            temp_rect[3] = pts[2][0]  # Bottom left

        # If furthest left point is lower than furthest right point,
        # card is tilted to the right
        else:
            # If card is titled to the right, approxPolyDP returns points
            # in this order: top left, bottom left, bottom right, top right
            temp_rect[0] = pts[0][0]  # Top left
            temp_rect[1] = pts[3][0]  # Top right
            temp_rect[2] = pts[2][0]  # Bottom right
            temp_rect[3] = pts[1][0]  # Bottom left

    maxWidth = 285  # = 5.7*50 ipv 200
    maxHeight = 435  # = 8.7*50 ipv 300

    # Create destination array, calculate perspective transform matrix,
    # and warp card image
    dst = np.array([[0, 0], [maxWidth - 1, 0], [maxWidth - 1, maxHeight - 1], [0, maxHeight - 1]], np.float32)
    M = cv2.getPerspectiveTransform(temp_rect, dst)
    warp = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    warp = cv2.cvtColor(warp, cv2.COLOR_BGR2GRAY)

    return warp


def find_match(img, moulds, diff_max):
    best_match_diff = 10000

    for i, mould in enumerate(moulds):
        diff_img = cv2.absdiff(img, mould)
        diff = int(np.sum(diff_img) / 255)

        if diff < best_match_diff:
            best_diff_img = diff_img
            cv2.imshow(f"Difference{len(moulds)}", best_diff_img)
            best_match_diff = diff
            best_value = i

    if best_match_diff < diff_max:
        return best_value  # best_match_diff

    return -1


def template_matching(template, kind, parts, ref_img):
    h, w = ref_img.shape
    h1, w1 = template.shape

    result = cv2.matchTemplate(ref_img, template, cv2.cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val < 0.5:
        return -1

    bottom_right = (max_loc[0] + w1, max_loc[1] + h1)
    center = (int(max_loc[0] + w1 / 2), int(max_loc[1] + h1 / 2))

    cv2.rectangle(ref_img, max_loc, bottom_right, (0, 0, 0), 2)

    ref_sized = cv2.resize(ref_img, (0, 0), fx=1, fy=1)

    cv2.imshow(kind, ref_sized)

    # Cut the reference image in parts
    w_part = w / parts

    for i in range(parts):
        # Find the part in which the center lies
        if i * w_part < center[0] < (i + 1) * w_part:
            return i


def display_cards(img, cards):
    size = 4
    for card in cards:
        x, y = card.center
        cv2.drawContours(img, [card.contour], -1, (255, 0, 0), 3)

        if card.rank == 14:
            cv2.putText(img, "Facedown", (x - 100, y - 20), FONT, size, (0, 0, 0), 5, cv2.LINE_AA)
            cv2.putText(img, "Facedown", (x - 100, y - 20), FONT, size, (255, 0, 0), 2, cv2.LINE_AA)

        elif card.rank == 13:
            cv2.putText(img, "Joker", (x - 90, y - 20), FONT, size + 1, (0, 0, 0), 5, cv2.LINE_AA)
            cv2.putText(img, "Joker", (x - 90, y - 20), FONT, size + 1, (255, 0, 0), 2, cv2.LINE_AA)

        elif card.rank == -1 or card.suit == -1:
            cv2.putText(img, "Unknown", (x - 140, y - 25), FONT, size, (0, 0, 0), 5, cv2.LINE_AA)
            cv2.putText(img, "Unknown", (x - 140, y - 25), FONT, size, (0, 0, 255), 2, cv2.LINE_AA)

            cv2.putText(img, "Card", (x - 75, y + 25), FONT, size, (0, 0, 0), 5, cv2.LINE_AA)
            cv2.putText(img, "Card", (x - 75, y + 25), FONT, size, (0, 0, 255), 2, cv2.LINE_AA)
        else:
            rank, suit = card.get_rank_suit()

            cv2.putText(img, rank + " of", (x - 100, y - 25), FONT, size, (0, 0, 0), 5, cv2.LINE_AA)
            cv2.putText(img, rank + " of", (x - 100, y - 25), FONT, size, (0, 255, 0), 2, cv2.LINE_AA)

            cv2.putText(img, suit, (x - 100, y + 25), FONT, size, (0, 0, 0), 5, cv2.LINE_AA)
            cv2.putText(img, suit, (x - 100, y + 25), FONT, size, (0, 255, 0), 2, cv2.LINE_AA)

    return img


def get_cards(img):
    thresh = binary_threshold(img)
    contours_pts = detect_cards(thresh)  # + detect_cards(np.invert(thresh))
    cards = [create_card(cnt, pts, img) for cnt, pts in contours_pts]
    m_cards = [i[0] for i in cards]
    tm_cards = [i[1] for i in cards]

    return m_cards, tm_cards


cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1440)  # 1920
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 810)  # 1080
prev_cards = []

while True:
    ret, img = cap.read()

    norm = np.zeros(img.shape)
    # img1 = cv2.normalize(img, norm, 0, 255, cv2.NORM_MINMAX)
    # img2 = cv2.normalize(img.copy(), norm, 0, 255, cv2.NORM_MINMAX)

    m_cards, tm_cards = get_cards(img)
    moulds = display_cards(img.copy(), m_cards)
    tm = display_cards(img.copy(), tm_cards)

    cv2.imshow('Colored', cv2.resize(cv2.hconcat([moulds, tm]), (0, 0), fx=0.5, fy=0.5))

    q = cv2.waitKey(1)
    if q == ord("q"):
        break

cv2.destroyAllWindows()
