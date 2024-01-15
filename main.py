import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

vertices = [
    [0, 1, 0],
    [-1, 0, 1],
    [1, 0, 1],
    [0, 0, -1]
]

triangles = [
    [0, 1, 3],
    [0, 1, 2],
    [0, 2, 3],
    [1, 2, 3]
]
colors = (
    (1, 0, 0),
    (1, 1, 0),
    (1, 0, 1),
    (0, 0, 1),
    (0, 1, 1),
    (0, 1, 0)
)

def draw_piramid(vertices):         #tworzy ostrosłup z kolorkiem
    glBegin(GL_TRIANGLES)
    for triangle in triangles:
        for i, vertex in enumerate(triangle):
            glColor3fv(colors[i])
            glVertex3fv(vertices[vertex])
    glEnd()

def sierpinski_pyramid(vertices, depth):     #glowna metoda tworzenia piramidy sierpinskiego
    if depth == 0:
        draw_piramid(vertices)
        return

    mid01 = [(vertices[0][i]+vertices[1][i]) / 2 for i in range(3)]
    mid02 = [(vertices[0][i]+vertices[2][i]) / 2 for i in range(3)]
    mid03 = [(vertices[0][i]+vertices[3][i]) / 2 for i in range(3)]
    mid12 = [(vertices[1][i]+vertices[2][i]) / 2 for i in range(3)]
    mid13 = [(vertices[1][i]+vertices[3][i]) / 2 for i in range(3)]
    mid23 = [(vertices[2][i]+vertices[3][i]) / 2 for i in range(3)]

    sierpinski_pyramid([vertices[0], mid01, mid02, mid03], depth - 1)
    sierpinski_pyramid([mid01, vertices[1], mid12, mid13], depth - 1)
    sierpinski_pyramid([mid02, mid12, vertices[2], mid23], depth - 1)
    sierpinski_pyramid([mid03, mid13, mid23, vertices[3]], depth - 1)


def light():
    glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, (-5.0, 5.0, -4.0, 0)) #swiatlo punktowe
    glLightfv(GL_LIGHT0, GL_SPECULAR, (0.0, 1.0, 0.0, 1.0)) #swiatlo kierunkowe


def main():
    print("Prosty program tworzący piramidę Sierpińskiego\n"
          "Instrukcja obsługi:\n"
          "R - reset kamery do stanu początkowego\n"
          "strzałki - poruszanie kamerą\n"
          "Aby ruszać kamerą za pomocą myszy przytrzymaj lewy przycisk myszy\n"
          "Scroll up/down - przybliż/oddal kamerę\n"
          "Esc - Wyjdź z programu")
    levels = int(input("Wpisz liczbę poziomów piramidy: "))
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.mouse.set_pos(display[0] // 2, display[1] // 2)
    glEnable(GL_DEPTH_TEST)
    glClearColor(1.0, 1.0, 1.0, 1.0)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    rotation_speed = 1.0
    translation_speed = 0.1
    zoom_speed = 0.05

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        sierpinski_pyramid(vertices, levels)
        light()


        keys = pygame.key.get_pressed()

        if keys[K_LEFT]:
            glTranslatef(translation_speed, 0, 0)
        if keys[K_RIGHT]:
            glTranslatef(-translation_speed, 0, 0)
        if keys[K_UP]:
            glTranslatef(0, -translation_speed, 0)
        if keys[K_DOWN]:
            glTranslatef(0, translation_speed, 0)

        if keys[K_r]:
            glLoadIdentity()
            gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
            glTranslatef(0.0, 0.0, -5.0)

        if event.type == pygame.MOUSEWHEEL:
            zoom_factor = 1.0 + event.y * zoom_speed
            glScalef(zoom_factor, zoom_factor, zoom_factor)

        if event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
            dx, dy = event.rel
            dx *= rotation_speed
            dy *= rotation_speed
            glRotatef(dy, 1, 0, 0)
            glRotatef(dx, 0, 1, 0)

        pygame.display.flip()
        pygame.time.wait(10)

main()
