import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

# Global variables to store spaceship positions
bottom_spaceship_x = -8
top_spaceship_x = 8
bottom_bullets = []  # List to store bottom spaceship's bullets
top_bullets = []  # List to store top spaceship's bullets
bullet_speed = 0.1

def draw_line(x1, y1, x2, y2, thickness):
    glLineWidth(thickness)
    glBegin(GL_LINES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glEnd()

thickness = 5
def draw_spaceship(x, y, scale):
    global thickness
    # Body
    draw_line(x - 2 * scale, y - 1 * scale, x + 2 * scale, y - 1 * scale, thickness)
    draw_line(x + 2 * scale, y - 1 * scale, x + 1.5 * scale, y + 1 * scale, thickness)
    draw_line(x + 1.5 * scale, y + 1 * scale, x - 1.5 * scale, y + 1 * scale, thickness)
    draw_line(x - 1.5 * scale, y + 1 * scale, x - 2 * scale, y - 1 * scale, thickness)

    # Wings
    draw_line(x - 1.5 * scale, y - 1 * scale, x - 2.5 * scale, y - 1 * scale, thickness)
    draw_line(x + 1.5 * scale, y - 1 * scale, x + 2.5 * scale, y - 1 * scale, thickness)

    # Cockpit
    draw_line(x - 0.5 * scale, y + 1 * scale, x + 0.5 * scale, y + 1 * scale, thickness)
    draw_line(x + 0.5 * scale, y + 1 * scale, x, y + 2 * scale, thickness)


def draw_filled_circle(x_centre, y_centre, r):
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(x_centre, y_centre)  # Center of the circle
    for i in range(361):  # 360 points on the circumference
        angle = math.radians(i)
        x = x_centre + r * math.cos(angle)
        y = y_centre + r * math.sin(angle)
        glVertex2f(x, y)
    glEnd()



bullet_radius = 0.2
def draw_bullet(x, y, radius):
    glColor3f(1.0, 1.0, 1.0)  # White color for the bullet
    draw_filled_circle(x, y, radius)

def check_collision(bullets, spaceship_x, spaceship_y, scale):
    for bullet in bullets:
        bullet_x, bullet_y = bullet[0], bullet[1]

        # Check if the bullet is within the boundaries of the spaceship
        if (
            bullet_x >= spaceship_x - 2 * scale
            and bullet_x <= spaceship_x + 2 * scale
            and bullet_y >= spaceship_y - 1 * scale
            and bullet_y <= spaceship_y + 2 * scale
        ):
            return True  # Collision detected

    return False  # No collision

def update_bullets(bullets, spaceship_x, spaceship_y, scale):
    global bullet_speed

    for bullet in bullets:
        bullet[1] += bullet_speed

    # Check for collisions with the bottom spaceship
    if check_collision(bullets, bottom_spaceship_x, -18, 0.5):
        print("Bottom spaceship hit!")

    # Check for collisions with the top spaceship
    if check_collision(bullets, top_spaceship_x, -8, 0.5):
        print("Top spaceship hit")



def draw_bottom_spaceship():
    glColor3f(1.0, 0.0, 0.0)  # Red color
    draw_spaceship(bottom_spaceship_x, -18, 0.5)

def draw_top_spaceship():
    glColor3f(0.0, 0.0, 1.0)  # Blue color
    glPushMatrix()
    glTranslatef(top_spaceship_x, 5, 0)
    glScalef(1, -1, 1)  # Mirror along the y-axis
    glTranslatef(-top_spaceship_x, -5, 0)
    draw_spaceship(top_spaceship_x, -8, 0.5)
    glPopMatrix()

def draw_bottom_spaceship_bullets():
    for bullet in bottom_bullets:
        draw_bullet(bullet[0], bullet[1], bullet_radius)
    

def draw_top_spaceship_bullets():
    glColor3f(0.0, 0.0, 1.0)  # Blue color

    # Draw the bullets and update their positions
    for bullet in top_bullets:
        # Mirror the y-coordinate to account for the mirroring of the spaceship
        mirrored_y = 2 * (5) - bullet[1]  # (y) should be opposite sign of the ships y
        draw_bullet(bullet[0], mirrored_y, bullet_radius)
    


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Draw bottom spaceship and bullets
    draw_bottom_spaceship()
    draw_bottom_spaceship_bullets()

    # Draw top spaceship and bullets (mirror version)
    draw_top_spaceship()
    draw_top_spaceship_bullets()

    update_bullets(bottom_bullets, bottom_spaceship_x, -18, 0.5)
    update_bullets(top_bullets, top_spaceship_x, -8, 0.5)

    glutSwapBuffers()


# ... (rest of the code remains unchanged)

def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-20, 20, -20, 20)
    glMatrixMode(GL_MODELVIEW)

def keyboard(key, x, y):
    global bottom_spaceship_x, top_spaceship_x, bottom_bullets, top_bullets

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

    # Shoot bullet from bottom spaceship (W key)
    elif key == b'W' or key == b'w':
        bottom_bullets.append([bottom_spaceship_x, -18])
        glutPostRedisplay()

    # Shoot bullet from top spaceship (Up arrow key)
    elif key == GLUT_KEY_UP:
        top_bullets.append([top_spaceship_x, -8])
        glutPostRedisplay()

    glutPostRedisplay()

def timer(value):
    glutPostRedisplay()
    glutTimerFunc(16, timer, 0)  # 60 FPS

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(800, 800)
    glutCreateWindow(b"Two Enhanced Spaceships")

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutTimerFunc(0, timer, 0)  # Call timer function immediately

    glEnable(GL_DEPTH_TEST)
    glClearColor(0.0, 0.0, 0.0, 1.0)

    glutKeyboardFunc(keyboard)
    glutSpecialFunc(keyboard)  # Register special key (arrow keys) callback

    glutMainLoop()

if __name__ == "__main__":
    main()
