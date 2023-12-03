import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Global variables to store spaceship positions
bottom_spaceship_x = -8
top_spaceship_x = 8

def draw_spaceship(x, y, direction):
    glPushMatrix()
    glTranslatef(x, y, 0)
    glScalef(0.5, 0.5, 1)

    # Body
    glBegin(GL_POLYGON)
    glVertex2f(-5 * direction, -2.5)
    glVertex2f(-2.5 * direction, 2.5)
    glVertex2f(2.5 * direction, 2.5)
    glVertex2f(5 * direction, -2.5)
    glEnd()

    # Cockpit
    glBegin(GL_TRIANGLES)
    glVertex2f(-1 * direction, 2.5)
    glVertex2f(1 * direction, 2.5)
    glVertex2f(0, 5)
    glEnd()

    glPopMatrix()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Draw bottom spaceship
    glColor3f(1.0, 0.0, 0.0)  # Red color
    draw_spaceship(max(min(bottom_spaceship_x, 19), -19), -5, 1)

    # Draw top spaceship
    glColor3f(0.0, 0.0, 1.0)  # Blue color
    draw_spaceship(max(min(top_spaceship_x, 19), -19), 5, -1)

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
        bottom_spaceship_x -= 1

    # Move bottom spaceship right (D key)
    elif key == b'D' or key == b'd':
        bottom_spaceship_x += 1

    # Move top spaceship left (Left arrow key)
    elif key == GLUT_KEY_LEFT:
        top_spaceship_x -= 1

    # Move top spaceship right (Right arrow key)
    elif key == GLUT_KEY_RIGHT:
        top_spaceship_x += 1

    glutPostRedisplay()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(800, 800)
    glutCreateWindow(b"Two Spaceships Facing Each Other")

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
