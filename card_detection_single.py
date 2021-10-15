import cv2

import urllib.request
import numpy as np


class Card:
    """Structure to store information about query cards in the camera image."""

    def __init__(self):
        self.contour = []  # Contour of card
        self.width, self.height = 0, 0  # Width and height of card
        self.corner_pts = []  # Corner points of card
        self.center = []  # Center point of card
        self.warp = []  # 400x600, flattened, grayed, blurred image
        self.rank = -1  # Rank
        self.suit = -1  # Suit
        self.rank_img = []  # Thresholded, sized image of card's rank
        self.suit_img = []  # Thresholded, sized image of card's suit


FONT = cv2.FONT_HERSHEY_PLAIN

CARD_MAX_AREA = 4000000
CARD_MIN_AREA = 10000

CORNER_WIDTH = 32
CORNER_HEIGHT = 84

URL = "http://192.168.1.102:8080/shot.jpg"

ICONS = ["Diamonds", "Clubs", "Hearts", "Spades"]

RANKS = cv2.imread("GetallenMoreSpace.png", 0)
SUITS = cv2.imread("SuitsLessTrimmed.png", 0)

# cap = cv2.VideoCapture(0)

def empty(_):
    pass


cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters", 600, 240)
cv2.createTrackbar("Contour", "Parameters", 120, 255, empty)
cv2.createTrackbar("x2", "Parameters", 45, 50, empty)
cv2.createTrackbar("y2", "Parameters", 110, 150, empty)
cv2.createTrackbar("tresh value", "Parameters", 140, 255, empty)




def find_match(template, kind):
    if template != [] and kind == "rank":
        ref_img = RANKS.copy()
        parts = 13
    elif template != [] and kind == "suit":
        ref_img = SUITS.copy()
        parts = 4
    else:
        return -1

    h0, w0 = template.shape
    h, w = ref_img.shape

    # scale to make a better fit
    template = cv2.resize(template, (0, 0), fx=h / h0, fy=h / h0)
    h1, w1 = template.shape

    result = cv2.matchTemplate(ref_img, template, cv2.cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    bottom_right = (max_loc[0] + w1, max_loc[1] + h1)
    center = (int(max_loc[0] + w1 / 2), int(max_loc[1] + h1 / 2))

    cv2.rectangle(ref_img, max_loc, bottom_right, (100, 100, 100), 2)
    cv2.circle(ref_img, center, 5, (100, 100, 100), 2)

    ref_sized = cv2.resize(ref_img, (0, 0), fx=0.3, fy=0.3)
    cv2.imshow(kind, ref_sized)

    # Cut the reference image in parts
    w_part = w / parts

    for i in range(1, parts + 1):
        # Find the part in which the center lies
        if (i - 1) * w_part < center[0] < i * w_part:
            return i


def preprocess_image(image):
    """Returns a grayed, blurred, and adaptively thresholded camera image."""

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)

    # img_w, img_h = np.shape(image)[:2]
    # bkg_level = gray[int(img_h / 100)][int(img_w / 2)]
    thresh_level = cv2.getTrackbarPos("Contour", "Parameters")  # + bkg_level

    retval, thresh = cv2.threshold(blur, thresh_level, 255, cv2.THRESH_BINARY)

    return thresh


