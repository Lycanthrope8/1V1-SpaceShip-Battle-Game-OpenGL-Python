import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

bottom_spaceship_x = -8
top_spaceship_x = 8
bottom_bullets = []
top_bullets = []
bullet_speed = 0.1

bottom_player_health = 100
top_player_health = 100

def draw_line(x1, y1, x2, y2, thickness):
    glLineWidth(thickness)
    glBegin(GL_LINES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glEnd()

thickness = 5

def draw_spaceship(x, y, scale):
    global thickness
    draw_line(x - 2 * scale, y - 1 * scale, x + 2 * scale, y - 1 * scale, thickness)
    draw_line(x + 2 * scale, y - 1 * scale, x + 1.5 * scale, y + 1 * scale, thickness)
    draw_line(x + 1.5 * scale, y + 1 * scale, x - 1.5 * scale, y + 1 * scale, thickness)
    draw_line(x - 1.5 * scale, y + 1 * scale, x - 2 * scale, y - 1 * scale, thickness)
    draw_line(x - 1.5 * scale, y - 1 * scale, x - 2.5 * scale, y - 1 * scale, thickness)
    draw_line(x + 1.5 * scale, y - 1 * scale, x + 2.5 * scale, y - 1 * scale, thickness)
    draw_line(x - 0.5 * scale, y + 1 * scale, x + 0.5 * scale, y + 1 * scale, thickness)
    draw_line(x + 0.5 * scale, y + 1 * scale, x, y + 2 * scale, thickness)

def draw_filled_circle(x_centre, y_centre, r):
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(x_centre, y_centre)
    for i in range(361):
        angle = math.radians(i)
        x = x_centre + r * math.cos(angle)
        y = y_centre + r * math.sin(angle)
        glVertex2f(x, y)
    glEnd()

bullet_radius = 0.2

def draw_bullet(x, y, radius):
    glColor3f(1.0, 1.0, 1.0)
    draw_filled_circle(x, y, radius)

def check_collision(bullet, spaceship_x, spaceship_width):
    bullet_x, bullet_y, is_bullet_bottom = bullet
    if spaceship_x - spaceship_width/2 <= bullet_x <= spaceship_x + spaceship_width/2:
        return True
    return False

def update_bullets(bullets, spaceship_x, spaceship_width, is_bottom_player):
    global bullet_speed, bottom_player_health, top_player_health

    new_bullets = []

    for bullet in bullets:
        bullet[1] += bullet_speed

        if check_collision(bullet, spaceship_x, spaceship_width):
            if is_bottom_player:
                top_player_health -= 5
                # Display health for both players after a collision
                print(f"Bottom Player Health: {bottom_player_health}")
                print(f"Top Player Health: {top_player_health}")
            else:
                bottom_player_health -= 5
                # Display health for both players after a collision
                print(f"Bottom Player Health: {bottom_player_health}")
                print(f"Top Player Health: {top_player_health}")
        else:
            new_bullets.append(bullet)

        # Remove bullets that are out of bounds
        if bullet[1] > 20 or bullet[1] < -20:
            pass

    return new_bullets

def draw_bottom_spaceship():
    glColor3f(1.0, 0.0, 0.0)
    draw_spaceship(bottom_spaceship_x, -18, 0.5)

def draw_top_spaceship():
    glColor3f(0.0, 0.0, 1.0)
    glPushMatrix()
    glTranslatef(top_spaceship_x, 5, 0)
    glScalef(1, -1, 1)
    glTranslatef(-top_spaceship_x, -5, 0)
    draw_spaceship(top_spaceship_x, -8, 0.5)
    glPopMatrix()

def draw_bottom_spaceship_bullets():
    for bullet in bottom_bullets:
        draw_bullet(bullet[0], bullet[1], bullet_radius)

def draw_top_spaceship_bullets():
    glColor3f(0.0, 0.0, 1.0)
    for bullet in top_bullets:
        mirrored_y = 2 * (5) - bullet[1]
        draw_bullet(bullet[0], mirrored_y, bullet_radius)

def display():
    global bottom_player_health, top_player_health, bottom_bullets, top_bullets

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    draw_bottom_spaceship()
    draw_bottom_spaceship_bullets()

    draw_top_spaceship()
    draw_top_spaceship_bullets()

    bottom_bullets = update_bullets(bottom_bullets, bottom_spaceship_x, 5.0, True)
    top_bullets = update_bullets(top_bullets, top_spaceship_x, 5.0, False)

    glutSwapBuffers()

def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-20, 20, -20, 20)
    glMatrixMode(GL_MODELVIEW)

def keyboard(key, x, y):
    global bottom_spaceship_x, top_spaceship_x, bottom_bullets, top_bullets

    if key == b'A' or key == b'a':
        bottom_spaceship_x = max(bottom_spaceship_x - 1, -19)
    elif key == b'D' or key == b'd':
        bottom_spaceship_x = min(bottom_spaceship_x + 1, 19)
    elif key == GLUT_KEY_LEFT:
        top_spaceship_x = max(top_spaceship_x - 1, -19)
    elif key == GLUT_KEY_RIGHT:
        top_spaceship_x = min(top_spaceship_x + 1, 19)
    elif key == b'W' or key == b'w':
        bottom_bullets.append([bottom_spaceship_x, -18, True])
        glutPostRedisplay()
    elif key == GLUT_KEY_UP:
        top_bullets.append([top_spaceship_x, -8, False])
        glutPostRedisplay()

    glutPostRedisplay()

def timer(value):
    glutPostRedisplay()
    glutTimerFunc(16, timer, 0)

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(800, 800)
    glutCreateWindow(b"Two Enhanced Spaceships")

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutTimerFunc(0, timer, 0)

    glEnable(GL_DEPTH_TEST)
    glClearColor(0.0, 0.0, 0.0, 1.0)

    glutKeyboardFunc(keyboard)
    glutSpecialFunc(keyboard)

    glutMainLoop()

if __name__ == "__main__":
    main()
