import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Global variables to store spaceship positions
bottom_spaceship_x = -8
top_spaceship_x = 8

def draw_line(x1, y1, x2, y2):
    glBegin(GL_LINES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glEnd()

def draw_spaceship(x, y, scale):
    # Body
    draw_line(x - 2 * scale, y - 1 * scale, x + 2 * scale, y - 1 * scale)
    draw_line(x + 2 * scale, y - 1 * scale, x + 1.5 * scale, y + 1 * scale)
    draw_line(x + 1.5 * scale, y + 1 * scale, x - 1.5 * scale, y + 1 * scale)
    draw_line(x - 1.5 * scale, y + 1 * scale, x - 2 * scale, y - 1 * scale)

    # Wings
    draw_line(x - 1.5 * scale, y - 1 * scale, x - 2.5 * scale, y - 1 * scale)
    draw_line(x + 1.5 * scale, y - 1 * scale, x + 2.5 * scale, y - 1 * scale)

    # Cockpit
    draw_line(x - 0.5 * scale, y + 1 * scale, x + 0.5 * scale, y + 1 * scale)
    draw_line(x + 0.5 * scale, y + 1 * scale, x, y + 2 * scale)

def draw_bottom_spaceship():
    global bottom_spaceship_x
    draw_spaceship(bottom_spaceship_x, -5, 0.5)

def draw_top_spaceship():
    global top_spaceship_x
    draw_spaceship(top_spaceship_x, 5, 0.5)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Draw bottom spaceship
    glColor3f(1.0, 0.0, 0.0)  # Red color
    draw_bottom_spaceship()

    # Draw top spaceship (mirror version)
    glColor3f(0.0, 0.0, 1.0)  # Blue color
    glPushMatrix()
    glTranslatef(top_spaceship_x, 5, 0)
    glScalef(1, -1, 1)  # Mirror along the y-axis
    glTranslatef(-top_spaceship_x, -5, 0)
    draw_top_spaceship()
    glPopMatrix()

    glutSwapBuffers()

def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-20, 20, -20, 20)
    glMatrixMode(GL_MODELVIEW)

def keyboard(key, x, y):
    global bottom_spaceship_x, top_spaceship_x

    # Move bottom spaceship left (A key)
    if key == b'A' or key == b'a':
        bottom_spaceship_x = max(bottom_spaceship_x - 1, -19)

    # Move bottom spaceship right (D key)
    elif key == b'D' or key == b'd':
        bottom_spaceship_x = min(bottom_spaceship_x + 1, 19)

    # Move top spaceship left (Left arrow key)
    elif key == GLUT_KEY_LEFT:
        top_spaceship_x = max(top_spaceship_x - 1, -19)

    # Move top spaceship right (Right arrow key)
    elif key == GLUT_KEY_RIGHT:
        top_spaceship_x = min(top_spaceship_x + 1, 19)

    glutPostRedisplay()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(800, 800)
    glutCreateWindow(b"Two Enhanced Spaceships")

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutIdleFunc(display)

    glEnable(GL_DEPTH_TEST)
    glClearColor(0.0, 0.0, 0.0, 1.0)

    glutKeyboardFunc(keyboard)
    glutSpecialFunc(keyboard)  # Register special key (arrow keys) callback

    glutMainLoop()

if __name__ == "__main__":
    main()
