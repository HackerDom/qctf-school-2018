import string

from svg_processing import SvgPathParser
from alphabet_utils import AlphabetParser, horizontally_space_letters
from cnc_generator import CncProgram


SVG_PATH_FILENAME = 'alphabet_svg_path.txt'

SVG_ALPHABET_ORDER = string.ascii_lowercase + string.ascii_uppercase + string.digits + '_-{}'
SVG_LETTER_SPACING_THRESHOLD = 20

FLAG = 'QCTF{Dont_you_love_cnc_milling}'
FLAG_KERNING = 4


def generate_cnc_program(text, alphabet):
    program = CncProgram()
    program.draw_contours(
        horizontally_space_letters(text, alphabet, FLAG_KERNING))
    program.finalize()
    return '\n'.join(program.instructions)


def read_alphabet(svg_path_filename):
    with open(svg_path_filename) as f:
        alphabet_svg_path = f.read()
    alphabet_contours = SvgPathParser.parse_contours(alphabet_svg_path)
    alphabet_parser = AlphabetParser(
        initial_alphabet_order=SVG_ALPHABET_ORDER,
        letter_spacing_threshold=SVG_LETTER_SPACING_THRESHOLD)
    alphabet = alphabet_parser.parse_alphabet(alphabet_contours)
    return alphabet


def main():
    alphabet = read_alphabet(SVG_PATH_FILENAME)
    print(generate_cnc_program(FLAG, alphabet))


if __name__ == '__main__':
    main()