def find_cards(pre_proc):
    """Finds all card-sized contours in a thresholded camera image.
    Returns the number of cards, and a list of card contours sorted
    from largest to smallest."""

    # Find contours and sort their indices by contour size
    cnts, hier = cv2.findContours(pre_proc, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    index_sort = sorted(range(len(cnts)), key=lambda i: cv2.contourArea(cnts[i]), reverse=True)
    # If there are no contours, do nothing
    if len(cnts) == 0:
        return [], []

    # Otherwise, initialize empty sorted contour and hierarchy lists
    cnts_sort = []
    hier_sort = []
    cnt_is_card = np.zeros(len(cnts), dtype=int)

    # Fill empty lists with sorted contour and sorted hierarchy. Now,
    # the indices of the contour list still correspond with those of
    # the hierarchy list. The hierarchy array can be used to check if
    # the contours have parents or not.
    for i in index_sort:
        cnts_sort.append(cnts[i])
        hier_sort.append(hier[0][i])

    # Determine which of the contours are cards by applying the
    # following criteria: 1) Smaller area than the maximum card size,
    # 2), bigger area than the minimum card size, 3) have no parents,
    # and 4) have four corners

    for i in range(len(cnts_sort)):
        size = cv2.contourArea(cnts_sort[i])
        peri = cv2.arcLength(cnts_sort[i], True)
        approx = cv2.approxPolyDP(cnts_sort[i], 0.01 * peri, True)  # Kan ook matchshape

        if CARD_MAX_AREA > size > CARD_MIN_AREA and hier_sort[i][3] == -1 and len(approx) == 4:
            cnt_is_card[i] = 1

    return cnts_sort, cnt_is_card


def flattener(image, pts, w, h):
    """Flattens an image of a card into a top-down 200x300 perspective.
    Returns the flattened, re-sized, grayed image.
    See www.pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/"""
    temp_rect = np.zeros((4, 2), dtype="float32")

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
        temp_rect[0] = tl
        temp_rect[1] = tr
        temp_rect[2] = br
        temp_rect[3] = bl

    if w >= 1.2 * h:  # If card is horizontally oriented
        temp_rect[0] = bl
        temp_rect[1] = tl
        temp_rect[2] = tr
        temp_rect[3] = br

    # If the card is 'diamond' oriented, a different algorithm
    # has to be used to identify which point is top left, top right
    # bottom left, and bottom right.

    if 0.8 * h < w < 1.2 * h:  # If card is diamond oriented
        # If furthest left point is higher than furthest right point,
        # card is tilted to the left.
        if pts[1][0][1] <= pts[3][0][1]:
            # If card is titled to the left, approxPolyDP returns points
            # in this order: top right, top left, bottom left, bottom right
            temp_rect[0] = pts[1][0]  # Top left
            temp_rect[1] = pts[0][0]  # Top right
            temp_rect[2] = pts[3][0]  # Bottom right
            temp_rect[3] = pts[2][0]  # Bottom left

        # If furthest left point is lower than furthest right point,
        # card is tilted to the right
        if pts[1][0][1] > pts[3][0][1]:
            # If card is titled to the right, approxPolyDP returns points
            # in this order: top left, bottom left, bottom right, top right
            temp_rect[0] = pts[0][0]  # Top left
            temp_rect[1] = pts[3][0]  # Top right
            temp_rect[2] = pts[2][0]  # Bottom right
            temp_rect[3] = pts[1][0]  # Bottom left

    maxWidth = 285  # 200
    maxHeight = 435  # 300

    # Create destination array, calculate perspective transform matrix,
    # and warp card image
    dst = np.array([[0, 0], [maxWidth - 1, 0], [maxWidth - 1, maxHeight - 1], [0, maxHeight - 1]], np.float32)
    M = cv2.getPerspectiveTransform(temp_rect, dst)
    warp = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    warp = cv2.cvtColor(warp, cv2.COLOR_BGR2GRAY)

    return warp


def preprocess_card(contour, image):
    """Uses contour to find information about the query card. Isolates rank
    and suit images from the card."""

    # Initialize new Query_card object
    qCard = Card()
    qCard.contour = contour

    # Find perimeter of card and use it to approximate corner points
    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.01 * peri, True)
    pts = np.float32(approx)
    qCard.corner_pts = pts

    # Find width and height of card's bounding rectangle
    x, y, w, h = cv2.boundingRect(contour)
    qCard.width, qCard.height = w, h

    # Find center point of card by taking x and y average of the four corners.
    average = np.sum(pts, axis=0) / len(pts)
    cent_x = int(average[0][0])
    cent_y = int(average[0][1])
    qCard.center = (cent_x, cent_y)

    # Warp card into 200x300 flattened image using perspective transform
    qCard.warp = flattener(image, pts, w, h)

    x2 = cv2.getTrackbarPos("x2", "Parameters")
    y2 = cv2.getTrackbarPos("y2", "Parameters")

    Qcorner_zoom = qCard.warp[2:y2, 2:x2]
    # qCard.value_img = Qcorner_zoom

    thresh_level = cv2.getTrackbarPos("tresh value", "Parameters")

    retval, query_thresh = cv2.threshold(Qcorner_zoom, thresh_level, 255, cv2.THRESH_BINARY)

    # Split in to top and bottom half (top shows rank, bottom shows suit)
    Qrank = query_thresh[5:66, 0:50]
    Qsuit = query_thresh[62:110, 0:48]

    # Find rank contour and bounding rectangle, isolate and find largest contour
    Qrank_cnts, hier = cv2.findContours(Qrank, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    Qrank_cnts = sorted(Qrank_cnts, key=cv2.contourArea, reverse=True)


    # Find bounding rectangle for largest contour, use it to resize query rank
    # image to match dimensions of the train rank image
    if len(Qrank_cnts) != 0:
        x1, y1, w1, h1 = cv2.boundingRect(Qrank_cnts[0])
        cv2.rectangle(Qrank, (x1, y1), (1 + w1, y1 + h1), (0, 255, 0), 2)
        Qrank_roi = Qrank[y1:y1 + h1, x1:x1 + w1]
        qCard.rank_img = Qrank_roi
        cv2.imshow(f"Rank ROI", Qrank_roi)

    cv2.imshow(f"Rank", Qrank)

    # Find suit contour and bounding rectangle, isolate and find largest contour
    Qsuit_cnts, hier = cv2.findContours(Qsuit, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    Qsuit_cnts = sorted(Qsuit_cnts, key=cv2.contourArea, reverse=True)
    cv2.imshow(f"Suit", Qsuit)

    # Find bounding rectangle for largest contour, use it to resize query suit
    # image to match dimensions of the train suit image
    if len(Qsuit_cnts) != 0:
        x2, y2, w2, h2 = cv2.boundingRect(Qsuit_cnts[0])
        Qsuit_roi = Qsuit[y2:y2 + h2, x2:x2 + w2]
        qCard.suit_img = Qsuit_roi


    return qCard




def draw_results(img, qCard):
    """Draw the card name, center point, and contour on the camera image."""

    x, y = qCard.center
    cv2.circle(img, (x, y), 5, (255, 0, 0), -1)

    rank = str(qCard.rank)
    suit = ICONS[qCard.suit - 1]

    cv2.putText(img, rank + ' of', (x - 60, y - 20), FONT, 5, (0, 0, 0), 5, cv2.LINE_AA)
    cv2.putText(img, rank + ' of', (x - 60, y - 20), FONT, 5, (50, 200, 200), 2, cv2.LINE_AA)

    cv2.putText(img, suit, (x - 60, y + 25), FONT, 5, (0, 0, 0), 5, cv2.LINE_AA)
    cv2.putText(img, suit, (x - 60, y + 25), FONT, 5, (50, 200, 200), 2, cv2.LINE_AA)

    return img


while True:
    img_arr = np.array(bytearray(urllib.request.urlopen(URL).read()), dtype=np.uint8)
    img = cv2.imdecode(img_arr, -1)

    pre_proc = preprocess_image(img)

    cnts_sort, cnt_is_card = find_cards(pre_proc)  # 1 lijst ipv 2 is sneller

    if len(cnts_sort) != 0:
        cards = []
        k = 0
        for i in range(len(cnts_sort)):
            if cnt_is_card[i] == 1:
                cards.append(preprocess_card(cnts_sort[i], img))

                rank = cards[k].rank_img
                suit = cards[k].suit_img

                cards[k].rank = find_match(rank, "rank")
                cards[k].suit = find_match(suit, "suit")

                if cards[k].rank != -1 and cards[k].suit != -1:
                    img = draw_results(img, cards[k])

                k += 1

            # Draw card contours on image (have to do contours all at once or
            # they do not show up properly for some reason)
        if len(cards) != 0:
            temp_cnts = []
            for i in range(len(cards)):
                temp_cnts.append(cards[i].contour)
            cv2.drawContours(img, temp_cnts, -1, (255, 0, 0), 3)

        resized2 = cv2.resize(img, (0, 0), fx=0.4, fy=0.4)
        cv2.imshow('Colored', resized2)
        q = cv2.waitKey(1)
        if q == ord("q"):
            break

cv2.destroyAllWindows()
