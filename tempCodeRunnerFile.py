from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Spaceship positions
bottom_spaceship_x = 400
bottom_spaceship_y = 50
top_spaceship_x = 400
top_spaceship_y = 750

# Bullet properties
bullet_radius = 5
bullet_speed = 5
bullet_cooldown = 10
bottom_bullet_cooldown = 0
top_bullet_cooldown = 0

# Spaceship sizes
spaceship_width = 80
spaceship_height = 20
circle_radius = 20

# Bullet lists
bottom_bullets = []
top_bullets = []

def draw_pixel(x, y):
    glBegin(GL_POINTS)
    glVertex2i(x, y)
    glEnd()

def circlePoints(x, y, x0, y0):
    draw_pixel(x + x0, y + y0)
    draw_pixel(y + x0, x + y0)
    draw_pixel(y + x0, -x + y0)
    draw_pixel(x + x0, -y + y0)
    draw_pixel(-x + x0, -y + y0)
    draw_pixel(-y + x0, -x + y0)
    draw_pixel(-y + x0, x + y0)
    draw_pixel(-x + x0, y + y0)

def midpointCircle(radius, x0, y0):
    d = 1 - radius
    x = 0
    y = radius

    circlePoints(x, y, x0, y0)

    while x < y:
        if d < 0:
            d = d + 2*x + 3
            x += 1
        else:
            d = d + 2*x - 2*y + 5
            x += 1
            y = y - 1

        circlePoints(x, y, x0, y0)

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

def draw_spaceships():
    glColor3f(1.0, 1.0, 1.0)  # Set color to white

    # Draw bottom spaceship rectangle
    draw_rectangle(
        bottom_spaceship_x - spaceship_width // 2,
        bottom_spaceship_y,
        bottom_spaceship_x + spaceship_width // 2,
        bottom_spaceship_y + spaceship_height
    )

    # Draw top spaceship rectangle
    draw_rectangle(
        top_spaceship_x - spaceship_width // 2,
        top_spaceship_y - spaceship_height,
        top_spaceship_x + spaceship_width // 2,
        top_spaceship_y
    )

    # Draw bottom spaceship circle
    midpointCircle(circle_radius, bottom_spaceship_x, bottom_spaceship_y)

    # Draw top spaceship circle
    midpointCircle(circle_radius, top_spaceship_x, top_spaceship_y)

def draw_bullets():
    glColor3f(1.0, 1.0, 1.0)  # Set color to white

    # Draw bottom bullets
    for bullet in bottom_bullets:
        midpointCircle(bullet_radius, bullet[0], bullet[1])

    # Draw top bullets
    for bullet in top_bullets:
        midpointCircle(bullet_radius, bullet[0], bullet[1])

def update_bullets():
    global bottom_bullet_cooldown, top_bullet_cooldown

    # Update bottom bullets
    if bottom_bullet_cooldown > 0:
        bottom_bullet_cooldown -= 1

    # Update top bullets
    if top_bullet_cooldown > 0:
        top_bullet_cooldown -= 1

    # Move bottom bullets
    for i, bullet in enumerate(bottom_bullets):
        bottom_bullets[i] = (bullet[0], bullet[1] + bullet_speed)

    # Move top bullets
    for i, bullet in enumerate(top_bullets):
        top_bullets[i] = (bullet[0], bullet[1] - bullet_speed)

def keyboard(key, x, y):
    global bottom_spaceship_x, top_spaceship_x, bottom_bullet_cooldown, top_bullet_cooldown

    # Move the bottom spaceship with 'A' and 'D' keys
    if key == b'A' or key == b'a':
        bottom_spaceship_x = max(bottom_spaceship_x - 10, 0)
    elif key == b'D' or key == b'd':
        bottom_spaceship_x = min(bottom_spaceship_x + 10, 800 - spaceship_width)

    # Move the top spaceship with left and right arrow keys
    elif key == GLUT_KEY_LEFT:
        top_spaceship_x = max(top_spaceship_x - 10, 0)
    elif key == GLUT_KEY_RIGHT:
        top_spaceship_x = min(top_spaceship_x + 10, 800 - spaceship_width)

    # Fire bottom bullet with 'W' key
    elif key == b'W' or key == b'w':
        if bottom_bullet_cooldown == 0:
            bottom_bullets.append((bottom_spaceship_x, bottom_spaceship_y + spaceship_height + bullet_radius))
            bottom_bullet_cooldown = bullet_cooldown

    # Fire top bullet with up arrow key
    elif key == GLUT_KEY_UP:
        if top_bullet_cooldown == 0:
            top_bullets.append((top_spaceship_x, top_spaceship_y - spaceship_height - bullet_radius))
            top_bullet_cooldown = bullet_cooldown

    glutPostRedisplay()

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_spaceships()
    draw_bullets()
    glutSwapBuffers()

def reshape(w, h):
    glViewport(0, 0, GLsizei(w), GLsizei(h))
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0.0, GLdouble(w), 0.0, GLdouble(h))
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def update(frame):
    update_bullets()
    glutTimerFunc(16, update, 0)  # Update every 16 milliseconds (60 FPS)
    glutPostRedisplay()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)  # Use double buffering
    glutInitWindowSize(800, 800)
    glutCreateWindow(b"Spaceship Game")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(keyboard)  # Register special function keys
    glClearColor(0.0, 0.0, 0.0, 0.0)
    gluOrtho2D(0.0, 800.0, 0.0, 800.0)
    glutTimerFunc(16, update, 0)  # Initial call for the update function
    glutMainLoop()

if __name__ == "__main__":
    main()
