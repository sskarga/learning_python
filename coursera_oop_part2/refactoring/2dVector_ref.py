"""
2d Vector
http://docs.godotengine.org/ru/latest/tutorials/math/vector_math.html
https://docs.unity3d.com/ru/current/Manual/UnderstandingVectorArithmetic.html
"""

import pygame
import random
import math


SCREEN_DIM = (800, 600)


class Vec2d:
    """
    Class 2d vector
    """
    def __init__(self, x, y):
        self._x = float(x)
        self._y = float(y)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, new_x):
        self._x = float(new_x)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, new_y):
        self._y = float(new_y)

    @property
    def list(self):
        return [self._x, self._y, ]

    def __repr__(self):
        return 'Vector ({}, {})'.format(self._x, self._y)   

    def __str__(self):
        return '({}, {})'.format(self._x, self._y)

    def __add__(self, other):
        types = (tuple, list)
        if isinstance(other, Vec2d):
            return Vec2d(self._x + other.x, self._y + other.y)
        elif isinstance(other, types):
            return Vec2d(self._x + other[0], self._y + other[1])
        else:
            return Vec2d(self._x + other, self._y + other)

    def __iadd__(self, other):
        types = (tuple, list)
        if isinstance(other, Vec2d):
            self._x += other.x
            self._y += other.y
        elif isinstance(other, types):
            self._x += other[0]
            self._y += other[1]
        else:
            self._x += other
            self._y += other
        return self

    def __sub__(self, other):
        types = (tuple, list)
        if isinstance(other, Vec2d):
            return Vec2d(self._x - other.x, self._y - other.y)
        elif isinstance(other, types):
            return Vec2d(self._x - other[0], self._y - other[1])
        else:
            return Vec2d(self._x - other, self._y - other)

    def __isub__(self, other):
        types = (tuple, list)
        if isinstance(other, Vec2d):
            self._x -= other.x
            self._y -= other.y
        elif isinstance(other, types):
            self._x -= other[0]
            self._y -= other[1]
        else:
            self._x -= other
            self._y -= other
        return self

    def __mul__(self, other):
        types = (tuple, list)
        if isinstance(other, Vec2d):
            return Vec2d(self._x * other.x, self._y * other.y)
        elif isinstance(other, types):
            return Vec2d(self._x * other[0], self._y * other[1])
        else:
            return Vec2d(self._x * other, self._y * other)

    def length(self):
        return math.sqrt(self._x * self._x + self._y * self._y)

    def __len__(self):
        return self.length()

    def __round__(self):
        return (int(self._x), int(self._y))

    def int_pair(self):
        return self.__round__()


class Polyline():
    """
    Class Polyline
    """
    _points = []
    _speeds = []

    def __init__(self, pgame):
        self._pgame = pgame
        self._surf = pygame.display.get_surface()
        self._screen_width = self._surf.get_width()
        self._screen_height = self._surf.get_height()

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, val):
        self._points = val

    @property
    def speeds(self):
        return self._speeds

    @speeds.setter
    def speeds(self, val):
        self._speeds = val

    def append(self, point, speed):
        self._points = self._points + [point]
        self._speeds = self._speeds + [speed]

    def extend(self, point, speed):
        self._points.extend(point)
        self._speeds.extend(speed)

    def set_points(self):
        for p in range(len(self._points)):

            self._points[p] += self._speeds[p]

            if self._points[p].x > self._screen_width or self._points[p].x < 0:
                self._speeds[p] = Vec2d(- self._speeds[p].x, self._speeds[p].y)

            if self._points[p].y > self._screen_height or self._points[p].y < 0:
                self._speeds[p] = Vec2d(self._speeds[p].x, - self._speeds[p].y)

    def draw_points(self, style="points", width=3, color=(255, 255, 255)):
        if style == "line":
            for p_n in range(-1, len(self._points) - 1):
                self._pgame.draw.line(
                    self._surf,
                    color,
                    round(self._points[p_n]),
                    round(self._points[p_n + 1]),
                    width
                )

        elif style == "points":
            for p in self._points:
                self._pgame.draw.circle(
                    self._surf,
                    color,
                    round(p),
                    width
                )


class Knot(Polyline):

    _knots = []
    
    @property
    def knots(self):
        return self._knots

    @knots.setter
    def knots(self, val):
        self._knots = val

    def clear(self):
        self._knots = []
        self._points = []
        self._speeds = []

    def _get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return (points[deg]*alpha) + (self._get_point(points, alpha, deg-1)*(1-alpha))

    def _get_points(self, base_points, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(self._get_point(base_points, i * alpha))
        return res

    def get_knot(self, count):
        if len(self._points) < 3:
            return []
        res = []
        for i in range(-2, len(self._points) - 2):
            ptn = []
            ptn.append((self._points[i] + self._points[i+1])*0.5)
            ptn.append(self._points[i+1])
            ptn.append((self._points[i+1] + self._points[i+2])*0.5)

            res.extend(self._get_points(ptn, count))

        self._knots = res
        return res

    def draw_knots(self, style="line", width=3, color=(255, 255, 255)):
        if style == "line":
            for p_n in range(-1, len(self._knots) - 1):
                self._pgame.draw.line(
                    self._surf,
                    color,
                    round(self._knots[p_n]),
                    round(self._knots[p_n + 1]),
                    width
                )

        elif style == "points":
            for p in self._knots:
                self._pgame.draw.circle(
                    self._surf,
                    color,
                    round(p),
                    width
                )


# Отрисовка справки
def draw_help():
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = []
    data.append(["F1", "Show Help"])
    data.append(["R", "Restart"])
    data.append(["P", "Pause/Play"])
    data.append(["Num+", "More points"])
    data.append(["Num-", "Less points"])
    data.append(["", ""])
    data.append([str(steps), "Current points"])

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
                      (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * i))


# Основная программа
if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    # New Class
    pline = Knot(pygame)

    steps = 35
    working = True
    show_help = False
    pause = True

    hue = 0
    color = pygame.Color(0)

    while working:
        for event in pygame.event.get():

            # Quit
            if event.type == pygame.QUIT:
                working = False

            # Key down    
            if event.type == pygame.KEYDOWN:

                # Exit
                if event.key == pygame.K_ESCAPE:
                    working = False

                # Reset
                if event.key == pygame.K_r:
                    pline.clear()

                # Pause
                if event.key == pygame.K_p:
                    pause = not pause

                # Inc point
                if event.key == pygame.K_KP_PLUS:
                    steps += 1

                # Dec point
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0

                # Help
                if event.key == pygame.K_F1:
                    show_help = not show_help
                
            # Add point
            if event.type == pygame.MOUSEBUTTONDOWN:
                pline.append(
                        Vec2d(event.pos[0], event.pos[1]),
                        Vec2d(random.random() * 2, random.random() * 2)
                    )
                pline.get_knot(steps)

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)

        pline.draw_points()
        pline.draw_knots(color=color)

        # Next step
        if not pause:
            pline.set_points()
            pline.get_knot(steps)
    
        # Help
        if show_help:
            draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
