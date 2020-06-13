# This is a game called tic tac toe
# you can play with friend or AI


import math
import random
import pygame
import os


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
    global grid, turn, undoaix, undoaiy, undox, undoy
    undoaix, undoaiy, undox, undoy = -1, -1, -1, -1
    for i in range(3):
        for j in range(3):
            grid[i][j] = " "
    turn = opponent(last_turn)


def undo(x, y):
    global grid, turn
    grid[x][y] = " "
    turn = opponent(turn)
    win.blit(undopic, (18+122*x, 18+122*y))
    if turn == X:
        drawGrid(red)
    else:
        drawGrid(green)


def endText(msg):
    reset()
    text = pygame.font.SysFont(
        None, 100).render(msg, True, white)
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
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if 220 <= mx <= 390 and 390 <= my <= 435:
                    play()
                elif 220 <= mx <= 390 and 440 <= my <= 485:
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
    global turn, undoaix, undoaiy, winx, tie
    depth = 0
    for i in range(3):
        for j in range(3):
            if grid[i][j] == " ":
                depth += 1
    if depth == 9 and level > 1:
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
    if winCheck(X, x, y):
        winx += 1
        endText("AI WIN!")
    elif isTie():
        tie += 1
        endText("TIE!")
    else:
        turn = O
        drawGrid(green)


def play():
    global grid, turn, undox, undoy, winx, wino, tie, undoaix, undoaiy, last_turn
    win.blit(background, (0, 0))
    if turn == X:
        last_turn = X
        drawGrid(red)
        if level != -1:
            AI()
    else:
        last_turn = O
        drawGrid(green)
    pygame.draw.rect(win, white, (220, 390, 150, 45))
    win.blit(pygame.font.SysFont(
        None, 50).render("Clear", True, black), [230, 397])
    pygame.draw.rect(win, white, (220, 440, 150, 45))
    win.blit(pygame.font.SysFont(
        None, 50).render("Undo", True, black), [230, 447])
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
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                x, y = (mx-15)//122, (my-15)//122
                if 0 <= x <= 2 and 0 <= y <= 2 and grid[x][y] == " ":
                    grid[x][y] = turn
                    undox, undoy = x, y
                    if turn == X:
                        win.blit(cross, (27+122*x, 27+122*y))
                    else:
                        win.blit(nought, (25+122*x, 25+122*y))
                    pygame.display.update()
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
                    play()
                elif 220 <= mx <= 370 and 440 <= my <= 485:
                    if undox != -1:
                        undo(undox, undoy)
                        undox = -1
                        if undoaix != -1:
                            undo(undoaix, undoaiy)
                            undoaix = -1
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
                exit()
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
    reset()
    winx, wino, tie = 0, 0, 0
    win.blit(background, (0, 0))
    win.blit(pygame.font.SysFont(
        None, 70).render("TIC TAC TOE!", True, white), [50, 80])
    pygame.draw.rect(win, white, (60, 200, 300, 60))
    win.blit(pygame.font.SysFont(
        None, 50).render("YOU VS FRIEND", True, black), [75, 210])
    pygame.draw.rect(win, white, (60, 300, 300, 60))
    win.blit(pygame.font.SysFont(
        None, 50).render("YOU VS AI", True, black), [85, 310])
    pygame.draw.rect(win, white, (60, 400, 300, 60))
    win.blit(pygame.font.SysFont(
        None, 50).render("EXIT!", True, black), [85, 410])
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if 60 <= mx <= 360 and 200 <= my <= 260:
                    level = -1
                    play()
                elif 60 <= mx <= 360 and 300 <= my <= 360:
                    difficulty()
                elif 60 <= mx <= 360 and 400 <= my <= 460:
                    exit()
        pygame.display.update()
        Clock.tick(fps)


pygame.init()
pygame.display.set_caption("Tic Tac Toe")
pygame.display.set_icon(pygame.image.load(
    os.path.join("data/images", "icon.png")))
win = pygame.display.set_mode((400, 500))
background = pygame.image.load(os.path.join("data/images", "background.jpg"))
cross = pygame.image.load(os.path.join("data/images", "cross.png"))
nought = pygame.image.load(os.path.join("data/images", "nought.png"))
undopic = pygame.image.load(os.path.join("data/images", "undo.jpg"))
Clock = pygame.time.Clock()
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


main()
