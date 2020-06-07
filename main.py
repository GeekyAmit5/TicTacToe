# This is a game called tic tac toe
# you can play with friend or AI


import math
import random
import pygame
import time


pygame.init()
pygame.display.set_caption("Tic Tac Toe")
pygame.display.set_icon(pygame.image.load("icon.png"))
win = pygame.display.set_mode((500, 500))
background = pygame.image.load("background.jpg")
board = pygame.image.load("board.png")
cross = pygame.image.load("cross.png")
nought = pygame.image.load("nought.png")
fps = pygame.time.Clock()
black = (0, 0, 0)
white = (255, 255, 255)
run = True

grid = [[" " for x in range(3)] for y in range(3)]
ai = "X"
human = "O"
turn = ai


def AI():
    global run
    win.blit(background, (0, 0))
    win.blit(board, (0, 0))
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                print("AI")
        pygame.display.update()
        fps.tick(5)


def difficulty():
    global run
    win.blit(background, (0, 0))
    cho = pygame.font.SysFont(
        None, 85).render("Choose Difficulty!", True, white)
    # win.blit(welcome_text, [55, 80])
    pygame.draw.rect(win, white, (60, 200, 300, 60))
    vsFriend = pygame.font.SysFont(
        None, 50).render("You VS Friend", True, black)
    win.blit(vsFriend, [75, 210])
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                AI()
        pygame.display.update()
        fps.tick(5)


def friend():
    global run
    win.blit(background, (0, 0))
    win.blit(board, (0, 0))
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                print("friend")
        pygame.display.update()
        fps.tick(5)


def main():
    global run
    win.blit(background, (0, 0))
    welcome_text = pygame.font.SysFont(
        None, 85).render("TIC TAC TOE!", True, white)
    win.blit(welcome_text, [55, 80])

    pygame.draw.rect(win, white, (60, 200, 300, 60))
    vsFriend = pygame.font.SysFont(
        None, 50).render("VS FRIEND", True, black)
    win.blit(vsFriend, [75, 210])

    pygame.draw.rect(win, white, (60, 300, 300, 60))
    vsAI = pygame.font.SysFont(
        None, 50).render("You VS AI", True, black)
    win.blit(vsAI, [85, 310])

    pygame.draw.rect(win, white, (60, 400, 300, 60))
    vsAI = pygame.font.SysFont(
        None, 50).render("EXIT!", True, black)
    win.blit(vsAI, [85, 410])

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if 60 <= mx <= 360 and 200 <= my <= 260:
                    friend()
                elif 60 <= mx <= 360 and 300 <= my <= 360:
                    difficulty()
        pygame.display.update()
        fps.tick(5)


main()


# def convert(x, y):
#     return [y * row // height, x * column // width]


# def opponent(turn):
#     if turn == ai:
#         return human
#     return ai


# def printGrid():
#     print("\n-------------")
#     for i in range(3):
#         print("|", end="")
#         for j in range(3):
#             print(" {} ".format(grid[i][j]), end="|")
#         print("\n-------------")
#     print()


# def emptyPlaces():
#     l = []
#     for i in range(3):
#         for j in range(3):
#             if grid[i][j] == " ":
#                 l.append([i, j])
#     return l


# def isWinner(turn):
#     for i in range(3):
#         for j in range(3):
#             if grid[i][j] != turn:
#                 break
#         else:
#             return True
#         for j in range(3):
#             if grid[j][i] != turn:
#                 break
#         else:
#             return True

#     for i in range(3):
#         if grid[i][i] != turn:
#             break
#     else:
#         return True

#     for i in range(3):
#         if grid[i][2 - i] != turn:
#             break
#     else:
#         return True
#     return False


# def isTie():
#     for i in range(3):
#         for j in range(3):
#             if grid[i][j] == " ":
#                 return False
#     return True


