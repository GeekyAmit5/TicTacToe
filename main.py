# This is a game called tic tac toe
# you can play with friend or AI
# add score,reset and undo button


import math
import random
import pygame
import time


pygame.init()
pygame.display.set_caption("Tic Tac Toe")
pygame.display.set_icon(pygame.image.load("icon.png"))
win = pygame.display.set_mode((400, 500))
background = pygame.image.load("background.jpg")
board = pygame.image.load("board.png")
cross = pygame.image.load("cross.png")
nought = pygame.image.load("nought.png")
Clock = pygame.time.Clock()
fps = 10
black = (0, 0, 0)
white = (255, 255, 255)
run = True
level = -1


grid = [[" " for x in range(3)] for y in range(3)]
X = "X"
O = "O"
turn = random.choice([X, O])


def opponent(turn):
    if turn == X:
        return O
    return X


def winCheck(x, y):
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


def endText(msg):
    global run, grid, turn
    for i in range(3):
        for j in range(3):
            grid[i][j] = " "
    turn = opponent(turn)
    time.sleep(0.25)
    win.blit(background, (0, 0))
    text = pygame.font.SysFont(
        None, 100).render(msg, True, white)
    win.blit(text, [200 - 20*len(msg), 130])

    pygame.draw.rect(win, white, (60, 250, 300, 60))
    text = pygame.font.SysFont(
        None, 50).render("Play Again!", True, black)
    win.blit(text, [85, 260])

    pygame.draw.rect(win, white, (60, 350, 300, 60))
    text = pygame.font.SysFont(
        None, 50).render("Main Menu", True, black)
    win.blit(text, [85, 360])

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if 60 <= mx <= 360 and 250 <= my <= 310:
                    play()
                elif 60 <= mx <= 360 and 350 <= my <= 410:
                    main()
        pygame.display.update()
        Clock.tick(fps)


def isWinner(turn):
    for i in range(3):
        for j in range(3):
            if grid[i][j] != turn:
                break
        else:
            return True
        for j in range(3):
            if grid[j][i] != turn:
                break
        else:
            return True

    for i in range(3):
        if grid[i][i] != turn:
            break
    else:
        return True

    for i in range(3):
        if grid[i][2 - i] != turn:
            break
    else:
        return True
    return False


def minimaxPro(alpha, beta, isMaximizing):
    if isWinner(X):
        return 1
    if isWinner(O):
        return - 1
    if isTie():
        return 0
    if isMaximizing:
        bestScore = -math.inf
        for i in range(3):
            for j in range(3):
                if grid[i][j] == " ":
                    grid[i][j] = X
                    score = minimaxPro(alpha, beta, False)
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
                    score = minimaxPro(alpha, beta, True)
                    grid[i][j] = " "
                    bestScore = min(score, bestScore)
                    beta = min(beta, score)
                    if beta <= alpha:
                        break
        return bestScore


def AI():
    global turn, grid
    if level == 3 or random.choice([0, 1, level, level == 2]):
        bestScore = -math.inf
        for i in range(3):
            for j in range(3):
                if grid[i][j] == " ":
                    grid[i][j] = X
                    score = minimaxPro(-math.inf, math.inf, False)
                    grid[i][j] = " "
                    if score > bestScore:
                        bestScore = score
                        x, y = i, j
    else:
        while True:
            i, j = random.randint(0, 2), random.randint(0, 2)
            if grid[i][j] == " ":
                x, y = i, j
                break
    if x == 0:
        xcord = 40
    elif x == 1:
        xcord = 160
    elif x == 2:
        xcord = 275

    if y == 0:
        ycord = 40
    elif y == 1:
        ycord = 160
    elif y == 2:
        ycord = 275

    win.blit(cross, (xcord, ycord))
    pygame.display.update()
    grid[x][y] = X
    if winCheck(x, y):
        endText("AI WIN!")
    elif isTie():
        endText("TIE!")
    else:
        turn = O


