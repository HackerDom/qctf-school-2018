def shift_point(point, dx, dy):
    return point[0] + dx, point[1] + dy


def shift_contour(contour, dx, dy):
    return [shift_point(point, dx, dy) for point in contour]


def shift_contours(contours, dx, dy):
    return [shift_contour(contour, dx, dy) for contour in contours]


def iterate_all_points(contours):
    for contour in contours:
        for point in contour:
            yield point


def horizontally_space_contoursets(contoursets, spacing):
    all_contours = []
    current_shift = 0
    for contours in contoursets:
        shifted_contours = shift_contours(contours, current_shift, 0)
        all_contours.extend(shifted_contours)
        max_x = max(point[0] for point in iterate_all_points(shifted_contours))
        current_shift = max_x + spacing
    return all_contours
