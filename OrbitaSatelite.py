import sys
import math
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Inicializar variáveis globais
window_width = 800
window_height = 600
satellite_angle = 0.0
orbit_points = []
show_orbit = True

def init():
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.0, 0.0, 0.0, 1.0)

def calculate_orbit(radius, steps=360):
    """Calcula os pontos da órbita circular"""
    global orbit_points
    orbit_points = [
        (math.cos(math.radians(angle)) * radius, math.sin(math.radians(angle)) * radius)
        for angle in range(steps)
    ]

def draw_planet():
    """Desenha o planeta no centro."""
    glColor3f(0.0, 0.5, 1.0)
    glPushMatrix()
    glutSolidSphere(0.1, 50, 50)
    glPopMatrix()

def draw_satellite():
    """Desenha o satélite em órbita."""
    global satellite_angle

    # Calcular posição do satélite
    radius = 0.5
    x = math.cos(math.radians(satellite_angle)) * radius
    y = math.sin(math.radians(satellite_angle)) * radius

    glColor3f(1.0, 1.0, 0.0)
    glPushMatrix()
    glTranslatef(x, y, 0.0)
    glutSolidSphere(0.05, 30, 30)
    glPopMatrix()

def draw_orbit():
    """Desenha a linha da órbita se habilitada."""
    if not show_orbit:
        return

    glColor3f(0.5, 0.5, 0.5)
    glBegin(GL_LINE_LOOP)
    for x, y in orbit_points:
        glVertex3f(x, y, 0.0)
    glEnd()

def display():
    global satellite_angle

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Desenhar objetos
    draw_planet()
    draw_orbit()
    draw_satellite()

    glutSwapBuffers()

    # Atualizar ângulo do satélite para animação
    satellite_angle += 0.5
    if satellite_angle >= 360.0:
        satellite_angle -= 360.0

def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-1.0, 1.0, -1.0, 1.0)
    glMatrixMode(GL_MODELVIEW)

def keyboard(key, x, y):
    global show_orbit

    if key == b'l' or key == b'L':
        show_orbit = not show_orbit
    elif key == b'q' or key == b'Q':
        sys.exit()

    glutPostRedisplay()

def main():
    global orbit_points

    if not bool(glutInit):
        raise RuntimeError("A função glutInit não está disponível. Verifique sua instalação do FreeGLUT.")
    
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(window_width, window_height)
    glutCreateWindow(b"Satelite em Orbita")

    init()
    calculate_orbit(0.5)

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutIdleFunc(display)
    glutMainLoop()

if __name__ == "__main__":
    main()
