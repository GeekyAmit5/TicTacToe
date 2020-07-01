# This is a game called tic tac toe
# you can play with friend or AI


import math
import random
import pygame
import time
import os
import sys
import pkg_resources.py2_warn
import re
import fileinput


def drawGrid(color):
    s = 15
    e = 380
    d = 122
    w = 5
    for i in range(4):
        pygame.draw.line(win, color,
                         (s+d*i, s), (s+d*i, e), w)
    for i in range(4):
        pygame.draw.line(win, color,
                         (s, s+d*i), (e, s+d*i), w)


def opponent(turn):
    if turn == X:
        return O
    return X


def winCheck(turn, x, y):
    for i in range(3):
        if grid[x][i] != turn:
            break
    else:
        return True
    for i in range(3):
        if grid[i][y] != turn:
            break
    else:
        return True
    if x == y:
        for i in range(3):
            if grid[i][i] != turn:
                break
        else:
            return True
    if x + y == 2:
        for i in range(3):
            if grid[2-i][i] != turn:
                break
        else:
            return True
    return False


def reset():
    global grid, turn, undoaix, undoaiy, undox, undoy, depth
    undoaix, undoaiy, undox, undoy = -1, -1, -1, -1
    depth = 0
    for i in range(3):
        for j in range(3):
            grid[i][j] = " "
    turn = opponent(last_turn)


def undo(x, y):
    global grid, turn, depth
    grid[x][y] = " "
    turn = opponent(turn)
    win.blit(undopic, (18+122*x, 18+122*y))
    depth -= 1
    if turn == X:
        drawGrid(red)
    else:
        drawGrid(green)


def playSound(sound):
    if sound_on:
        sound.play()


def button(rect, buttoncolor, textsize, textcolor, text):
    pygame.draw.rect(win, buttoncolor, rect)
    win.blit(pygame.font.SysFont(None, textsize).render(
        text, True, textcolor), [rect.x+10, rect.y+10])


def endText(msg):
    reset()
    win.blit(pygame.font.SysFont(None, 100).render(
        msg, True, white), [200 - 20*len(msg), 170])
    button(rect6, white, 40, black, "Play Again!")
    button(rect7, white, 40, black, "Main Menu")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                playSound(click)
                mx, my = pygame.mouse.get_pos()
                if rect6.collidepoint((mx, my)):
                    game()
                elif rect7.collidepoint((mx, my)):
                    main()
        pygame.display.update()
        Clock.tick(fps)


def minimaxPro(x, y, alpha, beta, isMaximizing):
    global depth
    if winCheck(X, x, y):
        return 1
    elif winCheck(O, x, y):
        return - 1
    elif depth == 9:
        return 0
    elif isMaximizing:
        bestScore = -math.inf
        for i in range(3):
            for j in range(3):
                if grid[i][j] == " ":
                    grid[i][j] = X
                    depth += 1
                    score = minimaxPro(i, j, alpha, beta, False)
                    grid[i][j] = " "
                    depth -= 1
                    bestScore = max(score, bestScore)
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        break
        return bestScore
    else:
        bestScore = math.inf
        for i in range(3):
            for j in range(3):
                if grid[i][j] == " ":
                    grid[i][j] = O
                    depth += 1
                    score = minimaxPro(i, j, alpha, beta, True)
                    grid[i][j] = " "
                    depth -= 1
                    bestScore = min(score, bestScore)
                    beta = min(beta, score)
                    if beta <= alpha:
                        break
        return bestScore


def AI():
    global turn, undoaix, undoaiy, winx, tie, depth
    if depth == 9 and level > 0:
        x = random.randint(0, 2)
        if x == 1:
            y = 1
        else:
            y = random.choice([0, 2])
    elif random.choice([1, 1, level, level >= 2, level == 3]):
        bestScore = -math.inf
        for i in range(3):
            for j in range(3):
                if grid[i][j] == " ":
                    grid[i][j] = X
                    depth += 1
                    score = minimaxPro(i, j, -math.inf, math.inf, False)
                    grid[i][j] = " "
                    depth -= 1
                    if score > bestScore:
                        bestScore = score
                        x, y = i, j
    else:
        while True:
            x, y = random.randint(0, 2), random.randint(0, 2)
            if grid[x][y] == " ":
                break
    grid[x][y] = X
    undoaix, undoaiy = x, y
    win.blit(cross, (27+122*x, 27+122*y))
    pygame.time.delay(200)
    pygame.display.update()
    playSound(gameplay)
    depth += 1
    if winCheck(X, x, y):
        winx += 1
        endText("AI WIN!")
    elif depth == 9:
        tie += 1
        endText("TIE!")
    else:
        turn = O
        drawGrid(green)