# def minimaxPro(alpha, beta, isMaximizing):
#     if isWinner(ai):
#         return 1
#     if isWinner(human):
#         return - 1
#     if isTie():
#         return 0
#     if isMaximizing:
#         bestScore = -math.inf
#         for child in emptyPlaces():
#             grid[child[0]][child[1]] = ai
#             score = minimaxPro(alpha, beta, False)
#             grid[child[0]][child[1]] = " "
#             bestScore = max(score, bestScore)
#             alpha = max(alpha, score)
#             if beta <= alpha:
#                 break
#         return bestScore
#     else:
#         bestScore = math.inf
#         for child in emptyPlaces():
#             grid[child[0]][child[1]] = human
#             score = minimaxPro(alpha, beta, True)
#             grid[child[0]][child[1]] = " "
#             bestScore = min(score, bestScore)
#             beta = min(beta, score)
#             if beta <= alpha:
#                 break
#         return bestScore


# def endPrint(text="TIE!"):
#     global grid, turn
#     pygame.display.update()
#     time.sleep(0.5)
#     msg = pygame.font.SysFont(None, 50).render(text, True, (255, 0, 0))
#     win.fill((255, 255, 255))
#     win.blit(msg, [100, 100])
#     pygame.display.update()
#     time.sleep(1)
#     # pygame.quit()
#     grid = [[" " for x in range(row)] for y in range(column)]
#     # turn = random.choice([ai, human])
#     turn = ai
#     main(True)


# def bestMove():
#     global turn
#     bestScore = -math.inf
#     for i in range(3):
#         for j in range(3):
#             if grid[i][j] == " ":
#                 grid[i][j] = ai
#                 score = minimaxPro(-math.inf, math.inf, False)
#                 grid[i][j] = " "
#                 if score > bestScore:
#                     bestScore = score
#                     p = [i, j]
#     grid[p[0]][p[1]] = turn
#     cross(p[0], p[1])
#     if isWinner(turn):
#         endPrint("AI WIN!")
#     elif isTie():
#         endPrint()
#     else:
#         turn = opponent(turn)


# def play(l):
#     global turn
#     if grid[l[0]][l[1]] == " ":
#         grid[l[0]][l[1]] = turn
#         printGrid()
#         nought(l[0], l[1])
#         if isWinner(turn):
#             endPrint("YOU WIN!")
#         elif isTie():
#             endPrint()
#         else:
#             turn = opponent(turn)
#             bestMove()


# grid = [[" " for x in range(3)] for y in range(3)]
# ai = "X"
# human = "O"
# winx, wino, tie = 0, 0, 0
# gameMode = 0
# exitCode = "1"
# while True:
#     gameMode = input(
#         "Press 0 for You vs AI\nPress 1 for Player X vs Player O\n")
#     if gameMode in ["0", "1"]:
#         gameMode = int(gameMode)
#         break
#     else:
#         print("Please enter a valid input")


# def isWinner(turn):
#     for i in range(3):
#         for j in range(3):
#             if grid[i][j] != turn:
#                 break
#         else:
#             return True
#         for j in range(3):
#             if grid[j][i] != turn:
#                 break
#         else:
#             return True

#     for i in range(3):
#         if grid[i][i] != turn:
#             break
#     else:
#         return True

#     for i in range(3):
#         if grid[i][2 - i] != turn:
#             break
#     else:
#         return True
#     return False


# def printGrid():
#     print("\n-------------")
#     for i in range(3):
#         print("|", end="")
#         for j in range(3):
#             print(" {} ".format(grid[i][j]), end="|")
#         print("\n-------------")
#     print()


# def opponent(turn):
#     if turn == ai:
#         return human
#     return ai


# def isTie():
#     for i in range(3):
#         for j in range(3):
#             if grid[i][j] == " ":
#                 return False
#     return True


# def emptyPlaces():
#     l = []
#     for i in range(3):
#         for j in range(3):
#             if grid[i][j] == " ":
#                 l.append([i, j])
#     return l


# def computer(turn, difficulty):
#     if difficulty > 0 or rd.randint(0, 3):
#         for i in range(3):
#             for j in range(3):
#                 if grid[i][j] == " " and isWin(grid, i, j, turn):
#                     return [i, j]

#     if difficulty > 0 or rd.randint(0, 2):
#         for i in range(3):
#             for j in range(3):
#                 if grid[i][j] == " " and isWin(grid, i, j, opponent(turn)):
#                     return [i, j]

#     if difficulty > 0:
#         if len(emptyPlaces()) == 9:
#             return [rd.choice([0, 2]), rd.choice([0, 2])]

