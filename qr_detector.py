import math
import numpy as np
import cv2
import qr_detector_helper as helper

# Constants
SQUARE_TOLERANCE = 0.5
AREA_TOLERANCE = 0.1
DISTANCE_TOLERANCE = 0.5
WARP_DIM = 200
SMALL_DIM = 100

def is_square(contour, peri, area):
    return 1 - SQUARE_TOLERANCE < math.fabs((peri / 4) ** 2) / area < 1 + SQUARE_TOLERANCE

def find_squares(contours, hierarchy):
    squares = []
    square_indices = []
    for i, c in enumerate(contours):
        peri = cv2.arcLength(c, True)
        area = cv2.contourArea(c)
        approx = cv2.approxPolyDP(c, 0.03 * peri, True)
        if len(approx) == 4 and area > 25 and is_square(approx, peri, area) and helper.count_children(hierarchy[0], i) >= 2 and not helper.has_square_parent(hierarchy[0], square_indices, i):
            squares.append(approx)
            square_indices.append(i)
    return squares, square_indices

def detect_qr_corners(squares, helper):

    main_corners = []
    east_corners = []
    south_corners = []
    tiny_squares = []
    rectangles = []

    # Iterate over each square to find QR code corners
    for square in squares:
        area = cv2.contourArea(square)
        center = helper.get_center_of_contour(square)
        peri = cv2.arcLength(square, True)

        similar = []
        tiny = []
        for other in squares:
            if square[0][0][0] != other[0][0][0]:
                other_area = cv2.contourArea(other)
                other_peri = cv2.arcLength(other, True)
                # Check if other square is similar within AREA_TOLERANCE
                if abs(area - other_area) / max(area, other_area) <= AREA_TOLERANCE:
                    similar.append(other)
                # Check if other square is a tiny square
                elif peri / 4 / 2 > other_peri / 4:
                    tiny.append(other)

        # If enough similar squares are found, proceed to find corners
        if len(similar) >= 2:
            distances = []
            distances_to_contours = {}
            for sim in similar:
                sim_center = helper.get_center_of_contour(sim)
                d = math.hypot(sim_center[0] - center[0], sim_center[1] - center[1])
                distances.append(d)
                distances_to_contours[d] = sim
            distances.sort()
            closest_a = distances[-1]
            closest_b = distances[-2]

            # Determine if this square is the top left QR code indicator
            if max(closest_a, closest_b) < peri * 2.5 and abs(
                    closest_a - closest_b) / max(closest_a, closest_b) <= DISTANCE_TOLERANCE:
                # Determine placement of other indicators
                angle_a = helper.get_angle(helper.get_center_of_contour(distances_to_contours[closest_a]), center)
                angle_b = helper.get_angle(helper.get_center_of_contour(distances_to_contours[closest_b]), center)
                if angle_a < angle_b or (angle_b < -90 and angle_a > 0):
                    east = distances_to_contours[closest_a]
                    south = distances_to_contours[closest_b]
                else:
                    east = distances_to_contours[closest_b]
                    south = distances_to_contours[closest_a]
                midpoint = helper.get_midpoint(helper.get_center_of_contour(east),helper.get_center_of_contour(south))

                # Determine location of fourth corner
                diagonal = peri / 4 * math.sqrt(2)
                offset = helper.extend(midpoint, center, diagonal / 2)

                # Append rectangle, offsetting to farthest borders
                rectangles.append([
                    helper.extend(midpoint, center, diagonal / 2, True),
                    helper.extend(midpoint, helper.get_center_of_contour(distances_to_contours[closest_b]),
                                  diagonal / 2, True),
                    offset,
                    helper.extend(midpoint, helper.get_center_of_contour(distances_to_contours[closest_a]),
                                  diagonal / 2, True)
                ])
                east_corners.append(east)
                south_corners.append(south)
                main_corners.append(square)


    return main_corners, east_corners, south_corners, tiny_squares, rectangles


def warp_qr_codes(rectangles, img):
    codes = []
    i = 0
    for rect in rectangles:
        i += 1
        # Draw rectangle
        vrx = np.array((rect[0], rect[1], rect[2], rect[3]), np.int32)
        vrx = vrx.reshape((-1, 1, 2))
        # cv2.polylines(output, [vrx], True, (128, 255, 0), 2)
        # Warp codes and draw them
        wrect = np.zeros((4, 2), dtype="float32")
        wrect[0] = rect[0]
        wrect[1] = rect[1]
        wrect[2] = rect[2]
        wrect[3] = rect[3]
        dst = np.array([
            [0, 0],
            [WARP_DIM - 1, 0],
            [WARP_DIM - 1, WARP_DIM - 1],
            [0, WARP_DIM - 1]], dtype="float32")
        warp = cv2.warpPerspective(img, cv2.getPerspectiveTransform(wrect, dst), (WARP_DIM, WARP_DIM))
        # Increase contrast
        warp = cv2.bilateralFilter(warp, 11, 17, 17)
        warp = cv2.cvtColor(warp, cv2.COLOR_BGR2GRAY)
        small = cv2.resize(warp, (SMALL_DIM, SMALL_DIM), 0, 0, interpolation=cv2.INTER_CUBIC)
        _, small = cv2.threshold(small, 100, 255, cv2.THRESH_BINARY)
        codes.append(small)

    return codes

def draw_debug_info(output, squares, main_corners, east_corners, south_corners, tiny_squares):
    #cv2.drawContours(output, squares, -1, (0, 255, 255), 2) # yellow
    cv2.drawContours(output, main_corners, -1, (0, 0, 255), 3) # red
    #cv2.drawContours(output, east_corners, -1, (255, 0, 0), 2) # blue
    #cv2.drawContours(output, south_corners, -1, (255, 255, 0), 2) # green
    #cv2.drawContours(output, tiny_squares, -1, (255, 0, 255), 2) # magenta
    return output


def detect(img):
    output = img.copy()
    edged = cv2.Canny(img, 30, 200)
    contours, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    squares, square_indices = find_squares(contours, hierarchy)
    main_corners, east_corners, south_corners, tiny_squares, rectangles = detect_qr_corners(squares, helper)
    #codes = warp_qr_codes(rectangles, img)
    output = draw_debug_info(output, squares, main_corners, east_corners, south_corners, tiny_squares)

    return output




