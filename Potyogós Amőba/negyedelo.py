import numpy as np
from tkinter import messagebox
import pygame
import sys
import math

#színek
KEK = (0, 50, 255)
FEKETE = (0, 0, 0)
PINK = (200, 0, 80)
SARGA = (255, 255, 0)
SOROK = 6
OSZLOPOK = 7
mainmenurunning = True
game_over = False


#tábla létrehozása
def LETREHOZ_TABLA():
    TABLA = np.zeros((SOROK, OSZLOPOK))
    return TABLA
def drop_KORONG(TABLA, row, col, KORONG):
    TABLA[row][col] = KORONG
def is_valid_location(TABLA, col):
    return TABLA[SOROK - 1][col] == 0
def get_next_open_row(TABLA, col):
    for r in range(SOROK):
        if TABLA[r][col] == 0:
            return r
def PRINT_TABLA(TABLA):
    print(np.flip(TABLA, 0))

#NYERÉS vizsgálása
def NYERES(TABLA, KORONG):
    #vízszintes vizsgálat
    for I in range(OSZLOPOK - 3):
        for J in range(SOROK):
            if TABLA[J][I] == KORONG and TABLA[J][I + 1] == KORONG and TABLA[J][I + 2] == KORONG and TABLA[J][
                I + 3] == KORONG:
                return True
    #függőlegesen
    for I in range(OSZLOPOK):
        for J in range(SOROK - 3):
            if TABLA[J][I] == KORONG and TABLA[J + 1][I] == KORONG and TABLA[J + 2][I] == KORONG and TABLA[J + 3][
                I] == KORONG:
                return True
    #keresztben
    for I in range(OSZLOPOK - 3):
        for J in range(SOROK - 3):
            if TABLA[J][I] == KORONG and TABLA[J + 1][I + 1] == KORONG and TABLA[J + 2][I + 2] == KORONG and TABLA[J + 3][
                I + 3] == KORONG:
                return True
    #keresztben
    for I in range(OSZLOPOK - 3):
        for J in range(3, SOROK):
            if TABLA[J][I] == KORONG and TABLA[J - 1][I + 1] == KORONG and TABLA[J - 2][I + 2] == KORONG and TABLA[J - 3][
                I + 3] == KORONG:
                return True

#tábla kirajzolása
def TABLA_KIRAJZOL(TABLA):
    for I in range(OSZLOPOK):
        for J in range(SOROK):
            pygame.draw.rect(KEPERNYO, KEK, (I * MERET, J * MERET + MERET, MERET, MERET))
            pygame.draw.circle(KEPERNYO, FEKETE, (
                int(I * MERET + MERET / 2), int(J * MERET + MERET + MERET / 2)), RADIUS)

    for I in range(OSZLOPOK):
        for J in range(SOROK):
            if TABLA[J][I] == 1:
                pygame.draw.circle(KEPERNYO, PINK, (
                    int(I * MERET + MERET / 2), MAGASSAG - int(J * MERET + MERET / 2)), RADIUS)
            elif TABLA[J][I] == 2:
                pygame.draw.circle(KEPERNYO, SARGA, (
                    int(I * MERET + MERET / 2), MAGASSAG - int(J * MERET + MERET / 2)), RADIUS)
    pygame.display.update()

TABLA = LETREHOZ_TABLA()
PRINT_TABLA(TABLA)
turn = 0

#játék kirajzolása
pygame.init()
#ablak mérete
MERET = 100
SZELESSEG = OSZLOPOK * MERET
scwidth = OSZLOPOK * MERET
MAGASSAG = (SOROK + 1) * MERET
scheight = (SOROK + 1) * MERET
SIZE = (SZELESSEG, MAGASSAG)
screen = pygame.display.set_mode((scwidth, scheight))
RADIUS = int(MERET / 2 - 5)
KEPERNYO = pygame.display.set_mode(SIZE)
TABLA_KIRAJZOL(TABLA)
pygame.display.update()
BETU = pygame.font.SysFont("monospace", 75)

#ha mainmenurunning akkor gameover=true, mainmenurunning = true
#ha start akkor mainmenurunning false, gameover = false

while mainmenurunning:
    game_over = True
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 250 <= mouse[0] <= 550 and 250 <= mouse[1] <= 325:
                screen.fill((0, 0, 0))
                pygame.display.update()
                mainmenurunning = False
                game_over = False

            elif 250 <= mouse[0] <= 550 and 350 <= mouse[1] <= 425:
                pygame.quit()
                sys.exit()

    screen.fill((255, 80, 100))
    # négyzet megrajzolás && hover effect
    if 250 <= mouse[0] <= 550 and 250 <= mouse[1] <= 325:
        pygame.draw.rect(screen, (255, 134, 25), (250, 250, 300, 75))
    else:
        pygame.draw.rect(screen, (255, 50, 80), (250, 250, 300, 75))

    if 250 <= mouse[0] <= 550 and 350 <= mouse[1] <= 425:
        pygame.draw.rect(screen, (255, 134, 25), (250, 350, 300, 75))
    else:
        pygame.draw.rect(screen, (255, 50, 80), (250, 350, 300, 75))

    # megjelenő szöveg a mainmenuben
    font = pygame.font.SysFont("Times new roman", 24)
    StartText = font.render("Start", True, (0, 0, 0))
    QuitGameText = font.render("Kilépés", True, (0, 0, 0))
    screen.blit(StartText, (350, 275))
    screen.blit(QuitGameText, (350, 375))

    pygame.display.update()

#a játék
while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                mainmenurunning = True
                game_over = True

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(KEPERNYO, FEKETE, (0, 0, SZELESSEG, MERET))
            position_x = event.pos[0]
            if turn == 0:
                pygame.draw.circle(KEPERNYO, PINK, (position_x, int(MERET / 2)), RADIUS)
            else:
                pygame.draw.circle(KEPERNYO, SARGA, (position_x, int(MERET / 2)), RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(KEPERNYO, FEKETE, (0, 0, SZELESSEG, MERET))
            #Első játékos rak
            if turn == 0:
                position_x = event.pos[0]
                col = int(math.floor(position_x / MERET))
                if is_valid_location(TABLA, col):
                    row = get_next_open_row(TABLA, col)
                    drop_KORONG(TABLA, row, col, 1)
                    if NYERES(TABLA, 1):
                        label = BETU.render("A pink nyert!", 1, PINK)

                        KEPERNYO.blit(label, (40, 10))

                        game_over = True
                        messagebox.showinfo("Játék vége", "A pink nyert! Játék vége.")
            #Második játékos rak
            else:
                position_x = event.pos[0]
                col = int(math.floor(position_x / MERET))
                if is_valid_location(TABLA, col):
                    row = get_next_open_row(TABLA, col)
                    drop_KORONG(TABLA, row, col, 2)
                    if NYERES(TABLA, 2):
                        label = BETU.render("A sárga nyert!", 1, SARGA)

                        KEPERNYO.blit(label, (40, 10))

                        game_over = True
                        messagebox.showinfo("Játék vége", "A sárga nyert! Játék vége.")
            PRINT_TABLA(TABLA)
            TABLA_KIRAJZOL(TABLA)
            turn += 1
            turn = turn % 2
            if game_over:
                pygame.time.wait(3000)
