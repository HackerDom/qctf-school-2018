import string

from svg_processing import SvgPathParser
from alphabet_utils import AlphabetParser, horizontally_space_letters
from cnc_generator import CncProgram


SVG_PATH_FILENAME = 'alphabet_svg_path.txt'

SVG_ALPHABET_ORDER = string.ascii_lowercase + string.ascii_uppercase + '_-{}'
SVG_LETTER_SPACING_THRESHOLD = 20

FLAG = 'QCTF{Dont_you_love_cnc_milling}'
FLAG_KERNING = 4


def generate_cnc_program(text, alphabet):
    program = CncProgram()
    program.draw_contours(
        horizontally_space_letters(text, alphabet, FLAG_KERNING))
    program.finalize()
    return '\n'.join(program.instructions)


def main(alphabet_svg_path_file):
    alphabet_svg_path = alphabet_svg_path_file.read()
    alphabet_contours = SvgPathParser.parse_contours(alphabet_svg_path)
    alphabet_parser = AlphabetParser(
        initial_alphabet_order=SVG_ALPHABET_ORDER,
        letter_spacing_threshold=SVG_LETTER_SPACING_THRESHOLD)
    alphabet = alphabet_parser.parse_alphabet(alphabet_contours)
    print(generate_cnc_program(FLAG, alphabet))


if __name__ == '__main__':
    with open(SVG_PATH_FILENAME) as f:
        main(f)
