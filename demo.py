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

# Key states
key_states = {'a': False, 'd': False, 'left': False, 'right': False, 'w': False, 'up': False}

# Bullet cooldown
bottom_bullet_cooldown = 0
top_bullet_cooldown = 0

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

# Function to handle key press events
def keyboard(key, x, y):
    global key_states

    key = key.decode("utf-8")

    if key in key_states:
        key_states[key] = True

    glutPostRedisplay()

# Function to handle key release events
def keyboardUp(key, x, y):
    global key_states

    key = key.decode("utf-8")

    if key in key_states:
        key_states[key] = False

    glutPostRedisplay()

# Function to handle special key press events
def specialKeys(key, x, y):
    global key_states

    if key == GLUT_KEY_LEFT:
        key_states['left'] = True
    elif key == GLUT_KEY_RIGHT:
        key_states['right'] = True
    elif key == GLUT_KEY_UP:
        key_states['up'] = True

    glutPostRedisplay()

# Function to handle special key release events
def specialKeysUp(key, x, y):
    global key_states

    if key == GLUT_KEY_LEFT:
        key_states['left'] = False
    elif key == GLUT_KEY_RIGHT:
        key_states['right'] = False
    elif key == GLUT_KEY_UP:
        key_states['up'] = False

    glutPostRedisplay()

# Function to check collision between a bullet and a spaceship
def checkCollision(bulletX, bulletY, spaceshipX, spaceshipY):
    return (
        spaceshipX - 0.1 < bulletX < spaceshipX + 0.1 and
        spaceshipY - 0.1 < bulletY < spaceshipY + 0.1
    )

# Function to update game logic
def updateGameLogic(value):
    global bottom_bullets, top_bullets, bottom_spaceship_x, top_spaceship_x, bottom_bullet_cooldown, top_bullet_cooldown

    # Update bottom spaceship position
    if key_states['a']:
        bottom_spaceship_x = max(bottom_spaceship_x - spaceship_speed, -1.0)
    if key_states['d']:
        bottom_spaceship_x = min(bottom_spaceship_x + spaceship_speed, 1.0)

    # Update top spaceship position
    if key_states['left']:
        top_spaceship_x = max(top_spaceship_x - spaceship_speed, -1.0)
    if key_states['right']:
        top_spaceship_x = min(top_spaceship_x + spaceship_speed, 1.0)

    # Shoot bullet from bottom spaceship (W key)
    if key_states['w'] and bottom_bullet_cooldown <= 0:
        bottom_bullets.append([bottom_spaceship_x, -0.7])
        bottom_bullet_cooldown = 10  # Cooldown in frames

    # Shoot bullet from top spaceship (Up arrow key)
    if key_states['up'] and top_bullet_cooldown <= 0:
        top_bullets.append([top_spaceship_x, 0.7])
        top_bullet_cooldown = 10  # Cooldown in frames

    # Update bottom bullets
    for bullet in bottom_bullets:
        bullet[1] += 0.01

    # Update top bullets
    for bullet in top_bullets:
        bullet[1] -= 0.01

    # Check collisions
    for bullet in bottom_bullets:
        if checkCollision(bullet[0], bullet[1], top_spaceship_x, 0.9):
            print("Spaceship 2 hit!")
            bottom_bullets.remove(bullet)

    for bullet in top_bullets:
        if checkCollision(bullet[0], bullet[1], bottom_spaceship_x, -0.9):
            print("Spaceship 1 hit!")
            top_bullets.remove(bullet)

    # Reduce bullet cooldown
    if bottom_bullet_cooldown > 0:
        bottom_bullet_cooldown -= 1

    if top_bullet_cooldown > 0:
        top_bullet_cooldown -= 1

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
    glutKeyboardUpFunc(keyboardUp)
    glutSpecialFunc(specialKeys)
    glutSpecialUpFunc(specialKeysUp)
    glutTimerFunc(16, updateGameLogic, 0)

    glutMainLoop()

if __name__ == "__main__":
    main()
