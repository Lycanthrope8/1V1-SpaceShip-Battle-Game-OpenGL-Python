from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Window size
window_width = 800
window_height = 800

# Spaceship properties
bottom_spaceship_x = 0.0
top_spaceship_x = 0.0
spaceship_speed = 0.01

# Bullet properties
bottom_bullets = []
top_bullets = []

# Function to draw a spaceship
def drawSpaceship(x, y):
    glBegin(GL_QUADS)
    glVertex2f(x - 0.1, y - 0.1)
    glVertex2f(x + 0.1, y - 0.1)
    glVertex2f(x + 0.1, y + 0.1)
    glVertex2f(x - 0.1, y + 0.1)
    glEnd()

# Function to draw a bullet
def drawBullet(x, y):
    glBegin(GL_QUADS)
    glVertex2f(x - 0.02, y - 0.02)
    glVertex2f(x + 0.02, y - 0.02)
    glVertex2f(x + 0.02, y + 0.02)
    glVertex2f(x - 0.02, y + 0.02)
    glEnd()

# Function to handle keyboard input
def keyboard(key, x, y):
    global bottom_spaceship_x, top_spaceship_x, bottom_bullets, top_bullets

    # Move bottom spaceship left (A key)
    if key == b'A' or key == b'a':
        bottom_spaceship_x = max(bottom_spaceship_x - spaceship_speed, -1.0)

    # Move bottom spaceship right (D key)
    elif key == b'D' or key == b'd':
        bottom_spaceship_x = min(bottom_spaceship_x + spaceship_speed, 1.0)

    # Move top spaceship left (Left arrow key)
    elif key == GLUT_KEY_LEFT:
        top_spaceship_x = max(top_spaceship_x - spaceship_speed, -1.0)

    # Move top spaceship right (Right arrow key)
    elif key == GLUT_KEY_RIGHT:
        top_spaceship_x = min(top_spaceship_x + spaceship_speed, 1.0)

    # Shoot bullet from bottom spaceship (W key)
    elif key == b'W' or key == b'w':
        bottom_bullets.append([bottom_spaceship_x, -0.7])

    # Shoot bullet from top spaceship (Up arrow key)
    elif key == GLUT_KEY_UP:
        top_bullets.append([top_spaceship_x, 0.7])

    glutPostRedisplay()

# Function to check collision between a bullet and a spaceship
def checkCollision(bulletX, bulletY, spaceshipX, spaceshipY):
    return (
        spaceshipX - 0.1 < bulletX < spaceshipX + 0.1 and
        spaceshipY - 0.1 < bulletY < spaceshipY + 0.1
    )

# Function to update game logic
def updateGameLogic(value):
    global bottom_bullets, top_bullets, bottom_spaceship_x, top_spaceship_x

    # Update bottom bullets
    for bullet in bottom_bullets:
        bullet[1] += 0.01
        if checkCollision(bullet[0], bullet[1], top_spaceship_x, 0.9):
            print("Spaceship 2 hit!")
            bottom_bullets.remove(bullet)

    # Update top bullets
    for bullet in top_bullets:
        bullet[1] -= 0.01
        if checkCollision(bullet[0], bullet[1], bottom_spaceship_x, -0.9):
            print("Spaceship 1 hit!")
            top_bullets.remove(bullet)

    glutTimerFunc(16, updateGameLogic, 0)
    glutPostRedisplay()


# Function to draw the scene
def drawScene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glColor3f(1.0, 1.0, 1.0)
    drawSpaceship(bottom_spaceship_x, -0.9)

    glColor3f(0.0, 1.0, 0.0)
    for bullet in bottom_bullets:
        drawBullet(bullet[0], bullet[1])

    glColor3f(1.0, 1.0, 1.0)
    drawSpaceship(top_spaceship_x, 0.9)

    glColor3f(0.0, 0.0, 1.0)
    for bullet in top_bullets:
        drawBullet(bullet[0], bullet[1])

    glutSwapBuffers()

# Initialize OpenGL
def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-1.0, 1.0, -1.0, 1.0)

# Main function
def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(window_width, window_height)
    glutCreateWindow(b"Spaceship Shooter")

    init()

    glutDisplayFunc(drawScene)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(keyboard)
    glutTimerFunc(16, updateGameLogic, 0)

    glutMainLoop()

if __name__ == "__main__":
    main()
