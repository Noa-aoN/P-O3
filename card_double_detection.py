import cv2

import numpy as np
from Camera import init_camera

from Deck import Card, SUITS, RANKS

FONT = cv2.FONT_HERSHEY_PLAIN

MAX_CARD_AREA = 500000000
MIN_CARD_AREA = 10000

RANK_WIDTH_HEIGHT = (70, 100)
SUIT_WIDTH_HEIGHT = (100, 100)

SUITS_IMG = [cv2.imread(f"Images/MyMoulds/{suit}.jpg", cv2.IMREAD_GRAYSCALE) for suit in SUITS]
RANKS_IMG = [cv2.imread(f"Images/MyMoulds/{rank}.jpg", cv2.IMREAD_GRAYSCALE) for rank in RANKS]

TEMPLATE_SUITS_IMG = cv2.imread("Images/References/ReferenceSuits.jpg", cv2.IMREAD_GRAYSCALE)
TEMPLATE_RANKS_IMG = cv2.imread("Images/References/ReferenceRanks.jpg", cv2.IMREAD_GRAYSCALE)


def binary_threshold(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)

    threshs = []

    for thresh_level in range(180, 130, -10):
        retval, thresh = cv2.threshold(blur, thresh_level, 255, cv2.THRESH_BINARY)
        threshs.append(thresh)

    return threshs


def detect_cards(thresh):
    card_cnts_pts = []
    cnts, hiers = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Card when: min < area < max, no parents, four corners

    for i, contour in enumerate(cnts):
        area = cv2.contourArea(contour)
        peri = cv2.arcLength(contour, True)
        pts = cv2.approxPolyDP(contour, 0.01 * peri, True)

        if MIN_CARD_AREA < area < MAX_CARD_AREA and hiers[0][i][3] == -1 and len(pts) == 4:
            card_cnts_pts.append((contour, pts))

    return card_cnts_pts


def create_card(contour, pts, image):
    average = np.sum(pts, axis=0) / len(pts)
    center = (int(average[0][0]), int(average[0][1]))

    # Warp card into 285x435 flattened image using perspective transform
    x, y, w, h = cv2.boundingRect(contour)
    warp = transform(image, pts, w, h)

    corner_zoom = warp[2:110, 2:45]

    for thresh_level in range(190, 130, -1):
        retval, corner_thresh = cv2.threshold(corner_zoom, thresh_level, 255, cv2.THRESH_BINARY)

        rank_img = corner_thresh[4:66, 0:50]
        suit_img = corner_thresh[62:110, 0:48]

        # Inverting!
        rank_cnts, hier = cv2.findContours(np.invert(rank_img), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        rank_cnts = sorted(rank_cnts, key=cv2.contourArea, reverse=True)
        rank_cnts = list(filter(lambda cnt: cv2.contourArea(cnt) > 350, rank_cnts))

        suit_cnts, hier = cv2.findContours(np.invert(suit_img), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        suit_cnts = sorted(suit_cnts, key=cv2.contourArea, reverse=True)

        if rank_cnts and suit_cnts:
            x1, y1, w1, h1 = cv2.boundingRect(rank_cnts[0])
            rank_img = rank_img[y1:y1 + h1, x1:x1 + w1]
            rank_img = cv2.resize(rank_img, RANK_WIDTH_HEIGHT, 0, 0)
            rank, r_perc = find_match(rank_img, RANKS_IMG)
            t_rank, t_r_perc = template_matching(rank_img, len(RANKS), TEMPLATE_RANKS_IMG)

            x1, y1, w1, h1 = cv2.boundingRect(suit_cnts[0])
            suit_img = suit_img[y1:y1 + h1, x1:x1 + w1]
            suit_img = cv2.resize(suit_img, SUIT_WIDTH_HEIGHT, 0, 0)
            suit, s_perc = find_match(suit_img, SUITS_IMG)
            t_suit, t_s_perc = template_matching(suit_img, len(SUITS), TEMPLATE_SUITS_IMG)

            if t_rank == rank and t_suit == suit:
                # print(r_perc * t_r_perc)
                # print(s_perc * t_s_perc)
                if r_perc * t_r_perc > 0.5 and s_perc * t_s_perc > 0.5:
                    card = Card(contour, pts, w, h, center, rank, suit)
                    card.match = ((r_perc * t_r_perc)**2 + (s_perc * t_s_perc)**2)**(1/2)
                    return card

    return Card(contour, pts, w, h, center, -1, -1)


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


def find_match(img, moulds):
    diff_imgs = [cv2.absdiff(img, mould) for mould in moulds]
    diff_perc = [1 - float(np.sum(diff_img) / (255 * 5000)) for diff_img in diff_imgs]

    max_perc = max(diff_perc)
    i = diff_perc.index(max_perc)

    return i, max_perc


def template_matching(template, parts, ref_img):
    h, w = ref_img.shape
    h1, w1 = template.shape

    result = cv2.matchTemplate(ref_img, template, cv2.cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    center = (int(max_loc[0] + w1 / 2), int(max_loc[1] + h1 / 2))

    # Cut the reference image in parts
    w_part = w / parts

    for i in range(parts):
        # Find the part in which the center lies
        if i * w_part < center[0] < (i + 1) * w_part:
            return i, max_val

    return -1, 0


def display_cards(img, cards, size=4):
    for card in cards:
        x, y = card.center
        cv2.drawContours(img, [card.contour], -1, (255, 0, 0), 3)

        if card.rank == 13:
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


def get_cards(img, amount):
    all_cards = []
    threshs = binary_threshold(img)
    for i, thresh in enumerate(threshs):
        contours_pts = detect_cards(thresh)
        print(len(contours_pts))
        if len(contours_pts) == amount:
            print("thresh", i)
            cards = [create_card(cnt, pts, img) for cnt, pts in contours_pts]
            if all(cards):
                all_cards.append(cards)

    if all_cards:
        arr = np.array(all_cards)
        best_cards = [max(card_list, key=lambda card: card.match) for card_list in arr.T]
        return best_cards
    else:
        return []


def get_card(img):
    if cards := get_cards(img, 1):
        return cards[0]
    return None


def card_double_detection():
    cap = init_camera()
    while True:

        ret, img = cap.read()

        img = cv2.imread("10_kaarten.jpg")
        """y, x, c = img.shape
    
        norm = np.zeros(img.shape)
        norm = cv2.normalize(img, norm, 0, 255, cv2.NORM_MINMAX)"""

        cards = get_cards(img, 10)
        img = display_cards(img, cards)

        cv2.imshow('Colored', cv2.resize(img, (0, 0), fx=0.4, fy=0.4))

        q = cv2.waitKey(1)
        if q == ord("q"):
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    card_double_detection()