def game():
    global grid, turn, undox, undoy, winx, wino, tie, undoaix, undoaiy, last_turn, depth
    t0 = time.time()
    win.blit(background, (0, 0))
    if turn == X:
        last_turn = X
        drawGrid(red)
        if level != -1:
            AI()
    else:
        last_turn = O
        drawGrid(green)
    win.blit(pygame.font.SysFont(
        None, 50).render("SCORE", True, white), [30, 385])
    win.blit(pygame.font.SysFont(
        None, 40).render("YOU:", True, green), [80, 416])
    win.blit(pygame.font.SysFont(
        None, 40).render("TIE:", True, white), [91, 470])
    if level != -1:
        win.blit(pygame.font.SysFont(
            None, 40).render("AI:", True, red), [109, 441])
    else:
        win.blit(pygame.font.SysFont(
            None, 40).render("FRIEND:", True, red), [34, 441])
    win.blit(pygame.font.SysFont(
        None, 45).render(str(wino), True, green), [150, 416])
    win.blit(pygame.font.SysFont(
        None, 45).render(str(winx), True, red), [150, 441])
    win.blit(pygame.font.SysFont(
        None, 45).render(str(tie), True, white), [150, 470])
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                x, y = (mx-15)//122, (my-15)//122
                if 0 <= x <= 2 and 0 <= y <= 2 and grid[x][y] == " ":
                    playSound(gameplay)
                    t0 = time.time()
                    grid[x][y] = turn
                    undox, undoy = x, y
                    if turn == X:
                        win.blit(cross, (27+122*x, 27+122*y))
                    else:
                        win.blit(nought, (25+122*x, 25+122*y))
                    pygame.display.update()
                    depth += 1
                    if winCheck(turn, x, y):
                        if turn == X:
                            winx += 1
                        else:
                            wino += 1
                        if level != -1:
                            endText("YOU WIN!")
                        else:
                            endText(turn+" WIN!")
                    elif depth == 9:
                        tie += 1
                        endText("TIE!")
                    else:
                        turn = opponent(turn)
                        if turn == X:
                            drawGrid(red)
                        else:
                            drawGrid(green)
                        pygame.display.update()
                        if level != -1:
                            AI()
                elif rect6.collidepoint((mx, my)):
                    reset()
                    game()
                elif rect7.collidepoint((mx, my)):
                    if not depth:
                        main()
                    else:
                        if undox != -1:
                            undo(undox, undoy)
                            undox = -1
                            if undoaix != -1:
                                undo(undoaix, undoaiy)
                                undoaix = -1
        if not depth:
            button(rect6, white, 40, black, "Swap turn")
            button(rect7, white, 40, black, "Main Menu")
        else:
            button(rect6, white, 40, black, "Clear")
            if undox != -1:
                button(rect7, white, 40, black, "Undo")
            else:
                button(rect7, white, 40, (128, 128, 128), "Undo")
        if depth and time_on and time.time() - t0 > time_limit:
            if level != -1:
                winx += 1
                endText("AI WIN!")
            else:
                if turn == X:
                    winx += 1
                else:
                    wino += 1
                endText(opponent(turn)+" WIN!")
        pygame.display.update()
        Clock.tick(fps)


def difficulty():
    global level
    win.blit(background, (0, 0))
    win.blit(pygame.font.SysFont(
        None, 60).render("Select Difficulty!", True, white), [40, 60])
    button(rect1, white, 50, black, "Easy")
    button(rect2, white, 50, black, "Medium")
    button(rect3, white, 50, black, "Hard")
    button(rect4, white, 50, black, "Impossible")
    button(rect5, white, 50, black, "Main Menu")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                playSound(click)
                mx, my = pygame.mouse.get_pos()
                if rect1.collidepoint((mx, my)):
                    level = 0
                    game()
                elif rect2.collidepoint((mx, my)):
                    level = 1
                    game()
                elif rect3.collidepoint((mx, my)):
                    level = 2
                    game()
                elif rect4.collidepoint((mx, my)):
                    level = 3
                    game()
                elif rect5.collidepoint((mx, my)):
                    main()
        pygame.display.update()
        Clock.tick(fps)


def about():
    win.blit(background, (0, 0))
    win.blit(pygame.font.SysFont(
        None, 80).render("Developer", True, white), [70, 30])
    win.blit(pygame.font.SysFont(
        None, 80).render("AMIT MISHRA", True, green), [20, 100])
    win.blit(pygame.font.SysFont(
        None, 80).render("IIT DELHI", True, white), [70, 170])
    win.blit(pygame.font.SysFont(
        None, 65).render("MSc Mathematics", True, white), [20, 240])
    button(rect5, white, 50, black, "MAIN MENU")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                playSound(click)
                mx, my = pygame.mouse.get_pos()
                if rect5.collidepoint((mx, my)):
                    main()
        pygame.display.update()
        Clock.tick(fps)


