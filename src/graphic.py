import math

from OpenGL import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import pygame
from pygame.locals import *

import numpy as np

from PIL import Image

import pyglet
from pyglet.gl import *

WIDTH, HEIGHT = 800, 600
SQUARE_SIZE = 20
XOFFSET = math.floor(47 * SQUARE_SIZE / 2) + 100
ZOFFSET = math.floor(20 * SQUARE_SIZE / 2) + 100


def darker_color(color):
    r, g, b = color
    glColor3f(max(0.0, r - 0.2), max(0.0, g - 0.2), max(0.0, b - 0.2))


# Width es com de llarg al eix de les x, height la y, depth la z
# Color es una tripla r,g,b
def draw_prism(coordinates, size, color):
    x, y, z = coordinates
    width, height, depth = size
    r, g, b = color
    glColor3f(r, g, b)

    glNormal3f(0, 1, 0)
    glBegin(GL_QUADS)
    glVertex3i(x - XOFFSET, y + height, z + depth - ZOFFSET)
    glVertex3i(x + width - XOFFSET, y + height, z + depth - ZOFFSET)
    glVertex3i(x + width - XOFFSET, y + height, z - ZOFFSET)
    glVertex3i(x - XOFFSET, y + height, z - ZOFFSET)
    glEnd()

    # Quadrat 1
    glBegin(GL_QUADS)
    glColor3f(r, g, b)
    glVertex3i(x + width - XOFFSET, y + height, z - ZOFFSET)
    glVertex3i(x + width - XOFFSET, y + height, z + depth - ZOFFSET)
    darker_color(color)
    glVertex3i(x + width - XOFFSET, y, z + depth - ZOFFSET)
    glVertex3i(x + width - XOFFSET, y, z - ZOFFSET)
    glColor3f(r, g, b)
    glEnd()

    # Quadrat 5
    glNormal3f(0, 0, 1)
    glBegin(GL_QUADS)
    darker_color(color)
    glVertex3i(x + width - XOFFSET, y, z + depth - ZOFFSET)
    glColor3f(r, g, b)
    glVertex3i(x + width - XOFFSET, y + height, z + depth - ZOFFSET)
    glVertex3i(x - XOFFSET, y + height, z + depth - ZOFFSET)
    darker_color(color)
    glVertex3i(x - XOFFSET, y, z + depth - ZOFFSET)
    glColor3f(r, g, b)
    glEnd()

    # Quadrat 2
    glNormal3f(-1, 0, 0)
    glBegin(GL_QUADS)
    darker_color(color)
    glVertex3i(x - XOFFSET, y, z + depth - ZOFFSET)
    glColor3f(r, g, b)
    glVertex3i(x - XOFFSET, y + height, z + depth - ZOFFSET)
    glVertex3i(x - XOFFSET, y + height, z - ZOFFSET)
    darker_color(color)
    glVertex3i(x - XOFFSET, y, z - ZOFFSET)
    glColor3f(r, g, b)
    glEnd()

    # Quadrat 3
    glNormal3f(0, 0, -1)
    glBegin(GL_QUADS)
    darker_color(color)
    glVertex3i(x - XOFFSET, y, z - ZOFFSET)
    glColor3f(r, g, b)
    glVertex3i(x - XOFFSET, y + height, z - ZOFFSET)
    glVertex3i(x - XOFFSET + width, y + height, z - ZOFFSET)
    darker_color(color)
    glVertex3i(x - XOFFSET + width, y, z - ZOFFSET)
    glColor3f(r, g, b)
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

    gluLookAt(x, y, z, 0, 0, 0, upx, upy, upz)


def draw_rectangle(coordinates, size, color):
    x, y, z = coordinates
    width, height, depth = size
    r, g, b = color
    glColor3f(r, g, b)
    glBegin(GL_QUADS)

    glNormal3f(0, -1, 0)
    glVertex3i(x - XOFFSET, 0, z - ZOFFSET)
    glNormal3f(0, -1, 0)
    glVertex3i(x - XOFFSET, 0, z + depth - ZOFFSET)
    glNormal3f(0, -1, 0)
    glVertex3i(x + width - XOFFSET, 0, z + depth - ZOFFSET)
    glNormal3f(0, -1, 0)
    glVertex3i(x + width - XOFFSET, 0, z - ZOFFSET)

    glEnd()


def load_texture(filename):
    img = Image.open(filename)
    img_data = np.array(list(img.getdata()), np.uint8)
    texture_id = glGenTextures(1, img_data)

    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.width, img.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)

    return texture_id


def draw_text(text, position, bold=False):
    font = pygame.font.SysFont("Arial", 16, bold)
    text_surface = font.render(text, True, (255, 255, 255), (140, 208, 252))
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    glRasterPos2d(*position)
    glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)


def draw_semaphore(position, color, bold=False):
    font = pygame.font.SysFont("Arial", 16, bold)
    text_surface = font.render("     ", True, color, color)
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    glRasterPos2d(*position)
    glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)


def draw_table_text(text, position, bold=False):
    font = pygame.font.SysFont("Arial", 16, bold)
    text_surface = font.render(text, True, (0, 0, 0), (255, 255, 255))
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    glRasterPos2d(*position)
    glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)


def draw_rectangle_2d(sizex, sizey, position):
    glColor3f(1.0, 1.0, 1.0)  # Set color to white
    glBegin(GL_QUADS)
    glVertex2f(position[0], position[1])  # Top-left corner
    glVertex2f(position[0], position[1] - sizey)  # Bottom-left corner
    glVertex2f(position[0] + sizex, position[1] - sizey)  # Bottom-right corner
    glVertex2f(position[0] + sizex, position[1])  # Top-right corner
    glEnd()


def draw_rectangle_test(width, height, position):
    surface = pygame.Surface((800, 600))
    pygame.draw.rect(surface, (0, 0, 0), (position[0], position[1], width, height))
    text_data = pygame.image.tostring(surface, "RGBA", True)
    glRasterPos2d(*position)
    glDrawPixels(surface.get_width(), surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)


def draw_header(text, position, bold=False):
    font = pygame.font.SysFont("Arial", 16, bold)
    text_surface = font.render(text, True, (255, 255, 255), (51, 51, 51))
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    glRasterPos2d(*position)
    glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)


def init_graphics():
    glutInit()
    pygame.init()
    pygame.font.init()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(WIDTH, HEIGHT)
    glutInitWindowPosition(0, 0)
    wind = glutCreateWindow("BonAreaROCC - Conquistadors Del Commit")
    glEnable(GL_DEPTH_TEST)
