from OpenGL.GL import *
from OpenGL.GLUT import *
import math

def dezone(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y
    else:
        print("problem")
        return x, y

def zone_fnc(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if abs(dx) >= abs(dy) and (dx >= 0 and dy >= 0):
        zone = 0
        return x1, y1, x2, y2, zone
    elif abs(dy) > abs(dx) and (dx >= 0 and dy >= 0):
        zone = 1
        return y1, x1, y2, x2, zone
    elif abs(dy) > abs(dx) and (dx < 0 and dy >= 0):
        zone = 2
        return y1, -x1, y2, -x2, zone
    elif abs(dx) >= abs(dy) and (dx < 0 and dy >= 0):
        zone = 3
        return -x1, y1, -x2, y2, zone
    elif abs(dx) >= abs(dy) and (dx < 0 and dy < 0):
        zone = 4
        return -x1, -y1, -x2, -y2, zone
    elif abs(dy) > abs(dx) and (dx < 0 and dy < 0):
        zone = 5
        return -y1, -x1, -y2, -x2, zone
    elif abs(dy) > abs(dx) and (dx >= 0 and dy < 0):
        zone = 6
        return -y1, x1, -y2, x2, zone
    elif abs(dx) >= abs(dy) and (dx >= 0 and dy < 0):
        zone = 7
        return x1, -y1, x2, -y2, zone

def mid_line(x1, y1, x2, y2):
    lst = []
    zone = 0
    x1 , y1 , x2, y2, zone = zone_fnc(x1, y1, x2, y2)
    dx = x2 - x1
    dy = y2 - y1
    d = 2*dy - dx
    incE = 2*dy
    incNE = 2*(dy-dx)
    y = y1
    x = x1
    while (x <= x2):
        x_t , y_t = dezone(x , y , zone)
        lst.append((x_t, y_t))
        if (d > 0):
            y += 1
            d += incNE
        else:
            d += incE
        x += 1
    return lst

def draw_rectangle(x1, y1, x2, y2):
    points = []
    # Draw top side
    points.extend(mid_line(x1, y1, x2, y1))
    # Draw right side
    points.extend(mid_line(x2, y1, x2, y2))
    # Draw bottom side
    points.extend(mid_line(x2, y2, x1, y2))
    # Draw left side
    points.extend(mid_line(x1, y2, x1, y1))

    glBegin(GL_POINTS)
    for point in points:
        glVertex2f(point[0], point[1])
    glEnd()
    glFlush()



def draw_circle(center_x, center_y, radius):
    points = []
    x = 0
    y = radius
    d = 1 - radius

    while x <= y:
        points.extend(mid_line(center_x, center_y, center_x + x, center_y + y))
        points.extend(mid_line(center_x, center_y, center_x + y, center_y + x))
        points.extend(mid_line(center_x, center_y, center_x + y, center_y - x))
        points.extend(mid_line(center_x, center_y, center_x + x, center_y - y))
        points.extend(mid_line(center_x, center_y, center_x - x, center_y - y))
        points.extend(mid_line(center_x, center_y, center_x - y, center_y - x))
        points.extend(mid_line(center_x, center_y, center_x - y, center_y + x))
        points.extend(mid_line(center_x, center_y, center_x - x, center_y + y))

        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * (x - y) + 5
            y -= 1

        x += 1
        
    glBegin(GL_POINTS)
    for point in points:
        glVertex2f(point[0], point[1])
    glEnd()
    glFlush()



def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1.0, 1.0, 1.0)  # Set color (white in this case)
    draw_rectangle(10, 10, 100, 80)  # Example rectangle coordinates
    draw_circle(200, 150, 50)  # Example circle parameters
    glutSwapBuffers()

def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, -1.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(400, 300)  # Set your desired window size
    glutCreateWindow(b"Rectangle and Circle Drawing")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glClearColor(0.0, 0.0, 0.0, 0.0)  # Set background color to black
    glutMainLoop()

if __name__ == "__main__":
    main()
