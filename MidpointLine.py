from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

def draw_pixel(x, y):
    glBegin(GL_POINTS)
    glVertex2i(x, y)
    glEnd()

def drawMidpointLine(x1, y1, x2, y2):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    while x1 != x2 or y1 != y2:
        draw_pixel(x1, y1)
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy
        draw_pixel(x1, y1)

def draw_rectangle(x1, y1, x2, y2):
    drawMidpointLine(x1, y1, x2, y1)
    drawMidpointLine(x2, y1, x2, y2)
    drawMidpointLine(x2, y2, x1, y2)
    drawMidpointLine(x1, y2, x1, y1)


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1.0, 1.0, 1.0)  # Set color to white

    # Generate random coordinates within a certain range
    x1 = random.randint(50, 550)
    y1 = random.randint(50, 550)
    size = 50  # Fixed size of the rectangle
    x2, y2 = x1 + size, y1 + size

    draw_rectangle(x1, y1, x2, y2)

    glutSwapBuffers()  # Use double buffering

def reshape(w, h):
    glViewport(0, 0, GLsizei(w), GLsizei(h))
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0.0, GLdouble(w), 0.0, GLdouble(h))
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)  # Use double buffering
    glutInitWindowSize(600, 600)
    glutCreateWindow(b"Random Rectangle Placement")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    gluOrtho2D(0.0, 600.0, 0.0, 600.0)
    glutMainLoop()

if __name__ == "__main__":
    main()
