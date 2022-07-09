from math import *

import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
import datetime

# initialization
window_width = 600
window_height = 600
# text
FONT_DOWNSCALE = 0.0018
# timer
INTERVAL = 1000  # discrete second-hand movement only like some real clocks
TOTAL_TIME = 0
HOUR = 0
MINUTE = 0
SECOND = 0

# setting time to its true value ...
time = datetime.datetime.now()
INIT_V = time.hour * 60 * 60 + time.minute * 60 + time.second
# print(INIT_V)


def init():  # useless here
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # default cube mapped from -1 tp 1
    glMatrixMode(GL_MODELVIEW)


def draw_axes():
    glLoadIdentity()

    glColor(1, 0, 0)  # red
    glBegin(GL_LINES)
    glVertex3d(1, 0, 0)
    glVertex3d(0, 0, 0)
    glEnd()

    glColor(0, 1, 0)  # green
    glBegin(GL_LINES)
    glVertex3d(0, 1, 0)
    glVertex3d(0, 0, 0)
    glEnd()


def draw_circle(r):
    glLoadIdentity()
    step = 0.1
    glBegin(GL_LINE_LOOP)
    for theta in np.arange(0, 360, step):
        x = r * cos(pi / 180 * theta)
        y = r * sin(pi / 180 * theta)
        glVertex3d(x, y, 0)
    glEnd()


def draw_hours_markers(r, step):
    glLoadIdentity()

    length = .08
    glLineWidth(3)
    glBegin(GL_LINES)

    for theta in np.arange(0, 360, step):
        x1 = r * cos(pi / 180 * theta)
        y1 = r * sin(pi / 180 * theta)
        x2 = x1 - length * x1
        y2 = y1 - length * y1

        glVertex3d(x1, y1, 0)
        glVertex3d(x2, y2, 0)
    glEnd()


def draw_minutes_markers(r, step):
    glLoadIdentity()
    glPointSize(4)
    glBegin(GL_POINTS)

    for theta in np.arange(0, 360, step):
        x = r * cos(pi / 180 * theta)
        y = r * sin(pi / 180 * theta)
        glVertex3d(x, y, 1)

    glEnd()


def draw_text(string, x, y):
    glLineWidth(2)
    glPushMatrix()
    glTranslate(x, y, 0)
    glScale(FONT_DOWNSCALE, FONT_DOWNSCALE, 1)
    string = string.encode()

    for c in string:
        glutStrokeCharacter(GLUT_STROKE_ROMAN, c)

    glPopMatrix()


def align_text(r):
    res = 30
    num = 2
    glScale(.8, .8, 1)  # by trial to adjust its place
    for theta in np.arange(0, 360, res):
        x1 = r * cos(pi / 180 * theta)
        y1 = r * sin(pi / 180 * theta)
        draw_text(str(num + 1), x1 - 0.072, y1 - 0.072)  # 0.072 by trail for adjustment too
        num -= 1
        num = ((num % 12) + 12) % 12  # for positive modulo ((x % divisor) + divisor) % divisor


def draw_hand(length, width):
    # bottom left
    x1 = -width / 2
    y1 = 0
    # top right
    x2 = width / 2
    y2 = length

    glBegin(GL_QUADS)
    glVertex3d(x1, y1, 0)
    glVertex3d(x1, y2, 0)
    glVertex3d(x2, y2, 0)
    glVertex3d(x2, y1, 0)
    glEnd()


def display():
    global HOUR, MINUTE, SECOND
    glClearColor(1, 1, 1, 1)
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    # draw_axes()

    glColor3ub(111, 78, 55)  # brown
    radius = 0.9
    # 1 - clock frame
    draw_circle(radius + 0.05)

    # 2 - minutes-markers
    draw_minutes_markers(r=radius, step=6)
    # 3 - hours-markers
    draw_hours_markers(r=radius, step=30)

    # 4 - numbers alignment
    align_text(radius)

    # 5 - hours hand with animation
    glPushMatrix()
    glRotate(HOUR * 30, 0, 0, -1)
    glTranslate(0, -0.1, 0)
    draw_hand(0.7, 0.04)  # hours
    glPopMatrix()

    # 6 - minutes hand with animation
    glPushMatrix()
    glRotate(MINUTE * 6, 0, 0, -1)
    glTranslate(0, -0.1, 0)
    draw_hand(.9, 0.015)  # minutes
    glPopMatrix()

    # 7 - seconds hand with animation
    glPushMatrix()
    glRotate(SECOND * 6, 0, 0, -1)
    glTranslate(0, -0.1, 0)
    draw_hand(1, 0.01)  # seconds
    glPopMatrix()

    # 8 - pin
    glPointSize(10)
    glColor(1, 1, 1, 1)
    draw_circle(0.005)

    glutSwapBuffers()


def timer(v):
    global TOTAL_TIME, HOUR, MINUTE, SECOND
    v %= 43200  # to avoid overflow (43 200 = 12 * 60 * 60 )

    TOTAL_TIME = v  # in sec
    TOTAL_TIME = TOTAL_TIME
    HOUR = TOTAL_TIME / (60 * 60)
    whole_hr = TOTAL_TIME // (60 * 60)

    rem = TOTAL_TIME - (whole_hr * 60 * 60)
    MINUTE = rem / 60
    whole_min = rem // 60

    rem = rem - (whole_min * 60)
    SECOND = rem

    display()

    print(str(whole_hr) + " : " + str(whole_min) + " : " + str(SECOND))
    glutTimerFunc(INTERVAL, timer, v + 1)


if __name__ == "__main__":
    print("hr  : min  : sec ")
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(window_width, window_height)
    glutCreateWindow("Clock")
    glutPositionWindow(0, 0)
    glutDisplayFunc(display)
    glutTimerFunc(INTERVAL, timer, INIT_V)  # curr time
    # glutSpecialFunc(keyboard_callback)
    init()
    glutMainLoop()