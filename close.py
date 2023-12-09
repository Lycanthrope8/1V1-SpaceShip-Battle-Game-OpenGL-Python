from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

# Window size
window_width = 800
window_height = 800

# Spaceship properties
bottom_spaceship_x = 0.0
top_spaceship_x = 0.0
spaceship_speed = 0.01

# Health variables
bottom_spaceship_health = 100
top_spaceship_health = 100
match_result = None

# Bullet properties
bottom_bullets = []
top_bullets = []

# Key states
key_states = {'a': False, 'd': False, 'left': False, 'right': False, 'w': False, 'up': False}

# Bullet cooldown
bottom_bullet_cooldown = 0
top_bullet_cooldown = 0

# Box properties

box_respawn_time = 20  # Respawn time for the box in seconds
box_timer = 0

# Add these lines among your other global variables
box_position = None
box_size = 0.1  # Adjust the size of the box as needed
box_health_bonus = 20  # Health bonus when hitting the box
box_spawn_interval = 20000  # Box respawn interval in milliseconds (20 seconds)
box_timer = None  # Timer to track the box respawn time

# Function to draw a spaceship
def drawSpaceship(x, y, color1, color2, facing_up=True):
    direction = 1 if facing_up else -1
    scale_factor = 0.8  # Adjust the scale factor to make the spaceship smaller

    def drawLine(x0, y0, x1, y1):
        # Midpoint line algorithm
        dx = x1 - x0
        dy = y1 - y0
        d = dy - (dx / 2)
        x = x0
        y = y0

        # Plotting the line
        while x < x1:
            glVertex2f(x, y)
            x += 1
            if d < 0:
                d = d + dy
            else:
                d += (dy - dx)
                y += 1

    glColor3f(color1[0], color1[1], color1[2])
    glBegin(GL_POINTS)
    glColor3f(color1[0], color1[1], color1[2])
    glVertex2f(x - 0.04 * scale_factor, y - direction *
               0.08 * scale_factor)  # Point 1
    glColor3f(color1[0], color1[1], color1[2])
    glVertex2f(x + 0.04 * scale_factor, y - direction *
               0.08 * scale_factor)  # Point 2
    glColor3f(color2[0], color2[1], color2[2])
    glVertex2f(x + 0.04 * scale_factor, y + direction *
               0.08 * scale_factor)  # Point 3
    glColor3f(color2[0], color2[1], color2[2])
    glVertex2f(x - 0.04 * scale_factor, y + direction *
               0.08 * scale_factor)  # Point 4
    # Drawing spaceship parts using the drawLine function
    # Adjust coordinates according to your spaceship design
    drawLine(x - 0.04 * scale_factor, y - direction * 0.08 * scale_factor,
             x + 0.04 * scale_factor, y - direction * 0.08 * scale_factor)
    # Add other lines for spaceship body, cockpit, and wings

    glEnd()

    glColor3f(color2[0], color2[1], color2[2])
    glBegin(GL_POINTS)
    glVertex2f(x - 0.016 * scale_factor, y + direction *
               0.08 * scale_factor)  # Top vertex
    glVertex2f(x + 0.016 * scale_factor, y + direction *
               0.08 * scale_factor)  # Top-right vertex
    glVertex2f(x, y + direction * 0.12 * scale_factor)  # Tip vertex
    # Drawing cockpit using drawLine
    # Adjust coordinates as needed
    drawLine(x - 0.016 * scale_factor, y + direction * 0.08 * scale_factor,
             x + 0.016 * scale_factor, y + direction * 0.08 * scale_factor)
    # Add other lines for cockpit

    glEnd()

    # Left wing
    glBegin(GL_POINTS)
    glVertex2f(x - 0.04 * scale_factor, y - direction *
               0.04 * scale_factor)  # Bottom-left vertex
    glVertex2f(x - 0.08 * scale_factor, y - direction *
               0.08 * scale_factor)  # Top-left vertex
    glVertex2f(x - 0.04 * scale_factor, y + direction *
               0.04 * scale_factor)  # Top-right vertex
    glEnd()

    # Right wing
    glBegin(GL_POINTS)
    glVertex2f(x + 0.04 * scale_factor, y - direction *
               0.04 * scale_factor)  # Bottom-right vertex
    glVertex2f(x + 0.08 * scale_factor, y - direction *
               0.08 * scale_factor)  # Top-left vertex
    glVertex2f(x + 0.04 * scale_factor, y + direction *
               0.04 * scale_factor)  # Top-right vertex
    glEnd()