def options():
    global sound_on, time_on
    win.blit(background, (0, 0))
    win.blit(pygame.font.SysFont(
        None, 100).render("OPTIONS", True, white), [30, 80])
    button(rect2, white, 50, black, "ABOUT")
    button(rect5, white, 50, black, "MAIN MENU")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                playSound(click)
                mx, my = pygame.mouse.get_pos()
                if rect2.collidepoint((mx, my)):
                    about()
                elif rect3.collidepoint((mx, my)):
                    if time_on:
                        time_on = False
                    else:
                        time_on = True
                    fh = fileinput.input("data/settings.txt", inplace=True)
                    for line in fh:
                        if line.startswith("time"):
                            words = line.split()
                            line = line.replace(
                                str(int(words[-1])), str(1-int(words[-1])))
                        sys.stdout.write(line)
                elif rect4.collidepoint((mx, my)):
                    if sound_on:
                        sound_on = False
                        pygame.mixer.music.pause()
                    else:
                        sound_on = True
                        pygame.mixer.music.play(-1)
                    fh = fileinput.input("data/settings.txt", inplace=True)
                    for line in fh:
                        if line.startswith("sound"):
                            words = line.split()
                            line = line.replace(
                                str(int(words[-1])), str(1-int(words[-1])))
                        sys.stdout.write(line)
                elif rect5.collidepoint((mx, my)):
                    main()
        if time_on:
            button(rect3, green, 50, black, "TIME LIMIT 3 sec")
        else:
            button(rect3, red, 50, black, "TIME LIMIT OFF")
        if sound_on:
            button(rect4, green, 50, black, "SOUNDS ON")
        else:
            button(rect4, red, 50, black, "SOUNDS OFF")
        pygame.display.update()
        Clock.tick(fps)


def main():
    global level, winx, wino, tie
    reset()
    winx, wino, tie = 0, 0, 0
    win.blit(background, (0, 0))
    win.blit(pygame.font.SysFont(
        None, 80).render("TIC TAC TOE!", True, white), [20, 80])
    button(rect2, white, 50, black, "TWO PLAYER")
    button(rect3, white, 50, black, "YOU VS AI")
    button(rect4, white, 50, black, "OPTIONS")
    button(rect5, white, 50, black, "EXIT!")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                playSound(click)
                mx, my = pygame.mouse.get_pos()
                if rect2.collidepoint((mx, my)):
                    level = -1
                    game()
                elif rect3.collidepoint((mx, my)):
                    difficulty()
                elif rect4.collidepoint((mx, my)):
                    options()
                elif rect5.collidepoint((mx, my)):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()
        Clock.tick(fps)


pygame.init()
pygame.display.set_caption("Tic Tac Toe")
pygame.display.set_icon(pygame.image.load("data/images/icon.ico"))
win = pygame.display.set_mode((400, 500))
background = pygame.image.load("data/images/background.jpg")
cross = pygame.image.load("data/images/cross.png")
nought = pygame.image.load("data/images/nought.png")
undopic = pygame.image.load("data/images/undo.jpg")
clear = pygame.mixer.Sound("data/audio/clear.wav")
tiemusic = pygame.mixer.Sound("data/audio/tie.wav")
click = pygame.mixer.Sound("data/audio/click.wav")
gameplay = pygame.mixer.Sound("data/audio/gameplay.wav")
undomusic = pygame.mixer.Sound("data/audio/undo.wav")
pygame.mixer.music.load("data/audio/music.wav")
Clock = pygame.time.Clock()
rect1 = pygame.Rect(50, 130, 300, 60)
rect2 = pygame.Rect(50, 200, 300, 60)
rect3 = pygame.Rect(50, 270, 300, 60)
rect4 = pygame.Rect(50, 340, 300, 60)
rect5 = pygame.Rect(50, 410, 300, 60)
rect6 = pygame.Rect(220, 390, 170, 45)
rect7 = pygame.Rect(220, 440, 170, 45)
fps = 10
black = (0, 0, 0)
white = (255, 255, 255)
green = (51, 204, 89)
red = (250, 51, 51)


X = "X"
O = "O"
grid = [[" " for x in range(3)] for y in range(3)]
turn = random.choice([X, O])
last_turn = turn
undoaix = -1
undoaiy = -1
undox = -1
undoy = -1
level = -1
winx = 0
wino = 0
tie = 0
depth = 0
time_limit = 3
time_on = None
sound_on = None
fh = open("data/settings.txt")
for line in fh:
    if line.startswith("sound"):
        pos = line.find("=")
        sound_on = bool(int(line[pos+1:]))
    elif line.startswith("time"):
        pos = line.find("=")
        time_on = bool(int(line[pos+1:]))
fh.close()

if sound_on:
    pygame.mixer.music.play(-1)

main()
