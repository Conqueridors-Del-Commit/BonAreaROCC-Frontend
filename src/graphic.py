import math

from OpenGL import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

WIDTH, HEIGHT = 800, 600


# Width es com de llarg al eix de les x, height la y, depth la z
# Color es una tripla r,g,b
def draw_prism(coordinates, size, color):
    x, y, z = coordinates
    width, height, depth = size
    r, g, b = color
    glColor3f(r, g, b)

    glNormal3f(0, 1, 0)
    glBegin(GL_QUADS)
    glVertex3i(x, y + height, z + depth)
    glVertex3i(x + width, y + height, z + depth)
    glVertex3i(x + width, y + height, z)
    glVertex3i(x, y + height, z)
    glEnd()

    # Quadrat 1
    glNormal3f(1, 0, 0)
    glBegin(GL_QUADS)
    glVertex3i(x + width, y + height, z)
    glVertex3i(x + width, y + height, z + depth)
    glVertex3i(x + width, y, z + depth)
    glVertex3i(x + width, y, z)
    glEnd()

    # Quadrat 5
    glNormal3f(0, 0, 1)
    glBegin(GL_QUADS)
    glVertex3i(x + width, y, z + depth)
    glVertex3i(x + width, y + height, z + depth)
    glVertex3i(x, y + height, z + depth)
    glVertex3i(x, y, z + depth)
    glEnd()

    # Quadrat 2
    glNormal3f(-1, 0, 0)
    glBegin(GL_QUADS)
    glVertex3i(x, y, z + depth)
    glVertex3i(x, y + height, z + depth)
    glVertex3i(x, y + height, z)
    glVertex3i(x, y, z)
    glEnd()

    # Quadrat 3
    glNormal3f(0, 0, -1)
    glBegin(GL_QUADS)
    glVertex3i(x, y, z)
    glVertex3i(x, y + height, z)
    glVertex3i(x + width, y + height, z)
    glVertex3i(x + width, y, z)
    glEnd()


def position_observer(alpha, beta, radi):
    PI = math.pi

    x = radi * math.cos(alpha * 2 * PI / 360.0) * math.cos(beta * 2 * PI / 360.0)
    y = radi * math.sin(beta * 2 * PI / 360.0)
    z = radi * math.sin(alpha * 2 * PI / 360.0) * math.cos(beta * 2 * PI / 360.0)

    if beta > 0:
        upx = -x
        upz = -z
        upy = (x * x + z * z) / y
    elif beta == 0:
        upx, upy, upz = 0, 1, 0
    else:
        upx = x
        upz = z
        upy = -(x * x + z * z) / y

    modul = math.sqrt(upx * upx + upy * upy + upz * upz)

    upx /= modul
    upy /= modul
    upz /= modul

    gluLookAt(500, 500, 500, 0, 0, 0, upx, upy, upz)


def square():
    glBegin(GL_QUADS)
    glNormal3f(0, -1, 0)
    glVertex3f(100, 100, 0)
    glNormal3f(0, -1, 0)
    glVertex3f(200, 100, 0)
    glNormal3f(0, -1, 0)
    glVertex3f(200, 200, 0)
    glNormal3f(0, -1, 0)
    glVertex3f(100, 200, 0)
    glEnd()


def create
def showScreen():
    glClearColor(0.15, 0.15, 0.15, 0.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    position_observer(45.0, 30.0, 450.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-WIDTH, WIDTH, -HEIGHT, HEIGHT, 0, 2000)

    glMatrixMode(GL_MODELVIEW)

    glPolygonMode(GL_FRONT, GL_FILL)
    glPolygonMode(GL_BACK, GL_LINE)

    graphics_procedure()

    glutSwapBuffers()


def graphics_procedure():
    # draw_prism((0, 0, 0), (100, 100, 100), (1.0, 0.0, 0.0))
    a


def init_graphics():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(WIDTH, HEIGHT)
    glutInitWindowPosition(0, 0)
    wind = glutCreateWindow("BonAreaROCC - Conquistadors Del Commit")
    glEnable(GL_DEPTH_TEST)
    glutDisplayFunc(showScreen)
    glutIdleFunc(showScreen)
    glutMainLoop()
