#!/usr/bin/python3

import sys

from PIL import Image, ImageDraw, ImageFont


FONT_NAME = 'DejaVuSansMono-Bold.ttf'
FONT_SIZE = 20

FONT = ImageFont.truetype(FONT_NAME, size=FONT_SIZE)


def _make_image(letter):
    offset = 2
    width, height = FONT.getsize(letter)
    img = Image.new('1', (width + offset * 2, height + offset * 2))
    
    draw = ImageDraw.Draw(img)
    draw.fontmode = '1'
    draw.text((offset, offset), letter, fill=255, font=FONT)
    
    return img


def _make_field(image):
    return [[
            image.getpixel((x, y)) // 255 \
            for x in range(image.width)
        ] for y in range(image.height)
    ]


def generate_field(letter):
    image = _make_image(letter)
    field = _make_field(image)

    return field


def print_field(field):
    for y in range(len(field)):
        print(''.join([' ' + (' ' if x else 'O') for x in field[y]]))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        print_field(generate_field(sys.argv[1]))
