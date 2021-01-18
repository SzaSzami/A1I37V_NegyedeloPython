import numpy as np
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

#NYERES() vizsgálása
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
game_over = False
turn = 0

#játék kirajzolása
pygame.init()
#ablak mérete
MERET = 100
SZELESSEG = OSZLOPOK * MERET
MAGASSAG = (SOROK + 1) * MERET
SIZE = (SZELESSEG, MAGASSAG)
RADIUS = int(MERET / 2 - 5)
KEPERNYO = pygame.display.set_mode(SIZE)
TABLA_KIRAJZOL(TABLA)
pygame.display.update()
BETU = pygame.font.SysFont("monospace", 75)

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

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
            PRINT_TABLA(TABLA)
            TABLA_KIRAJZOL(TABLA)
            turn += 1
            turn = turn % 2
            if game_over:
                pygame.time.wait(3000)
