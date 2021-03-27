# Snake Game
I created this game to demonstrate the use of threading in Python. I created a daemon thread to take the keystrokes from user while the game is running in main thread.
Some features of this game:
* Dynamic board size
* Five difficulty levels
* Two game modes
    * Classic mode
    * Constrained mode


# Demo
## Windows
![Windows](https://github.com/JameelKaisar/Snake-Game/blob/main/Images/Windows.png?raw=true)

## Ubuntu
![Ubuntu](https://github.com/JameelKaisar/Snake-Game/blob/main/Images/Ubuntu.png?raw=true)

## Kali Linux
![Kali Linux](https://github.com/JameelKaisar/Snake-Game/blob/main/Images/Kali%20Linux.png?raw=true)

## Tails OS
![Tails OS](https://github.com/JameelKaisar/Snake-Game/blob/main/Images/Tails%20OS.png?raw=true)


# Code
## User Comments
```python
# Snake Game by Jameel
# March 25, 2021
```

I created this game on March 25, 2021 during my semester break.

## Importing Libraries
```python
from os import name, system
from random import randint
from time import sleep
import threading
```

* **name** is imported to get the information about operating system.
* **system** is imported to clear game screen before printing the updated game screen.
* **randint** is imported to place food randomly.
* **sleep** is imported to control speed of snake.
* **threading** is imported to create a separate thread for taking keystrokes while main thread is running.

## Defining Function to Clear Screen
```python
if name == "nt":
    # Windows
    clear = lambda: system('cls')
else:
    # POSIX Systems
    clear = lambda: system('clear')
```

This function clears the screen and will work on all major operating systems. Remember **os.name** is **"nt"** for Windows and **"posix"** for Mac/Linux. You may use only the function specific to your OS.
* For Mac/Linux, use "*clear = lambda: system('clear')*" and "*clear()*"
* For Windows, use "*clear = lambda: system('cls')*" and "*clear()*"

## Defining Function to Handle Keystrokes
```python
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
```

Handling keystrokes does not come out of the box with Python. There are different modules for getting keystrokes depending on the OS. This function will handle keystrokes on all major operating systems. However, this function may behave unexpectedly in some situations. This function imports **msvcrt** on Windows and **sys**, **termios** and **tty** on POSIX systems. This function will throw an *ImportError* if required modules are not found (*ModuleNotFoundError*).
* For Windows, you can simply use "*from msvcrt import getch*"

## Defining Function to Print Game Screen
```python
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
```
  
This function takes **board**, **snake**, **food** and **score** as parameters and prints game screen. The game screen elements are printed using the following characters:
* **#** is used for Border
* **O** is used for Snake Head
* **0** is used for Snake Body
* **+** is used for Normal Food
* **\*** is used for Bonus Food
  
## Defining Function to Take Keystrokes
```python
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
```

This function appends keystrokes to global list **drn**. The value of arrow keys returned from **getch()** depends on the operating system. This function will work on Windows and POSIX systems. I used the following codes to represent directions:
* **1** is used to represent *Right* direction
* **-1** is used to represent *Left* direction
* **2** is used to represent *Up* direction
* **-2** is used to represent *Down* direction

## Defining Function to Get Next Position of Snake Head
```python
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
```

This function takes **board**, **snake**, **drn** and **classic** as parameters and returns next position of snake head as tuple. Value of next position of snake head depends on the size of game board, position of snake, keystrokes of user and mode of game.

## Defining Function to Append Next Position to Snake
```python
def append_snake(snake, nxt):
    snake.append(nxt)
    return snake
```

This function takes **snake** and **nxt** as parameters, appends next position to snake and returns it.

## Defining Function to Check Status of Food
```python
def check_food(board, snake, food, score):
    if food != snake[-1]:
        snake.pop(0)
        return snake, food, score
    while 1:
        food = (randint(1, board), randint(1, board))
        if food not in snake:
            return snake, food, score + ( 5 if score != 0 and score%5 == 0 and score%10 != 0 else 1)
```

This function takes **board**, **snake**, **food** and **score** as parameters and updates the values of snake, food and score and returns them.
* If snake head is not at the position of food, this function removes the tail position of snake.
* If snake head is at the position of food, it generates a new position for food using *randint()* and updates the value of score.
* 1 is added to score for normal food and 5 is added for bonus food.
* Bonus food is available after every 5 normal foods.

## Defining Function to Check Status of Game
```python
def check_play(board, snake, classic):
    if snake[-1] in snake[:-1]:
        return False
    elif (not classic) and (snake[-1][0] in [0, board+1] or snake[-1][1] in [0, board+1]):
        return False
    return True
```

This function takes **board**, **snake** and **classic** as parameters and checks if the snake has touched its body and also checks if the snake has touched border in case of constrained mode. If either of the two conditions is satisfied, the function returns *False*. Otherwise, the function returns *True*.

## Main Function
### Taking Input from User
```python
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
```

This block takes value of board from user. The value of board determines the size of game screen. Minimum value of board is 5 and recommended value is 10. For value of board = **N**, the size of game screen will be **NxN**. The screen is cleared after receiving correct input.

```python
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
```

This block takes value of difficulty level from user. Difficulty level corresponds to the speed of snake. Greater the difficulty level, greater will be the speed of snake. Difficulty level has no effect on score because the advantage for lesser difficulty levels is compensated by the additional time it takes to reach the same score as compared to the higher difficulty levels. Value of difficulty ranges from 1 to 5 and the screen is cleared after receiving correct input.


```python
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
```

This block takes input from user and defines game mode accordingly. This game has two modes:
* **Classic Mode**: Crossing border is allowed in this mode.
* **Constrained Mode**: Crossing border is **not** allowed in this mode.

### Declaring Game Variables
```python
snake = [(3, 2), (3, 3), (3, 4)]
drn = [1]
score = 0
nxt = ()
play = True
```

The main variables are declared in this block.
* **snake:** *list of tuples* This stores the position of snake.
* **drn:** *list* This stores the keystrokes of user.
* **score:** *int* This stores the score of user.
* **nxt:** *tuple* This stores next position of snake head.
* **play:** *bool* This stores status of game.

### Declaring Variable for Food
```python
while 1:
    food = (randint(1, board), randint(1, board))
    if food not in snake:
        break
```

This block declares variable for storing the position of food and initializes it to a random position.
* **food:** *int* This stores the position of food.

### Creating Daemon Thread for taking Keystrokes
```python
key_thread = threading.Thread(target=get_drn)
key_thread.daemon = True
key_thread.start()
```

We create a separate thread to take the keystrokes from user because we can't take keystrokes efficiently while running the game in same thread.
* First line creates a new thread named **key_thread** and sets target function to **get_drn()**. We do not pass any arguments. If needed, we can pass arguments as tuple using *args=( )*.
* Second line sets **key_thread** as daemon thread which means this thread is killed when the main thread finishes execution. Non-daemon threads continue running even after main thread finishes execution. In this case we don't need to take keystrokes after the game is over (i.e., after the main thread finishes execution), that's why we set **key_thread** as daemon thread.
* Third line starts the **key_thread** which runs the **get_drn()** function in secondary thread.

### Starting the Game
```python
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
```

This is the main block of this game. This block executes repetitively until the value of **play** becomes **False**. This block repeats the following steps:
* Clears the screen.
* Prints the updated game screen.
* Waits for some time, depending on the difficulty level chosen by user.
* Removes the first element of **drn** if it has two or more elements. This is important to change the direction of snake.
* Gets the next position of snake head.
* Appends the next position to snake.
* Checks the position of snake head and food and updates the values of food and score accordingly.
* Checks if game is over or not.

### Printing the Final Score
```python
print("\nGame Over! You Scored " + str(score) + " Point" + ("" if score == 1 else "s") + " in " + ("Classic" if classic else "Constrained") + " Mode!")
sleep(3)
```

This block is executed when the game is over. It prints the final score and waits for 3 second and then exits the program. Remember **sleep(3)** is the last statement in main program and when it finishes execution the main thread completes and the daemon thread **key_thread** is killed. It is not recommended to use **input()** instead of **sleep(3)** in this particular case.


# Full Code
```python
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
key_thread.daemon = True
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
```

# Operating Systems
This game is tested and is working on the following Operating Systems:
* Windows
* Ubuntu
* Kali Linux
* Tails OS
