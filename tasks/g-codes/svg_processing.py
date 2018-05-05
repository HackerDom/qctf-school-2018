class SvgPathParser:
    @classmethod
    def parse_ooords(cls, coords):
        x, y = map(float, coords.split(','))
        return x, y

    @classmethod
    def parse_contours(cls, svg_path):
        tokens = list(reversed(svg_path.split()))
        contours = []
        contour = []
        position = None
        while tokens:
            command = tokens.pop()
            if command in 'zZ':
                if not contour:
                    raise ValueError('A Z command was issued but the current contour is empty')
                contour.append(contour[0])
            elif command in 'ML':
                if not tokens:
                    raise ValueError(f'The last {command} command doesn\'t have any arguments')
                coords = cls.parse_ooords(tokens.pop())

                if command == 'M':
                    position = coords
                    if contour:
                        contours.append(contour)
                        contour = []
                else:
                    if position is None:
                        raise ValueError('An L command was issued but the position has not been set')
                    if not contour:
                        contour.append(position)
                    position = coords
                    contour.append(position)
        if contour:
            contours.append(contour)
        return contours


class SvgPathGenerator:
    @staticmethod
    def serialize_coords(point):
        x, y = point
        return f'{x:.6},{y:.6}'

    @classmethod
    def move_to(cls, point):
        coords = cls.serialize_coords(point)
        return f'M {coords}'

    @classmethod
    def line_to(cls, point):
        coords = cls.serialize_coords(point)
        return f'L {coords}'

    @classmethod
    def draw_contour(cls, contour):
        return ' '.join(
            [cls.move_to(contour[0])] +
            list(map(cls.line_to, contour)) +
            ['z'])

    @classmethod
    def draw_contours(cls, contours):
        return '\n'.join((cls.draw_contour(contour) for contour in contours))
