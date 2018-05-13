from collections import defaultdict

from contour_utils import iterate_all_points, shift_contours, horizontally_space_contoursets


class AlphabetParser:
    def __init__(self, initial_alphabet_order, letter_spacing_threshold):
        self._initial_alphabet_order = initial_alphabet_order
        self._letter_spacing_threshold = letter_spacing_threshold

    @staticmethod
    def normalize_letter(contours):
        min_x = min(point[0] for point in iterate_all_points(contours))
        return shift_contours(contours, -min_x, 0)

    def parse_alphabet(self, contours):
        contours_with_min_xs = [
            (min(point[0] for point in contour), contour)
            for contour in contours]
        contours_with_min_xs.sort()

        contours_by_letter = defaultdict(list)
        contour_index = 0
        letter_index = 0
        while letter_index < len(self._initial_alphabet_order) and contour_index < len(contours):
            letter = self._initial_alphabet_order[letter_index]
            min_x, contour = contours_with_min_xs[contour_index]
            if not contours_by_letter[letter]:
                contours_by_letter[letter].append(contour)
                contour_index += 1
                continue
            last_min_x, last_contour = contours_with_min_xs[contour_index - 1]
            if min_x - last_min_x > self._letter_spacing_threshold:
                letter_index += 1
                continue
            contours_by_letter[letter].append(contour)
            contour_index += 1

        return {
            letter: self.normalize_letter(contours)
            for letter, contours in contours_by_letter.items()}


def horizontally_space_letters(letters, alphabet, spacing):
    return horizontally_space_contoursets(
        (alphabet[letter] for letter in letters),
        spacing)