def play():
    global run, grid, turn
    win.blit(background, (0, 0))
    win.blit(board, (10, 10))
    if level != -1 and turn == X:
        AI()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                x, y = -1, -1
                xcord, ycord = 0, 0
                if 35 < mx < 130:
                    x, xcord = 0, 40
                elif 155 < mx < 250:
                    x, xcord = 1, 160
                elif 270 < mx < 365:
                    x, xcord = 2, 275

                if 35 < my < 130:
                    y, ycord = 0, 40
                elif 155 < my < 250:
                    y, ycord = 1, 160
                elif 270 < my < 365:
                    y, ycord = 2, 275

                if x != -1 and y != -1:
                    if grid[x][y] == " ":
                        if turn == X:
                            win.blit(cross, (xcord, ycord))
                        else:
                            win.blit(nought, (xcord, ycord))
                        pygame.display.update()
                        grid[x][y] = turn
                        if winCheck(x, y):
                            if level != -1:
                                endText("YOU WIN!")
                            else:
                                endText(turn+" WIN!")
                        elif isTie():
                            endText("TIE!")
                        else:
                            turn = opponent(turn)
                            if level != -1:
                                AI()

        pygame.display.update()
        Clock.tick(fps)


def difficulty():
    global run, level
    win.blit(background, (0, 0))
    text = pygame.font.SysFont(
        None, 60).render("Select Difficulty!", True, white)
    win.blit(text, [40, 60])

    pygame.draw.rect(win, white, (60, 130, 300, 60))
    text = pygame.font.SysFont(
        None, 50).render("Easy", True, black)
    win.blit(text, [85, 140])

    pygame.draw.rect(win, white, (60, 200, 300, 60))
    text = pygame.font.SysFont(
        None, 50).render("Medium", True, black)
    win.blit(text, [85, 210])

    pygame.draw.rect(win, white, (60, 270, 300, 60))
    text = pygame.font.SysFont(
        None, 50).render("Hard", True, black)
    win.blit(text, [85, 280])

    pygame.draw.rect(win, white, (60, 340, 300, 60))
    text = pygame.font.SysFont(
        None, 50).render("Impossible", True, black)
    win.blit(text, [85, 350])

    pygame.draw.rect(win, white, (60, 410, 300, 60))
    text = pygame.font.SysFont(
        None, 50).render("Main Menu", True, black)
    win.blit(text, [85, 420])

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if 60 <= mx <= 360 and 130 <= my <= 190:
                    level = 0
                    play()
                elif 60 <= mx <= 360 and 200 <= my <= 260:
                    level = 1
                    play()
                elif 60 <= mx <= 360 and 270 <= my <= 330:
                    level = 2
                    play()
                elif 60 <= mx <= 360 and 340 <= my <= 400:
                    level = 3
                    play()
                elif 60 <= mx <= 360 and 410 <= my <= 460:
                    main()
        pygame.display.update()
        Clock.tick(fps)


def main():
    global run
    win.blit(background, (0, 0))
    text = pygame.font.SysFont(
        None, 70).render("TIC TAC TOE!", True, white)
    win.blit(text, [50, 80])

    pygame.draw.rect(win, white, (60, 200, 300, 60))
    text = pygame.font.SysFont(
        None, 50).render("YOU VS FRIEND", True, black)
    win.blit(text, [75, 210])

    pygame.draw.rect(win, white, (60, 300, 300, 60))
    text = pygame.font.SysFont(
        None, 50).render("YOU VS AI", True, black)
    win.blit(text, [85, 310])

    pygame.draw.rect(win, white, (60, 400, 300, 60))
    text = pygame.font.SysFont(
        None, 50).render("EXIT!", True, black)
    win.blit(text, [85, 410])

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if 60 <= mx <= 360 and 200 <= my <= 260:
                    play()
                elif 60 <= mx <= 360 and 300 <= my <= 360:
                    difficulty()
                elif 60 <= mx <= 360 and 400 <= my <= 460:
                    exit()
        pygame.display.update()
        Clock.tick(fps)


main()
