from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random


window_width = 800
window_height = 800


bottom_spaceship_x = 0.0
top_spaceship_x = 0.0
spaceship_speed = 0.01


bottom_spaceship_health = 100
top_spaceship_health = 100
match_result = None

bottom_bullets = []
top_bullets = []


key_states = {'a': False, 'd': False, 'left': False, 'right': False, 'w': False, 'up': False}


bottom_bullet_cooldown = 0
top_bullet_cooldown = 0



box_respawn_time = 20  
box_timer = 0


box_position = None
box_size = 0.1 
box_health_bonus = 20  
box_spawn_interval = 20000  
box_timer = None  



def drawSpaceship(x, y, color1, color2, facing_up=True):
    direction = 1 if facing_up else -1
    scale_factor = 0.8  

    def drawLine(x0, y0, x1, y1):
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
    
    drawLine(x - 0.04 * scale_factor, y - direction * 0.08 * scale_factor,
             x + 0.04 * scale_factor, y - direction * 0.08 * scale_factor)
    

    glEnd()

    glColor3f(color2[0], color2[1], color2[2])
    glBegin(GL_POINTS)
    glVertex2f(x - 0.016 * scale_factor, y + direction *
               0.08 * scale_factor)  # Top vertex
    glVertex2f(x + 0.016 * scale_factor, y + direction *
               0.08 * scale_factor)  # Top-right vertex
    glVertex2f(x, y + direction * 0.12 * scale_factor)  # Tip vertex
    
    drawLine(x - 0.016 * scale_factor, y + direction * 0.08 * scale_factor,
             x + 0.016 * scale_factor, y + direction * 0.08 * scale_factor)
   

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
    # num_segments = 100
    # glBegin(GL_POINTS)
    # glVertex2f(x, y)
    # glEnd()
    # glBegin(GL_POINTS)
    # for i in range(num_segments + 1):
    #     theta = i * (2.0 * math.pi / num_segments)
    #     bullet_x = x + radius * math.cos(theta)
    #     bullet_y = y + radius * math.sin(theta)
    #     glVertex2f(bullet_x, bullet_y)
    num_segments = 100
    glBegin(GL_POINTS)

    
    circle_center = [x, y]
    x, y = radius, 0
    p = 1 - radius

    while x >= y:
        glVertex2f(x + circle_center[0], y + circle_center[1])
        glVertex2f(y + circle_center[0], x + circle_center[1])
        glVertex2f(-x + circle_center[0], y + circle_center[1])
        glVertex2f(-y + circle_center[0], x + circle_center[1])
        glVertex2f(-x + circle_center[0], -y + circle_center[1])
        glVertex2f(-y + circle_center[0], -x + circle_center[1])
        glVertex2f(x + circle_center[0], -y + circle_center[1])
        glVertex2f(y + circle_center[0], -x + circle_center[1])

        y += 1

        if p <= 0:
            p = p + 2 * y + 1
        else:
            x -= 1
            p = p + 2 * y - 2 * x + 1
    glEnd()


def drawBox(x, y, size):

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
    for _ in range(abs(int(dx))):
        if d >= 0:
            x, y = x + xi, y + yi
            d -= 2 * abs(dx)
        d += 2 * abs(dy)
        glVertex2f(x, y)
    glEnd()


def drawMatchResult(result_text):
    glColor3f(1.0, 1.0, 1.0)
    drawText(-0.08, 0.0, result_text)


def drawText(x, y, text):
    glRasterPos2f(x, y)
    for character in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ctypes.c_int(ord(character)))

is_game_paused = False


def keyboard(key, x, y):
    global key_states, is_game_paused

    key = key.decode("utf-8")

    if key == 'p':
        is_game_paused = not is_game_paused  
    elif key == '\x1b':  
        glutLeaveMainLoop() 
    elif key in key_states and not is_game_paused:
        key_states[key] = True

    glutPostRedisplay()


def keyboardUp(key, x, y):
    global key_states

    key = key.decode("utf-8")

    if key in key_states:
        key_states[key] = False

    glutPostRedisplay()


def specialKeys(key, x, y):
    global key_states, is_game_paused

    if key == GLUT_KEY_LEFT and not is_game_paused:
        key_states['left'] = True
    elif key == GLUT_KEY_RIGHT and not is_game_paused:
        key_states['right'] = True
    elif key == GLUT_KEY_UP and not is_game_paused:
        key_states['up'] = True

    glutPostRedisplay()


def specialKeysUp(key, x, y):
    global key_states

    if key == GLUT_KEY_LEFT:
        key_states['left'] = False
    elif key == GLUT_KEY_RIGHT:
        key_states['right'] = False
    elif key == GLUT_KEY_UP:
        key_states['up'] = False

    glutPostRedisplay()

def checkCollision(bulletX, bulletY, spaceshipX, spaceshipY):
    return (
        spaceshipX - 0.1 < bulletX < spaceshipX + 0.1 and
        spaceshipY - 0.1 < bulletY < spaceshipY + 0.1
    )


def checkCollisionWithBox(bulletX, bulletY):
    if box_position is not None:
        return (
            box_position[0] - box_size / 2 < bulletX < box_position[0] + box_size / 2 and
            box_position[1] - box_size / 2 < bulletY < box_position[1] + box_size / 2
        )
    return False