# Function to draw a bullet using midpoint circle algorithm with GL_POINTS
def drawBullet(x, y, radius):
    num_segments = 100
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()
    glBegin(GL_POINTS)
    for i in range(num_segments + 1):
        theta = i * (2.0 * math.pi / num_segments)
        bullet_x = x + radius * math.cos(theta)
        bullet_y = y + radius * math.sin(theta)
        glVertex2f(bullet_x, bullet_y)
    glEnd()

# Function to draw a box using midpoint line algorithm
def drawBox(x, y, size):
    # Calculate half size for convenience
    half_size = size / 2

    # Draw the box using lines
    glBegin(GL_LINES)
    glVertex2f(x - half_size, y - half_size)
    glVertex2f(x + half_size, y - half_size)

    glVertex2f(x + half_size, y - half_size)
    glVertex2f(x + half_size, y + half_size)

    glVertex2f(x + half_size, y + half_size)
    glVertex2f(x - half_size, y + half_size)

    glVertex2f(x - half_size, y + half_size)
    glVertex2f(x - half_size, y - half_size)
    glEnd()


# Function to draw a line using the midpoint line algorithm
def drawMidpointLine(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    x, y = x0, y0

    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1

    if abs(dy) > abs(dx):
        dx, dy = dy, dx
        xi, yi = 0, sx
    else:
        xi, yi = sy, 0

    d = 2 * abs(dy) - abs(dx)

    glBegin(GL_POINTS)
    glVertex2f(x, y)
    for _ in range(abs(dx)):
        if d >= 0:
            x, y = x + xi, y + yi
            d -= 2 * abs(dx)
        d += 2 * abs(dy)
        glVertex2f(x, y)
    glEnd()

# Function to draw the match result
def drawMatchResult(result_text):
    glColor3f(1.0, 1.0, 1.0)
    drawText(-0.08, 0.0, result_text)

# Function to draw text on the screen
def drawText(x, y, text):
    glRasterPos2f(x, y)
    for character in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ctypes.c_int(ord(character)))

# Pause state
is_game_paused = False

# Function to handle key press events
def keyboard(key, x, y):
    global key_states, is_game_paused

    key = key.decode("utf-8")

    if key == 'p':
        is_game_paused = not is_game_paused  # Toggle pause state
    elif key == '\x1b':  # Check for 'Escape' key
        glutLeaveMainLoop()  # Close the window
    elif key in key_states and not is_game_paused:
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
    global key_states, is_game_paused

    if key == GLUT_KEY_LEFT and not is_game_paused:
        key_states['left'] = True
    elif key == GLUT_KEY_RIGHT and not is_game_paused:
        key_states['right'] = True
    elif key == GLUT_KEY_UP and not is_game_paused:
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

# Add a function to check collision with the box
def checkCollisionWithBox(bulletX, bulletY):
    if box_position is not None:
        return (
            box_position[0] - box_size / 2 < bulletX < box_position[0] + box_size / 2 and
            box_position[1] - box_size / 2 < bulletY < box_position[1] + box_size / 2
        )
    return False