#     if difficulty > 1 or rd.randint(0, difficulty):
#         if len(emptyPlaces()) == 8:
#             if grid[1][1] == opponent(turn):
#                 return [rd.choice([0, 2]), rd.choice([0, 2])]
#             else:
#                 return [1, 1]

#     if difficulty > 1 or rd.choice([0, 0, difficulty]):
#         if len(emptyPlaces()) == 7:
#             if grid[1][1] == opponent(turn):
#                 while True:
#                     i = rd.choice([0, 2])
#                     j = rd.choice([0, 2])
#                     if grid[2 - i][2 - j] == turn:
#                         return [i, j]
#             else:
#                 while True:
#                     i = rd.choice([0, 2])
#                     j = rd.choice([0, 2])
#                     if grid[i][j] == turn and (
#                             grid[i][abs(j - 1)] == opponent(turn) or grid[abs(i - 1)][j] == opponent(turn)):
#                         return [1, 1]
#                     if grid[2 - i][2 - j] == turn and (
#                             grid[2 - i][j] == opponent(turn) or grid[i][2 - j] == opponent(turn)):
#                         return [i, j]
#                     if grid[i][j] == " " and (grid[2 - i][j] == turn or grid[i][2 - j] == turn) and grid[i][
#                             abs(j - 1)] == grid[abs(i - 1)][j]:
#                         return [i, j]

#     if difficulty > 2 or rd.choice([0, 2 in range(difficulty)]):
#         if len(emptyPlaces()) == 6:
#             for i in range(3):
#                 for j in range(3):
#                     if grid[i][j] == opponent(turn) and grid[2 - i][2 - j] == opponent(turn) and isCorner(grid, i, j):
#                         return rd.choice([[0, 1], [2, 1], [1, 0], [1, 2]])
#                     if (grid[2 - i][j] == opponent(turn) or grid[i][2 - j] == opponent(turn)) and isCorner(grid, i, j) and (
#                             grid[i][abs(j - 1)] == opponent(turn) or grid[abs(i - 1)][j] == opponent(turn)):
#                         return [i, j]
#                     if (grid[2 - i][j] == turn or grid[i][2 - j] == turn) and isCorner(grid, i, j) and grid[1][
#                             1] == opponent(turn):
#                         return [i, j]
#                     if grid[1][1] == turn and grid[i][abs(j - 1)] == opponent(turn) and grid[abs(i - 1)][j] == opponent(turn):
#                         return [i, j]

#     if difficulty > 2 or rd.choice([0, 0, 2 in range(difficulty)]):
#         if len(emptyPlaces()) == 5:
#             while True:
#                 i = rd.choice([0, 2])
#                 j = rd.choice([0, 2])
#                 if grid[abs(i - 1)][j] == grid[i][abs(j - 1)] and grid[i][j] == " ":
#                     return [i, j]

#     if difficulty > 1 or rd.randint(0, difficulty):
#         for i in range(3):
#             for j in range(3):
#                 if isCorner(grid, i, j) and grid[i][j] == " ":
#                     while True:
#                         i = rd.choice([0, 2])
#                         j = rd.choice([0, 2])
#                         if grid[i][j] == " ":
#                             return [i, j]

#     if difficulty >= 0:
#         while True:
#             i = rd.randint(0, 2)
#             j = rd.randint(0, 2)
#             if grid[i][j] == " ":
#                 return [i, j]


# def isCorner(l, x, y):
#     if (x == y or x+y == 2) and x != 1:
#         return True
#     return False


# def isWin(grid, x, y, turn):
#     for i in range(3):
#         if y != i and grid[x][i] != turn:
#             break
#     else:
#         return True
#     for i in range(3):
#         if x != i and grid[i][y] != turn:
#             break
#     else:
#         return True
#     if x == y:
#         for i in range(3):
#             if grid[i][i] != turn and x != i:
#                 break
#         else:
#             return True
#     if x + y == 2:
#         for i in range(3):
#             if grid[i][2 - i] != turn and x != i:
#                 break
#         else:
#             return True
#     return False