def updateGameLogic(value):
    global bottom_bullets, top_bullets, bottom_spaceship_x, top_spaceship_x
    global bottom_bullet_cooldown, top_bullet_cooldown, bottom_spaceship_health, top_spaceship_health
    global is_game_paused, match_result, box_position, box_timer

    if not is_game_paused:
        
        if key_states['a']:
            bottom_spaceship_x = max(bottom_spaceship_x - spaceship_speed, -1.0)
        if key_states['d']:
            bottom_spaceship_x = min(bottom_spaceship_x + spaceship_speed, 1.0)

        if key_states['left']:
            top_spaceship_x = max(top_spaceship_x - spaceship_speed, -1.0)
        if key_states['right']:
            top_spaceship_x = min(top_spaceship_x + spaceship_speed, 1.0)

        if key_states['w'] and bottom_bullet_cooldown <= 0:
            bottom_bullets.append([bottom_spaceship_x, -0.8])
            bottom_bullet_cooldown = 10  

        if key_states['up'] and top_bullet_cooldown <= 0:
            top_bullets.append([top_spaceship_x, 0.8])
            top_bullet_cooldown = 10  

        # Update bottom bullets
        for bullet in bottom_bullets:
            bullet[1] += 0.01

        # Update top bullets
        for bullet in top_bullets:
            bullet[1] -= 0.01

        # Check if it's time to spawn or respawn the box
        if box_timer is None or glutGet(GLUT_ELAPSED_TIME) - box_timer > box_spawn_interval:
            
            box_position = [random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5)]
            box_timer = glutGet(GLUT_ELAPSED_TIME)  

        # Check collisions with bullets for bottom spaceship
        for bullet in bottom_bullets:
            if checkCollision(bullet[0], bullet[1], top_spaceship_x, 0.9):
                bottom_bullets.remove(bullet)
                top_spaceship_health -= 2
            elif checkCollisionWithBox(bullet[0], bullet[1]):
                bottom_bullets.remove(bullet)
                bottom_spaceship_health += box_health_bonus
                box_position = None  
                box_timer = glutGet(GLUT_ELAPSED_TIME)  

        for bullet in top_bullets:
            if checkCollision(bullet[0], bullet[1], bottom_spaceship_x, -0.9):
                top_bullets.remove(bullet)
                bottom_spaceship_health -= 2
            elif checkCollisionWithBox(bullet[0], bullet[1]):
                top_bullets.remove(bullet)
                top_spaceship_health += box_health_bonus
                box_position = None 
                box_timer = glutGet(GLUT_ELAPSED_TIME)  

        
        if bottom_spaceship_health <= 0:
            match_result = "Spaceship 2 Win!\nPress Esc to Escape the game"
        elif top_spaceship_health <= 0:
            match_result = "Spaceship 1 Win!\nPress Esc to Escape the game"

        
        if bottom_bullet_cooldown > 0:
            bottom_bullet_cooldown -= 1

        if top_bullet_cooldown > 0:
            top_bullet_cooldown -= 1
    
    if glutGet(GLUT_ELAPSED_TIME) - box_timer > box_respawn_time * 1000:
        box_position = [random.uniform(-0.8, 0.8), random.uniform(-0.8, 0.8)]
        box_timer = glutGet(GLUT_ELAPSED_TIME)  

    glutTimerFunc(16, updateGameLogic, 0)
    glutPostRedisplay()

def drawScene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    
    if is_game_paused:
        result_text = "Paused"
        drawMatchResult(result_text)
    elif match_result is not None:
        result_text = match_result
        drawMatchResult(result_text)
    else:
        
        drawSpaceship(bottom_spaceship_x, -0.9, [0.0, 1.0, 0.0], [1.0, 1.0, 0.0])

        
        glColor3f(0.0, 1.0, 0.0)
        for bullet in bottom_bullets:
            drawBullet(bullet[0], bullet[1], 0.01)

        
        drawSpaceship(top_spaceship_x, 0.9, [0.0, 0.0, 1.0], [0.0, 1.0, 1.0], facing_up=False)

        
        glColor3f(0.0, 0.0, 1.0)
        for bullet in top_bullets:
            drawBullet(bullet[0], bullet[1], 0.01)

        
        glColor3f(1.0, 1.0, 1.0)
        drawText(-0.8, -0.9, f"Health: {bottom_spaceship_health}")

        
        glColor3f(1.0, 1.0, 1.0)
        drawText(-0.8, 0.8, f"Health: {top_spaceship_health}")

    if box_position is not None:
        drawBox(box_position[0], box_position[1], box_size)

    glutSwapBuffers()

def initialize():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, window_width, window_height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, window_width, 0.0, window_height, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(window_width, window_height)
    glutCreateWindow(b"Spaceship Shooter")
    initialize()
    glutDisplayFunc(drawScene)
    glutKeyboardFunc(keyboard)
    glutKeyboardUpFunc(keyboardUp)
    glutSpecialFunc(specialKeys)
    glutSpecialUpFunc(specialKeysUp)
    glutTimerFunc(16, updateGameLogic, 0)

    glutMainLoop()

if __name__ == "__main__":
    main()