# Function to update game logic
def updateGameLogic(value):
    global bottom_bullets, top_bullets, bottom_spaceship_x, top_spaceship_x
    global bottom_bullet_cooldown, top_bullet_cooldown, bottom_spaceship_health, top_spaceship_health
    global is_game_paused, match_result, box_position, box_timer

    if not is_game_paused:
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
            bottom_bullets.append([bottom_spaceship_x, -0.8])
            bottom_bullet_cooldown = 10  # Cooldown in frames

        # Shoot bullet from top spaceship (Up arrow key)
        if key_states['up'] and top_bullet_cooldown <= 0:
            top_bullets.append([top_spaceship_x, 0.8])
            top_bullet_cooldown = 10  # Cooldown in frames

        # Update bottom bullets
        for bullet in bottom_bullets:
            bullet[1] += 0.01

        # Update top bullets
        for bullet in top_bullets:
            bullet[1] -= 0.01

        # Check if it's time to spawn or respawn the box
        if box_timer is None or glutGet(GLUT_ELAPSED_TIME) - box_timer > box_spawn_interval:
            # Spawn the box at a random position in the middle of the window
            box_position = [random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5)]
            box_timer = glutGet(GLUT_ELAPSED_TIME)  # Reset the timer for the next respawn

        # Check collisions with bullets for bottom spaceship
        for bullet in bottom_bullets:
            if checkCollision(bullet[0], bullet[1], top_spaceship_x, 0.9):
                bottom_bullets.remove(bullet)
                top_spaceship_health -= 2
            elif checkCollisionWithBox(bullet[0], bullet[1]):
                bottom_bullets.remove(bullet)
                bottom_spaceship_health += box_health_bonus
                box_position = None  # Box disappears after being hit
                box_timer = glutGet(GLUT_ELAPSED_TIME)  # Reset the timer

        for bullet in top_bullets:
            if checkCollision(bullet[0], bullet[1], bottom_spaceship_x, -0.9):
                top_bullets.remove(bullet)
                bottom_spaceship_health -= 2
            elif checkCollisionWithBox(bullet[0], bullet[1]):
                top_bullets.remove(bullet)
                top_spaceship_health += box_health_bonus
                box_position = None  # Box disappears after being hit
                box_timer = glutGet(GLUT_ELAPSED_TIME)  # Reset the timer

        # Check for the end of the game
        if bottom_spaceship_health <= 0:
            match_result = "Spaceship 2 Win!\nPress Esc to Escape the game"
        elif top_spaceship_health <= 0:
            match_result = "Spaceship 1 Win!\nPress Esc to Escape the game"

        # Reduce bullet cooldown
        if bottom_bullet_cooldown > 0:
            bottom_bullet_cooldown -= 1

        if top_bullet_cooldown > 0:
            top_bullet_cooldown -= 1
    # Respawn the box after the respawn time has passed
    if glutGet(GLUT_ELAPSED_TIME) - box_timer > box_respawn_time * 1000:
        box_position = [random.uniform(-0.8, 0.8), random.uniform(-0.8, 0.8)]
        box_timer = glutGet(GLUT_ELAPSED_TIME)  # Reset the timer

    glutTimerFunc(16, updateGameLogic, 0)
    glutPostRedisplay()

# Function to draw the scene
def drawScene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Display "Paused" text or match result in the middle of the window
    if is_game_paused:
        result_text = "Paused"
        drawMatchResult(result_text)
    elif match_result is not None:
        result_text = match_result
        drawMatchResult(result_text)
    else:
        # Spaceship 1 (Green and Yellow)
        drawSpaceship(bottom_spaceship_x, -0.9, [0.0, 1.0, 0.0], [1.0, 1.0, 0.0])

        # Bullets of Spaceship 1
        glColor3f(0.0, 1.0, 0.0)
        for bullet in bottom_bullets:
            drawBullet(bullet[0], bullet[1], 0.01)

        # Spaceship 2 (Blue and Cyan, facing downwards)
        drawSpaceship(top_spaceship_x, 0.9, [0.0, 0.0, 1.0], [0.0, 1.0, 1.0], facing_up=False)

        # Bullets of Spaceship 2
        glColor3f(0.0, 0.0, 1.0)
        for bullet in top_bullets:
            drawBullet(bullet[0], bullet[1], 0.01)

        # Draw health for Spaceship 1
        glColor3f(1.0, 1.0, 1.0)
        drawText(-0.8, -0.9, f"Health: {bottom_spaceship_health}")

        # Draw health for Spaceship 2
        glColor3f(1.0, 1.0, 1.0)
        drawText(-0.8, 0.8, f"Health: {top_spaceship_health}")

    if box_position is not None:
        drawBox(box_position[0], box_position[1], box_size)

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
