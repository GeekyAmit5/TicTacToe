# This is a game called tic tac toe
# you can play with friend or AI
# add score,reset and undo button


import math
import random
import pygame
import sys


pygame.init()
pygame.display.set_caption("Tic Tac Toe")
pygame.display.set_icon(pygame.image.load("icon.png"))
win = pygame.display.set_mode((400, 500))
background = pygame.image.load("background.jpg")
greenboard = pygame.image.load("greenboard.png")
redboard = pygame.image.load("redboard.png")
cross = pygame.image.load("cross.png")
nought = pygame.image.load("nought.png")
undopic = pygame.image.load("undo.jpg")
Clock = pygame.time.Clock()
fps = 10
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
level = -1


grid = [[" " for x in range(3)] for y in range(3)]
X = "X"
O = "O"
turn = random.choice([X, O])
undox = -1
undoy = -1
winx = 0
wino = 0
tie = 0
undoaix = -1
undoaiy = -1


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


def reset():
    global grid, turn, undoaix, undoaiy, undox, undoy
    undoaix, undoaiy, undox, undoy = -1, -1, -1, -1
    for i in range(3):
        for j in range(3):
            grid[i][j] = " "
    turn = random.choice([X, O])
    play()


def undo(x, y):
    global grid, turn, undox, undoy
    grid[x][y] = " "
    turn = opponent(turn)
    xcord, ycord = coordinates(x, y)
    win.blit(undopic, (xcord-10, ycord-10))
    if turn == X:
        win.blit(redboard, (10, 10))
    else:
        win.blit(greenboard, (10, 10))
    undox, undoy = -1, -1


def endText(msg):
    global grid, turn, undoaix, undoaiy, undox, undoy
    for i in range(3):
        for j in range(3):
            grid[i][j] = " "
    turn = opponent(turn)
    undoaix, undoaiy, undox, undoy = -1, -1, -1, -1
    text = pygame.font.SysFont(
        None, 100).render(msg, True, black)
    win.blit(text, [200 - 20*len(msg), 170])

    pygame.draw.rect(win, white, (220, 390, 170, 45))
    text = pygame.font.SysFont(
        None, 40).render("Play Again!", True, black)
    win.blit(text, [230, 397])

    pygame.draw.rect(win, white, (220, 440, 170, 45))
    text = pygame.font.SysFont(
        None, 40).render("Main Menu", True, black)
    win.blit(text, [230, 447])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if 220 <= mx <= 390 and 390 <= my <= 435:
                    play()
                elif 220 <= mx <= 390 and 440 <= my <= 485:
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
    global turn, grid, undoaix, undoaiy, winx, tie
    depth = 0
    for i in range(3):
        for j in range(3):
            if grid[i][j] == " ":
                depth += 1
    if level > 1 and depth == 9:
        x, y = random.choice([0, 2]), random.choice([0, 2])
    elif level > 2 and depth == 8:
        if grid[1][1] == O:
            x, y = random.choice([0, 2]), random.choice([0, 2])
        else:
            x, y = 1, 1
    elif random.choice([1, 1, level, level >= 2, level == 3]):
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

    undoaix, undoaiy = x, y
    xcord, ycord = coordinates(x, y)
    win.blit(cross, (xcord, ycord))
    pygame.display.update()
    grid[x][y] = X
    if winCheck(x, y):
        winx += 1
        endText("AI WIN!")
    elif isTie():
        tie += 1
        endText("TIE!")
    else:
        turn = O
        win.blit(greenboard, (10, 10))


def coordinates(x, y):
    xcord, ycord = 0, 0
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
    return [xcord, ycord]


def play():
    global grid, turn, undox, undoy, winx, wino, tie, undoaix, undoaiy
    win.blit(background, (0, 0))
    if turn == X:
        win.blit(redboard, (10, 10))
    else:
        win.blit(greenboard, (10, 10))
    pygame.draw.rect(win, white, (220, 390, 150, 45))
    text = pygame.font.SysFont(
        None, 50).render("Reset", True, black)
    win.blit(text, [230, 397])

    pygame.draw.rect(win, white, (220, 440, 150, 45))
    text = pygame.font.SysFont(
        None, 50).render("Undo", True, black)
    win.blit(text, [230, 447])

    text = pygame.font.SysFont(
        None, 50).render("SCORE", True, black)
    win.blit(text, [30, 385])

    text = pygame.font.SysFont(
        None, 40).render("YOU:", True, green)
    win.blit(text, [80, 416])

    text = pygame.font.SysFont(
        None, 40).render("TIE:", True, black)
    win.blit(text, [90, 470])

    if level != -1:
        text = pygame.font.SysFont(
            None, 40).render("AI:", True, red)
        win.blit(text, [110, 441])
        if turn == X:
            AI()
    else:
        text = pygame.font.SysFont(
            None, 40).render("FRIEND:", True, red)
        win.blit(text, [35, 441])

    text = pygame.font.SysFont(
        None, 45).render(str(wino), True, black)
    win.blit(text, [150, 416])

    text = pygame.font.SysFont(
        None, 45).render(str(winx), True, black)
    win.blit(text, [150, 441])

    text = pygame.font.SysFont(
        None, 45).render(str(tie), True, black)
    win.blit(text, [150, 470])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                x, y = -1, -1
                if 35 < mx < 130:
                    x = 0
                elif 155 < mx < 250:
                    x = 1
                elif 270 < mx < 365:
                    x = 2
                if 35 < my < 130:
                    y = 0
                elif 155 < my < 250:
                    y = 1
                elif 270 < my < 365:
                    y = 2
                if x != -1 and y != -1:
                    undox, undoy = x, y
                    xcord, ycord = coordinates(x, y)
                    if grid[x][y] == " ":
                        if turn == X:
                            win.blit(cross, (xcord, ycord))
                        else:
                            win.blit(nought, (xcord, ycord))
                        pygame.display.update()
                        grid[x][y] = turn
                        if winCheck(x, y):
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
                                win.blit(redboard, (10, 10))
                            else:
                                win.blit(greenboard, (10, 10))
                            if level != -1:
                                AI()

                elif 220 <= mx <= 370 and 390 <= my <= 435:
                    reset()
                elif 220 <= mx <= 370 and 440 <= my <= 485:
                    if undox != -1:
                        undo(undox, undoy)
                        if undoaix != -1:
                            undo(undoaix, undoaiy)
                            undoaix, undoaiy = -1, -1

        pygame.display.update()
        Clock.tick(fps)


def difficulty():
    global level
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

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
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
    global level, winx, wino, tie
    winx, wino, tie = 0, 0, 0
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

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if 60 <= mx <= 360 and 200 <= my <= 260:
                    level = -1
                    play()
                elif 60 <= mx <= 360 and 300 <= my <= 360:
                    difficulty()
                elif 60 <= mx <= 360 and 400 <= my <= 460:
                    sys.exit()
        pygame.display.update()
        Clock.tick(fps)


main()
