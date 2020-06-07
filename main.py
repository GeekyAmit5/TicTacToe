
import math
import random
import pygame
import time

pygame.init()
width = 300
height = 300
row = 3
column = 3
pygame.display.set_caption("Tic Tac Toe")
win = pygame.display.set_mode((width, height))
black = (0, 0, 0)
white = (255, 255, 255)
yellow = (255, 255, 0)
red = (255, 0, 0)
green = (0, 255, 0)
grid = [[" " for x in range(row)] for y in range(column)]
ai = "X"
human = "O"
turn = random.choice([ai, human])


def drawGrid(color, row, column):
    for i in range(1, column):
        pygame.draw.line(win, color,
                         (i * width / column, 0), (i * width / column, height))
    for i in range(1, row):
        pygame.draw.line(win, color,
                         (0, i * height / row), (width, i * height / row))


def convert(x, y):
    return [y * row // height, x * column // width]


def colorIt(x, y, color=black):
    pygame.draw.rect(win, color, (y * width / column+2, x *
                                  height / row+2, width / column-4, height / row-4))


def opponent(turn):
    if turn == ai:
        return human
    return ai


def printGrid():
    print("\n-------------")
    for i in range(3):
        print("|", end="")
        for j in range(3):
            print(" {} ".format(grid[i][j]), end="|")
        print("\n-------------")
    print()


def cross(y, x, color=white):
    pygame.draw.line(win, color, (10+x*width/row, 10+y *
                                  height / column), ((x + 1) * width / row - 10, (y + 1) * height / column - 10), 5)
    pygame.draw.line(win, color, (10 + x * width / row, (y + 1) * height /
                                  column - 10), ((x + 1) * width / row - 10, 10 + y * height / column), 5)


def nought(y, x, color=white):
    pygame.draw.circle(win, color,
                       ((x+1)*100-50, (y+1) * 100-50), 45, 5)


def emptyPlaces():
    l = []
    for i in range(3):
        for j in range(3):
            if grid[i][j] == " ":
                l.append([i, j])
    return l


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


def isTie():
    for i in range(3):
        for j in range(3):
            if grid[i][j] == " ":
                return False
    return True


def minimaxPro(alpha, beta, isMaximizing):
    if isWinner(ai):
        return 1
    if isWinner(human):
        return - 1
    if isTie():
        return 0
    if isMaximizing:
        bestScore = -math.inf
        for child in emptyPlaces():
            grid[child[0]][child[1]] = ai
            score = minimaxPro(alpha, beta, False)
            grid[child[0]][child[1]] = " "
            bestScore = max(score, bestScore)
            alpha = max(alpha, score)
            if beta <= alpha:
                break
        return bestScore
    else:
        bestScore = math.inf
        for child in emptyPlaces():
            grid[child[0]][child[1]] = human
            score = minimaxPro(alpha, beta, True)
            grid[child[0]][child[1]] = " "
            bestScore = min(score, bestScore)
            beta = min(beta, score)
            if beta <= alpha:
                break
        return bestScore


def endPrint(text="TIE!"):
    global grid, turn
    pygame.display.update()
    time.sleep(0.5)
    msg = pygame.font.SysFont(None, 50).render(text, True, (255, 0, 0))
    win.fill((255, 255, 255))
    win.blit(msg, [100, 100])
    pygame.display.update()
    time.sleep(1)
    # pygame.quit()
    grid = [[" " for x in range(row)] for y in range(column)]
    # turn = random.choice([ai, human])
    turn = ai
    main(True)


def bestMove():
    global turn
    bestScore = -math.inf
    for i in range(3):
        for j in range(3):
            if grid[i][j] == " ":
                grid[i][j] = ai
                score = minimaxPro(-math.inf, math.inf, False)
                grid[i][j] = " "
                if score > bestScore:
                    bestScore = score
                    p = [i, j]
    grid[p[0]][p[1]] = turn
    cross(p[0], p[1])
    if isWinner(turn):
        endPrint("AI WIN!")
    elif isTie():
        endPrint()
    else:
        turn = opponent(turn)


def play(l):
    global turn
    if grid[l[0]][l[1]] == " ":
        grid[l[0]][l[1]] = turn
        printGrid()
        nought(l[0], l[1])
        if isWinner(turn):
            endPrint("YOU WIN!")
        elif isTie():
            endPrint()
        else:
            turn = opponent(turn)
            bestMove()


def main(run):
    win.fill((0, 0, 0))
    drawGrid(white, row, column)
    if turn == ai:
        bestMove()
    while run:
        pygame.time.delay(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and turn == human:
                mx, my = pygame.mouse.get_pos()
                play(convert(mx, my))
        pygame.display.update()


main(True)
