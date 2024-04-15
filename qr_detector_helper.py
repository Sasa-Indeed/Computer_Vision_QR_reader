import math
import numpy as np

# Quick note the contours list returned from cv2.findContours [next, previous, first_child, parent]

# A function that counts the number of child contours in a hierarchy of contours using BFS
# Purpose: Decide if a corner is one of the locators of the qr code or not by counting the contours
# Parameters: contours, parent, inner
# contours: A list of contours in hierarchical order
# parent: Index of the parent contour in the hierarchy
# Return value: An integer representing the number of child contours (squares) inside a parent contour (square)

def count_children(contours, parent):
    # Initialize a queue with the parent
    queue = [parent]
    contour_count = 0

    while queue:
        # Dequeue an element
        contour = queue.pop(0)

        # If the element is valid increment the count and enqueue its children
        if contour != -1:
            contour_count += 1
            queue.append(contours[contour][2])  # First child
            queue.append(contours[contour][0])  # Next sibling

    return contour_count



# A function that checks if a given contour has a square parent in a hierarchy of contours
# Purpose: Decide if a contour is part of one of the three locator squares by checking if it has a square parent
# Parameters: contours, squares, parent
# contours: A list of contours in hierarchical order
# squares: A list of contours that are squares
# parent: Index of the parent contour in the hierarchy
# Return value: A boolean value indicating whether the given contour has a square parent

def has_square_parent(contours, squares, parent):
    if contours[parent][3] == -1:
        return False
    if contours[parent][3] in squares:
        return True
    return has_square_parent(contours, squares, contours[parent][3])



# A function that calculates the center of a given contour
# Purpose: Determine the centroid of a contour which can be useful in determining the orientation of the QRcode
# Parameters: contour for which the center is to be calculated
# Return value: A list of two integers representing the x and y coordinates of the contour's center

def get_center_of_contour(contour):
    # Calculate the average x and y coordinates of all points in the contour
    center_x = int(np.mean(contour[:, :, 0]))
    center_y = int(np.mean(contour[:, :, 1]))

    return [center_x, center_y]



# A function that calculates the angle between the line connecting two points and the positive x-axis
# Purpose: Determine the orientation of a line or vector in 2D space
# Parameters: p1, p2
# p1, p2: Two 2D points represented as lists of two elements: [x, y]
# Return value: A floating-point number representing the angle in degrees

def get_angle(p1, p2):
    x_diff = p2[0] - p1[0]
    y_diff = p2[1] - p1[1]
    return math.degrees(math.atan2(y_diff, x_diff))



# A function that calculates the midpoint of the line segment connecting two points
# Purpose: Determine the center of a line segment in 2D space
# Parameters: p1, p2
# p1, p2: Two 2D points represented as lists of two elements: [x, y]
# Return value: A list of two elements representing the x and y coordinates of the midpoint

def get_midpoint(p1, p2):
    return [(p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2]



# A function that finds the two points in a contour that are farthest from a given center point
# Purpose: Identify key points in a contour based on their distance from the center
# Parameters: contour, center
# contour: A list of points representing the contour
# center: A 2D point represented as a list of two elements: [x, y]
# Return value: A list of two points representing the points in the contour that are farthest from the center

def get_farthest_points(contour, center):

    # Convert contour to a numpy array
    contour = np.squeeze(np.array(contour))

    # Calculate the distances from the center to each point in the contour
    distances = np.sqrt(np.sum((contour - center)**2, axis=1))

    # Get the indices of the two farthest points
    farthest_indices = np.argpartition(distances, -2)[-2:]

    return [contour[farthest_indices[0]].tolist(), contour[farthest_indices[1]].tolist()]



# A function that finds the intersection point of two lines
# Purpose: Determine the point at which two lines intersect in 2D space
# Parameters: line1, line2
# line1, line2: Two lines represented as lists of two 2D points: [[x1, y1], [x2, y2]]
# Return value: A list of two integers representing the x and y coordinates of the intersection point
# or [-1, -1] if the lines are parallel

def line_intersection(line1, line2):
    # Unpack the points
    (x1, y1), (x2, y2) = line1
    (x3, y3), (x4, y4) = line2

    # Calculate the slopes of the lines
    m1 = (y2 - y1) / (x2 - x1) if x2 != x1 else float('inf')
    m2 = (y4 - y3) / (x4 - x3) if x4 != x3 else float('inf')

    # If the slopes are equal then the lines are parallel
    if m1 == m2:
        return None

    # Calculate the y-intercepts of the lines
    b1 = y1 - m1 * x1
    b2 = y3 - m2 * x3

    # Calculate the x-coordinate of the intersection point
    denominator = m1 - m2
    if denominator == 0:
        return None

    x = (b2 - b1) / denominator

    # Calculate the y-coordinate of the intersection point
    y = m1 * x + b1

    return [int(round(x)), int(round(y))]



# A function that extends or shortens a line segment by a specified length from one of its endpoints
# Purpose: Estimate the position of the fourth corner of a QR code
# Parameters: a, b, length, int_represent
# a, b: Two 2D points represented as lists of two elements: [x, y], defining the line segment ab
# length: The length by which to extend (if positive) or shorten (if negative) the line segment
# int_represent: A boolean value indicating whether to round the coordinates of the new point to the nearest integer
# Return value: A list of two elements representing the x and y coordinates of the new point
# could be float or integer according to int_represent value

def extend(a, b, length, int_represent=False):
    length_ab = math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
    if length_ab * length <= 0:
        return b
    result = [b[0] + (b[0] - a[0]) / length_ab * length, b[1] + (b[1] - a[1]) / length_ab * length]
    if int_represent:
        return [int(result[0]), int(result[1])]
    else:
        return result
