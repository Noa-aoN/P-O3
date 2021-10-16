import cv2

import urllib.request
import numpy as np

FONT = cv2.FONT_HERSHEY_PLAIN

MAX_CARD_AREA = 4000000
MIN_CARD_AREA = 10000

URL = "http://192.168.1.102:8080/shot.jpg"

RANKS_IMG = cv2.imread("GetallenMoreSpace.png", 0)
SUITS_IMG = cv2.imread("SuitsLessTrimmed.png", 0)

SUITS = ["Diamonds", "Clubs", "Hearts", "Spades"]
RANKS = ["Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King"]


class Card:
    def __init__(self, contour, pts, w, h, center, rank_img, suit_img):
        self.contour = contour  # Contour of card
        self.corner_pts = pts # Corner points of card
        self.dimensions = (w, h)  # Width and height of card
        self.center = center  # Center point of card
        self.rank_img = rank_img  # Thresholded, sized image of card's rank
        self.suit_img = suit_img  # Thresholded, sized image of card's suit
        self.color = "Red"
        self.rank = -1  # Rank
        self.suit = -1  # Suit

    def get_rank_suit(self):
        suit = SUITS[self.suit - 1]
        rank = RANKS[self.rank - 1]
        return rank, suit


def empty(_):
    pass


cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters", 600, 120)
cv2.createTrackbar("Contour", "Parameters", 170, 255, empty)
cv2.createTrackbar("tresh value", "Parameters", 170, 255, empty)


def binary_threshold(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)

    # img_w, img_h = np.shape(image)[:2]
    # bkg_level = gray[int(img_h / 100)][int(img_w / 2)]
    thresh_level = cv2.getTrackbarPos("Contour", "Parameters")  # + bkg_level

    retval, thresh = cv2.threshold(blur, thresh_level, 255, cv2.THRESH_BINARY)

    return thresh


def detect_cards(thresh):
    card_cnts = []

    cnts, hiers = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Card when: min < area < max, no parents, four corners
    if len(cnts) != 0:
        for contour, hier in zip(cnts, hiers[0]):
            area = cv2.contourArea(contour)
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.01 * peri, True)

            if MIN_CARD_AREA < area < MAX_CARD_AREA and hier[3] == -1 and len(approx) == 4:
                pts = np.float32(approx)
                card_cnts.append((contour, pts))

    return card_cnts


def create_card(contour, pts, image):

    average = np.sum(pts, axis=0) / len(pts)
    center = (int(average[0][0]), int(average[0][1]))

    # Warp card into 285x435 flattened image using perspective transform
    x, y, w, h = cv2.boundingRect(contour)
    warp = transform(image, pts, w, h)

    corner_zoom = warp[2:110, 2:45]

    thresh_level = cv2.getTrackbarPos("tresh value", "Parameters")
    retval, corner_thresh = cv2.threshold(corner_zoom, thresh_level, 255, cv2.THRESH_BINARY)

    rank = corner_thresh[6:66, 0:50]
    suit = corner_thresh[62:110, 0:48]

    rank_cnts, hier = cv2.findContours(rank, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if len(rank_cnts) != 0:
        rank_cnts = sorted(rank_cnts, key=cv2.contourArea, reverse=True)
        x1, y1, w1, h1 = cv2.boundingRect(rank_cnts[0])
        rank_roi = rank[y1:y1 + h1, x1:x1 + w1]
    else:
        rank_roi = np.array([])

    cv2.imshow("Rank", rank)

    suit_cnts, hier = cv2.findContours(suit, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if len(suit_cnts) != 0:
        suit_cnts = sorted(suit_cnts, key=cv2.contourArea, reverse=True)
        x2, y2, w2, h2 = cv2.boundingRect(suit_cnts[0])
        suit_roi = suit[y2:y2 + h2, x2:x2 + w2]
    else:
        suit_roi = np.array([])

    cv2.imshow("Suit", suit)

    return Card(contour, pts, w, h, center, rank_roi, suit_roi)


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


def find_match(template, kind):
    if not np.array_equal(template, []) and kind == "rank":
        # Copy otherwise rect don't disappear
        ref_img = RANKS_IMG.copy()
        parts = 13
    elif not np.array_equal(template, []) and kind == "suit":
        # TODO implement color
        color = card.color
        ref_img = SUITS_IMG.copy()
        parts = 4
    else:
        return -1

    h0, w0 = template.shape
    h, w = ref_img.shape

    # scale to make a perfect fit
    template = cv2.resize(template, (0, 0), fx=h / h0, fy=h / h0)
    h1, w1 = template.shape

    result = cv2.matchTemplate(ref_img, template, cv2.cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val < 0.5:
        return -1

    bottom_right = (max_loc[0] + w1, max_loc[1] + h1)
    center = (int(max_loc[0] + w1 / 2), int(max_loc[1] + h1 / 2))

    cv2.rectangle(ref_img, max_loc, bottom_right, (0, 0, 0), 2)

    ref_sized = cv2.resize(ref_img, (0, 0), fx=0.3, fy=0.3)
    cv2.imshow(kind, ref_sized)

    # Cut the reference image in parts
    w_part = w / parts

    for i in range(1, parts + 1):
        # Find the part in which the center lies
        if (i - 1) * w_part < center[0] < i * w_part:
            return i


def display_text(img, card):
    size = 4
    x, y = card.center

    cv2.drawContours(img, [card.contour], -1, (255, 0, 0), 3)

    if card.rank == -1 or card.suit == -1:
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


while True:
    img_arr = np.array(bytearray(urllib.request.urlopen(URL).read()), dtype=np.uint8)
    img = cv2.imdecode(img_arr, -1)

    thresh = binary_threshold(img)
    contours_pts = detect_cards(thresh)
    cards = [create_card(cnt, pts, img) for cnt, pts in contours_pts]

    for card in cards:
        card.rank = find_match(card.rank_img, "rank")
        card.suit = find_match(card.suit_img, "suit")
        img = display_text(img, card)

    cv2.imshow('Thresh', cv2.resize(thresh, (0, 0), fx=0.4, fy=0.4))
    cv2.imshow('Colored', cv2.resize(img, (0, 0), fx=0.4, fy=0.4))

    q = cv2.waitKey(1)
    if q == ord("q"):
        break

cv2.destroyAllWindows()
