# This is a game called tic tac toe
# you can play with friend or AI
# code improvement left


import math
import random
import pygame
import time
import os
import sys
import pkg_resources.py2_warn


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


def isTie():
    for i in range(3):
        for j in range(3):
            if grid[i][j] == " ":
                return False
    else:
        return True


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


def font(size, color, msg):
    return pygame.font.SysFont(None, size).render(msg, True, color)


def endText(msg):
    reset()
    pygame.draw.rect(win, white, rect1)
    pygame.draw.rect(win, white, rect2)
    win.blit(font(100, white, msg), [200 - 20*len(msg), 170])
    win.blit(font(40, black, "Play Again!"), [230, 397])
    win.blit(font(40, black, "Main Menu"), [230, 447])
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                playSound(click)
                mx, my = pygame.mouse.get_pos()
                if rect1.collidepoint((mx, my)):
                    game()
                elif rect2.collidepoint((mx, my)):
                    main()
        pygame.display.update()
        Clock.tick(fps)


def minimaxPro(x, y, alpha, beta, isMaximizing):
    if winCheck(X, x, y):
        return 1
    if winCheck(O, x, y):
        return - 1
    if isTie():
        return 0
    if isMaximizing:
        bestScore = -math.inf
        for i in range(3):
            for j in range(3):
                if grid[i][j] == " ":
                    grid[i][j] = X
                    score = minimaxPro(i, j, alpha, beta, False)
                    grid[i][j] = " "
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
                    score = minimaxPro(i, j, alpha, beta, True)
                    grid[i][j] = " "
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
                    score = minimaxPro(i, j, -math.inf, math.inf, False)
                    grid[i][j] = " "
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
    elif isTie():
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
                    elif isTie():
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
                elif 220 <= mx <= 370 and 390 <= my <= 435:
                    reset()
                    game()
                elif 220 <= mx <= 370 and 440 <= my <= 485:
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
            pygame.draw.rect(win, white, (220, 390, 170, 45))
            win.blit(pygame.font.SysFont(
                None, 40).render("Swap turn", True, black), [230, 397])
            pygame.draw.rect(win, white, (220, 440, 170, 45))
            win.blit(pygame.font.SysFont(
                None, 40).render("Main Menu", True, black), [230, 447])
        else:
            pygame.draw.rect(win, white, (220, 390, 170, 45))
            win.blit(pygame.font.SysFont(
                None, 50).render("Clear", True, black), [250, 397])
            pygame.draw.rect(win, white, (220, 440, 170, 45))
            if undox != -1:
                win.blit(pygame.font.SysFont(
                    None, 50).render("Undo", True, black), [250, 447])
            else:
                win.blit(pygame.font.SysFont(
                    None, 50).render("Undo", True, (128, 128, 128)), [250, 447])
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
    pygame.draw.rect(win, white, (60, 130, 300, 60))
    win.blit(pygame.font.SysFont(
        None, 50).render("Easy", True, black), [85, 140])
    pygame.draw.rect(win, white, (60, 200, 300, 60))
    win.blit(pygame.font.SysFont(
        None, 50).render("Medium", True, black), [85, 210])
    pygame.draw.rect(win, white, (60, 270, 300, 60))
    win.blit(pygame.font.SysFont(
        None, 50).render("Hard", True, black), [85, 280])
    pygame.draw.rect(win, white, (60, 340, 300, 60))
    win.blit(pygame.font.SysFont(
        None, 50).render("Impossible", True, black), [85, 350])
    pygame.draw.rect(win, white, (60, 410, 300, 60))
    win.blit(pygame.font.SysFont(
        None, 50).render("Main Menu", True, black), [85, 420])
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                playSound(click)
                mx, my = pygame.mouse.get_pos()
                if 60 <= mx <= 360 and 410 <= my <= 460:
                    main()
                for i in range(4):
                    if 60 <= mx <= 360 and 130+i*70 <= my <= 190+i*70:
                        level = i
                        game()
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
    pygame.draw.rect(win, white, (50, 410, 300, 60))
    win.blit(pygame.font.SysFont(
        None, 50).render("MAIN MENU", True, black), [85, 420])
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                playSound(click)
                mx, my = pygame.mouse.get_pos()
                if 50 <= mx <= 350 and 410 <= my <= 470:
                    main()
        pygame.display.update()
        Clock.tick(fps)


