PROGRAM_PREFIX = [
    '%',
    'O1000',
    'G90 G17 G40 G80 G54',
    'M06 T2',
    'G43 H2',
    'F300. S10000 M03']

PROGRAM_SUFFIX = [
    'G00 Z25.',
    'M05',
    'M30',
    '%']

DEPTHS = [z * (-0.5) for z in range(1, 13)]


class CncProgram:
    def __init__(self):
        self.instructions = list(PROGRAM_PREFIX)
        self._next_number = 100
        self._movement_mode = None
        self._x = None
        self._y = None

    @staticmethod
    def format_point(point):
        x, y = point
        return f'X{x:.5} Y{y:.5}'

    def emit(self, *instructions):
        for instruction in instructions:
            parts = instruction.split()
            stripped_parts = []

            command = parts[0]
            if command != self._movement_mode:
                stripped_parts.append(command)
                if command in ('G00', 'G01'):
                    self._movement_mode = command

            for part in parts[1:]:
                if part[0] == 'X':
                    x = part[1:]
                    if self._x == x:
                        continue
                    self._x = x
                elif part[0] == 'Y':
                    y = part[1:]
                    if self._y == y:
                        continue
                    self._y = y
                stripped_parts.append(part)

            if not stripped_parts:
                continue

            stripped_instruction = ' '.join(stripped_parts)
            self.instructions.append(f'N{self._next_number} {stripped_instruction}')
            self._next_number += 2

    def go_up(self):
        self.emit('Z2.')

    def go_down(self, depth):
        self.emit(f'G01 Z{depth} F300.')

    def rapid_move(self, point):
        coords = self.format_point(point)
        self.emit(f'G00 {coords}')

    def linear_interpolation(self, point):
        coords = self.format_point(point)
        self.emit(f'G01 {coords}')

    def draw_contour(self, contour):
        self.rapid_move(contour[0])
        for depth in DEPTHS:
            self.go_down(depth)
            for point in contour[1:] + [contour[0]]:
                self.linear_interpolation(point)
        self.go_up()

    def draw_contours(self, contours):
        for contour in contours:
            self.draw_contour(contour)

    def finalize(self):
        self.instructions.extend(PROGRAM_SUFFIX)