# def minimaxPro(alpha, beta, isMaximizing):
#     if isWinner(ai):
#         return 1
#     if isWinner(human):
#         return - 1
#     if isTie():
#         return 0
#     if isMaximizing:
#         bestScore = -math.inf
#         for child in emptyPlaces():
#             grid[child[0]][child[1]] = ai
#             score = minimaxPro(alpha, beta, False)
#             grid[child[0]][child[1]] = " "
#             bestScore = max(score, bestScore)
#             alpha = max(alpha, score)
#             if beta <= alpha:
#                 break
#         return bestScore
#     else:
#         bestScore = math.inf
#         for child in emptyPlaces():
#             grid[child[0]][child[1]] = human
#             score = minimaxPro(alpha, beta, True)
#             grid[child[0]][child[1]] = " "
#             bestScore = min(score, bestScore)
#             beta = min(beta, score)
#             if beta <= alpha:
#                 break
#         return bestScore


# def scoreCard():
#     print("\nScore :")
#     if gameMode:
#         print("Player O : {}\nPlayer X : {}".format(wino, winx))
#     else:
#         if ai == "X":
#             print("You      : {}\nAI       : {}".format(wino, winx))
#         else:
#             print("You      : {}\nAI       : {}".format(winx, wino))
#     print("Tie      : {}".format(tie))


# def bestMove(difficulty):
#     if difficulty > 2 or rd.choice([0, 1, difficulty, difficulty == 2]):
#         bestScore = -math.inf
#         for i in range(3):
#             for j in range(3):
#                 if grid[i][j] == " ":
#                     grid[i][j] = ai
#                     score = minimaxPro(-math.inf, math.inf, False)
#                     grid[i][j] = " "
#                     if score > bestScore:
#                         bestScore = score
#                         play = i*10+j
#         return play
#     while True:
#         x = rd.randint(0, 2)
#         y = rd.randint(0, 2)
#         if grid[x][y] == " ":
#             return x*10+y


# def play(difficulty, turn):
#     global winx, wino, tie
#     while True:
#         while True:
#             if gameMode:
#                 print("Player {} : ".format(turn), end="")
#             else:
#                 if turn == human:
#                     print("You : ", end="")
#                 else:
#                     x = bestMove(difficulty)
#                     print("AI : {}".format(x))
#                     break
#             x = input()
#             if x.isnumeric():
#                 x = int(x)
#                 if [x//10, x % 10] in emptyPlaces():
#                     break
#                 else:
#                     print("Please enter a valid input!")
#             else:
#                 print("Please enter a valid input!")
#         grid[x//10][x % 10] = turn
#         printGrid()
#         if isWinner(turn):
#             if turn == "X":
#                 winx += 1
#             else:
#                 wino += 1
#             if gameMode:
#                 print("Player {} WON!".format(turn))
#             else:
#                 if turn == human:
#                     print("You WIN!")
#                 else:
#                     print("AI WIN!")
#             break
#         if isTie():
#             print("Match TIE!")
#             tie += 1
#             break
#         turn = opponent(turn)


# def main(difficulty=0, turn=rd.choice(["X", "O"])):
#     global gameMode, exitCode, winx, wino, tie
#     if exitCode == "2" or (exitCode == "1" and not gameMode):
#         wino, winx, tie, turn = 0, 0, 0, rd.choice(["X"])
#         while True:
#             difficulty = input(
#                 "\nPress 0 for Easy\nPress 1 for Medium\nPress 2 for Hard\nPress 3 for Expert\n")
#             if difficulty in ["0", "1", "2", "3"]:
#                 difficulty = int(difficulty)
#                 break
#             else:
#                 print("Please enter a valid input")
#     print("Start!")
#     printGrid()
#     play(difficulty, turn)
#     for i in range(3):
#         for j in range(3):
#             grid[i][j] = " "
#     scoreCard()
#     print("\nPress 0 to Exit!\nPress 1 to change Game Mode")
#     if not gameMode:
#         print("Press 2 to change Difficulty")
#     print("Press any other key to Continue!")
#     exitCode = input()
#     if exitCode == "0":
#         quit()
#     if exitCode == "1":
#         wino, winx, tie, turn = 0, 0, 0, rd.choice(["X", "O"])
#         print("\nGame Mode Changed to ", end="")
#         if gameMode:
#             print("You vs AI")
#         else:
#             print("Player X vs Player O")
#         gameMode = 1 - gameMode
#     main(difficulty, opponent(turn))


# main()
