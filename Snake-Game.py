# Snake Game by Jameel
# March 25, 2021


from os import name, system
from random import randint
from time import sleep
import threading


if name == "nt":
    # Windows
    clear = lambda: system('cls')
else:
    # POSIX Systems
    clear = lambda: system('clear')


def getch():
    try:
        # Windows (with msvcrt support)
        import msvcrt
        return msvcrt.getch()

    except ImportError:
        # POSIX Systems (with termios and tty support)
        import sys, termios, tty

        fd = sys.stdin.fileno()
        oldSettings = termios.tcgetattr(fd)

        try:
            tty.setcbreak(fd)
            get_char = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, oldSettings)

        return get_char


def print_map(board, snake, food, score):
    screen = ""
    for i in range(0, board+2):
        for j in range(0, board+2):
            if i in [0, board+1] or j in [0, board+1]:
                screen += "# "
            elif snake[-1] == (i, j):
                screen += "O "
            elif (i, j) in snake:
                screen += "0 "
            elif (i, j) == food:
                if score != 0 and score%5 == 0 and score%10 != 0:
                    screen += "* "
                else:
                    screen += "+ "
            else:
                screen += "  "
        screen += "\n"
    print(screen)
    print("Score: " + str(score))


def get_drn():
    global drn

    if name == "nt":
        # Windows
        while True:
            if ord(getch()) == 224:
                key = ord(getch())
                if key == 77 and drn[-1] != -1:
                    drn.append(1)
                elif key == 75 and drn[-1] != 1:
                    drn.append(-1)
                elif key == 72 and drn[-1] != -2:
                    drn.append(2)
                elif key == 80 and drn[-1] != 2:
                    drn.append(-2)
    else:
        # POSIX Systems
        while True:
            if ord(getch())==27 and ord(getch())==91:
                key = ord(getch())
                if key == 67 and drn[-1] != -1:
                    drn.append(1)
                elif key == 68 and drn[-1] != 1:
                    drn.append(-1)
                elif key == 65 and drn[-1] != -2:
                    drn.append(2)
                elif key == 66 and drn[-1] != 2:
                    drn.append(-2)



def get_nxt(board, snake, drn, classic):
    if drn[0] in [1, -1]:
        if classic and snake[-1][1] == board and drn[0] == 1:
            return (snake[-1][0], 1)
        elif classic and snake[-1][1] == 1 and drn[0] == -1:
            return (snake[-1][0], board)
        else:
            return (snake[-1][0], snake[-1][1]+drn[0])
    else:
        if classic and snake[-1][0] == 1 and drn[0] == 2:
            return (board, snake[-1][1])
        elif classic and snake[-1][0] == board and drn[0] == -2:
            return (1, snake[-1][1])
        else:
            return (snake[-1][0]-drn[0]/2, snake[-1][1])


def append_snake(snake, nxt):
    snake.append(nxt)
    return snake


def check_food(board, snake, food, score):
    if food != snake[-1]:
        snake.pop(0)
        return snake, food, score
    while 1:
        food = (randint(1, board), randint(1, board))
        if food not in snake:
            return snake, food, score + ( 5 if score != 0 and score%5 == 0 and score%10 != 0 else 1)


def check_play(board, snake, classic):
    if snake[-1] in snake[:-1]:
        return False
    elif (not classic) and (snake[-1][0] in [0, board+1] or snake[-1][1] in [0, board+1]):
        return False
    return True


clear()


# Minimum Value: 5, Recommended Value: 10
while 1:
    try:
        board = int(input("Enter Board Size (Recommended Size is 10): "))
        if board < 5:
            print("Minimum Board Size is 5!")
            continue
        break
    except:
        print("Invalid Input!")
clear()


# Range: 1 to 5
while 1:
    try:
        speed = int(input("Enter Difficulty Level (1 to 5): "))
        if speed < 1 or speed > 5:
            print("Enter Values Between 1 and 5!")
            continue
        break
    except:
        print("Invalid Input!")
clear()


# Classic or Constrained
while 1:
    try:
        game_mode = int(input("Choose Game Mode:\n1. Classic\n2. Constrained\nEnter Your Choice: "))
        if game_mode == 1:
            classic = True
            break
        elif game_mode == 2:
            classic = False
            break
        print("Enter 1 or 2")
    except:
        print("Invalid Input!")
clear()


snake = [(3, 2), (3, 3), (3, 4)]
drn = [1]
score = 0
nxt = ()
play = True


while 1:
    food = (randint(1, board), randint(1, board))
    if food not in snake:
        break


key_thread = threading.Thread(target=get_drn)
key_thread.setDaemon(True)
key_thread.start()


while play:
    clear()
    print_map(board, snake, food, score)
    sleep(0.5-(speed-1)*0.1)
    if len(drn) > 1:
        drn.pop(0)
    nxt = get_nxt(board, snake, drn, classic)
    snake = append_snake(snake, nxt)
    snake, food, score = check_food(board, snake, food, score)
    play = check_play(board, snake, classic)


print("\nGame Over! You Scored " + str(score) + " Point" + ("" if score == 1 else "s") + " in " + ("Classic" if classic else "Constrained") + " Mode!")
sleep(3)