def options():
    global sound_on, time_on
    win.blit(background, (0, 0))
    win.blit(pygame.font.SysFont(
        None, 100).render("OPTIONS", True, white), [30, 80])
    pygame.draw.rect(win, white, (50, 200, 300, 60))
    win.blit(pygame.font.SysFont(
        None, 50).render("ABOUT", True, black), [85, 210])
    pygame.draw.rect(win, white, (50, 410, 300, 60))
    win.blit(pygame.font.SysFont(
        None, 50).render("MAIN MENU", True, black), [85, 420])
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                playSound(click)
                mx, my = pygame.mouse.get_pos()
                if 50 <= mx <= 350:
                    for i in range(4):
                        if 200 + i*70 <= my <= 260 + i*70:
                            if not i:
                                about()
                            elif i == 1:
                                if time_on:
                                    time_on = False
                                else:
                                    time_on = True
                            elif i == 2:
                                if sound_on:
                                    sound_on = False
                                    pygame.mixer.music.pause()
                                else:
                                    sound_on = True
                                    pygame.mixer.music.unpause()
                            elif i == 3:
                                main()
        if time_on:
            pygame.draw.rect(win, green, (50, 270, 300, 60))
            win.blit(pygame.font.SysFont(
                None, 50).render("TIME LIMIT 3 sec", True, black), [60, 280])
        else:
            pygame.draw.rect(win, red, (50, 270, 300, 60))
            win.blit(pygame.font.SysFont(
                None, 50).render("TIME LIMIT OFF", True, black), [65, 280])
        if sound_on:
            pygame.draw.rect(win, green, (50, 340, 300, 60))
            win.blit(pygame.font.SysFont(
                None, 50).render("SOUNDS ON", True, black), [85, 350])
        else:
            pygame.draw.rect(win, red, (50, 340, 300, 60))
            win.blit(pygame.font.SysFont(
                None, 50).render("SOUNDS OFF", True, black), [85, 350])
        pygame.display.update()
        Clock.tick(fps)


def main():
    global level, winx, wino, tie
    reset()
    winx, wino, tie = 0, 0, 0
    win.blit(background, (0, 0))
    win.blit(pygame.font.SysFont(
        None, 80).render("TIC TAC TOE!", True, white), [20, 80])
    pygame.draw.rect(win, white, (50, 200, 300, 60))
    win.blit(pygame.font.SysFont(
        None, 50).render("TWO PLAYER", True, black), [85, 210])
    pygame.draw.rect(win, white, (50, 270, 300, 60))
    win.blit(pygame.font.SysFont(
        None, 50).render("YOU VS AI", True, black), [85, 280])
    pygame.draw.rect(win, white, (50, 340, 300, 60))
    win.blit(pygame.font.SysFont(
        None, 50).render("OPTIONS", True, black), [85, 350])
    pygame.draw.rect(win, red, (50, 410, 300, 60))
    win.blit(pygame.font.SysFont(
        None, 50).render("EXIT!", True, black), [85, 420])
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                playSound(click)
                mx, my = pygame.mouse.get_pos()
                if 50 <= mx <= 350:
                    for i in range(4):
                        if 200 + i*70 <= my <= 260 + i*70:
                            if not i:
                                level = -1
                                game()
                            elif i == 1:
                                difficulty()
                            elif i == 2:
                                options()
                            elif i == 3:
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
pygame.mixer.music.play(-1)
Clock = pygame.time.Clock()
fps = 10
black = (0, 0, 0)
white = (255, 255, 255)
green = (51, 204, 89)
red = (250, 51, 51)
rect1 = pygame.Rect(220, 390, 170, 45)
rect2 = pygame.Rect(220, 440, 170, 45)


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
time_on = False
sound_on = True


main()
