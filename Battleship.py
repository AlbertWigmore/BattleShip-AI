'''
    @ Albert Wigmore
    @ Starter Code By Harris Christiansen (Harris@purduecs.com)
    2016-01-28
    For: Purdue Hackers - Battleship
    Battleship Client
'''

import sys
import socket
import time
import random

API_KEY = "747910169" ########## PUT YOUR API KEY HERE ##########

GAME_SERVER = "battleshipgs.purduehackers.com"

##############################  PUT YOUR CODE HERE ##############################

let = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']  # This is here for reasons unexplained
letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
grid = [[-1 for x in range(8)] for x in range(8)] # Fill Grid With -1s

# -1 no move made
# 1 hit square
# 0 miss


def placeShips(opponentID):
    global grid
    # Fill Grid With -1s
    grid = [[-1 for x in range(8)] for x in range(8)] # Fill Grid With -1s
    mode = random.randrange(0, 2)
    # Place Ships
    if mode == 0:
        placeDestroyer("A6", "A7")  # Ship Length = 2
        placeSubmarine("H2", "H4")  # Ship Length = 3
        placeCruiser("B2", "B4")  # Ship Length = 3
        placeBattleship("E4", "E7")  # Ship Length = 4
        placeCarrier("B0", "F0")  # Ship Length = 5

    if mode == 1:
        placeDestroyer("G7", "H7")  # Ship Length = 2
        placeSubmarine("D3", "F3")  # Ship Length = 3
        placeCruiser("C6", "E6")  # Ship Length = 3
        placeBattleship("H0", "H3")  # Ship Length = 4
        placeCarrier("B0", "B4")  # Ship Length = 5


ships = [2, 3, 3, 4, 5]
orient = [1, 2]


# Find max value in probabilty density grid
def find_max(pdf_grid):
    max = 0
    for x in range(0, 8):  # Loop Till Find Square that has not been hit
        for y in range(0, 8):
            if pdf_grid[x][y] > max:
                max = pdf_grid[x][y]
                i = x
                j = y
    return i, j


# Function to check for hit and add to the probability density grid for a possible hit
def check_hit(pdf):
    for i in range(8):
        for j in range(8):
            if grid[i][j] == 1:
                try:
                    if grid[i+1][j] == -1:
                        pdf[i+1][j] += 5
                    if grid[i][j-1] == -1:
                        pdf[i][j-1] += 5
                    if grid[i-1][j] == -1:
                        pdf[i-1][j] += 5
                    if grid[i][j+1] == -1:
                        pdf[i][j+1] += 5
                    else:
                        size = 0
                        direction = None
                        # Never got this function working correctly, which is sad
                        # check_sunk(i, j, size, direction)
                except IndexError:
                    pass


# Function that very badly works out if ships are sunk, it's also recursive
# Oh and this function doesn't actually work in its current state
def check_sunk(i, j, size, direction):
    if direction == None:
        try:
            if grid[i+1][j] == 1:
                check_sunk(i + 1, j, size, 'right')
                size += 1
            if grid[i][j-1] == 1:
                check_sunk(i, j - 1, size, 'down')
                size += 1
            if grid[i-1][j] == 1:
                check_sunk(i - 1, j, size, 'left')
                size += 1
            if grid[i][j+1] == 1:
                check_sunk(i, j + 1, size, 'up')
                size += 1
            else:
                try:  # Horrendous method don't even look at this, it's broken
                    print(size)
                    if size == 6:
                        ships.remove(3)
                        ships.remove(3)
                    if size == 7:
                        ships.remove(5)
                        ships.remove(2)
                    if size == 8:
                        ships.remove(3)
                        ships.remove(3)
                        ships.remove(2)
                    if size == 10 and (4 not in ships):
                        ships.remove(5)
                        ships.remove(3)
                        ships.remove(2)
                    if size == 10 and (5 not in ships):
                        ships.remove(4)
                        ships.remove(4)
                        ships.remove(2)
                    if ((3 not in ships) and (2 not in ships)) and size == 5:
                        ships.remove(5)
                    if size == 5 and ((3 in ships) and (2 in ships)) and (5 not in ships):
                        ships.remove(3)
                        ships.remove(2)
                    if size == 11:
                        ships.remove(5)
                        ships.remove(4)
                        ships.remove(2)
                    if size == 11:
                        ships.remove(5)
                        ships.remove(4)
                        ships.remove(3)
                    if size == 13:
                        ships.remove(5)
                        ships.remove(3)
                        ships.remove(3)
                        ships.remove(2)
                except:
                    pass
        except ValueError:
            pass
        except IndexError:
            pass
    if direction == 'left':
        try:
            if grid[i-1][j] == 1:
                size += 1
                check_sunk(i - 1, j, size, 'left')
        except IndexError:
            pass
    if direction == 'right':
        try:
            if grid[i+1][j] == 1:
                size += 1
                check_sunk(i + 1, j, size, 'right')
        except IndexError:
            pass
    if direction == 'down':
        try:

            if grid[i][j-1] == 1:
                size += 1
                check_sunk(i, j - 1, size, 'down')
        except IndexError:
            pass
    if direction == 'up':
        try:
            if grid[i][j+1] == 1:
                size += 1
                check_sunk(i, j + 1, size, 'up')
        except IndexError:
            pass


# Create the probability density function grid
def makeMove():
    pdf = [[0 for x in range(8)] for x in range(8)]
    global grid
    for ship in ships:
        for i in range(8):
            for j in range(8):
                for orientation in orient:
                    if orientation == 1:  # Horizontal
                        try:
                            for length in range(0, ship):
                                if grid[i+length][j] == 0 or grid[i+length][j] == 2:
                                    raise IndexError

                            for length in range(0, ship):
                                if grid[i+length][j] == -1:
                                    pdf[i+length][j] += 1

                        except IndexError:
                            pass
                    if orientation == 2:  # Vertical
                        try:
                            for length in range(0, ship):
                                if grid[i][j+length] == 0 or grid[i][j+length] == 2:
                                    raise IndexError

                            for length in range(0, ship):
                                if grid[i][j+length] == -1:
                                    pdf[i][j+length] += 1

                        except IndexError:
                            pass
    check_hit(pdf)
    x, y = find_max(pdf)
    wasHitSunkOrMiss = placeMove(letters[x]+str(y)) # placeMove(LetterNumber) - Example: placeMove(D5)
    if wasHitSunkOrMiss == "Hit":
        grid[x][y] = 1
    elif wasHitSunkOrMiss == "Sunk":
        grid[x][y] = 1
    else:
        grid[x][y] = 0
    return


############################## ^^^^^ PUT YOUR CODE ABOVE HERE ^^^^^ ##############################


def sendMsg(msg):
    global s
    try:
        s.send(msg)
    except:
        s = None


def connectToServer():
    global s
    invalidKey = False
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((GAME_SERVER, 23345))

        sendMsg(API_KEY)
        data = s.recv(1024)

        if("False" in data):
            s = None
            print "Invalid API_KEY"
            invalidKey = True
    except:
        s = None

    if invalidKey:
        sys.exit()


destroyer=submarine=cruiser=battleship=carrier=("A0","A0")
dataPassthrough = None


def gameMain():
    global s, dataPassthrough, moveMade
    while True:
        if(dataPassthrough == None):
            if s == None:
                return
            data = s.recv(1024)
        else:
            data = dataPassthrough
            dataPassthrough = None

        if not data:
            s.close()
            return
        
        if "Welcome" in data: # "Welcome To Battleship! You Are Playing:xxxx"
            welcomeMsg = data.split(":")
            placeShips(welcomeMsg[1])
            if "Destroyer" in data: # Only Place Can Receive Double Message, Pass Through
                dataPassthrough = "Destroyer(2):"
        elif "Destroyer" in data: # Destroyer(2)
            sendMsg(destroyer[0])
            sendMsg(destroyer[1])
        elif "Submarine" in data: # Submarine(3)
            sendMsg(submarine[0])
            sendMsg(submarine[1])
        elif "Cruiser" in data: # Cruiser(3)
            sendMsg(cruiser[0])
            sendMsg(cruiser[1])
        elif "Battleship" in data: # Battleship (4)
            sendMsg(battleship[0])
            sendMsg(battleship[1])
        elif "Carrier" in data: # Carrier(3)
            sendMsg(carrier[0])
            sendMsg(carrier[1])
        elif "Enter" in data: # Enter Coordinates
            moveMade = False
            makeMove()
        elif "Error" in data: # Error: xxx
            print("Received Error: "+data)
            sys.exit()
        elif "Hit" in data or "Miss" in data or "Sunk" in data:
            print("Error: Please Make Only 1 Move Per Turn.")
            sys.exit()
        elif "Die" in data:
            print("Error: Your client was disconnected using the Game Viewer.")
            sys.exit()
        else:
            print("Received Unknown Response: "+data)
            sys.exit()


def placeDestroyer(startPos, endPos):
    global destroyer
    destroyer = (startPos.upper(), endPos.upper())


def placeSubmarine(startPos, endPos):
    global submarine
    submarine = (startPos.upper(), endPos.upper())


def placeCruiser(startPos, endPos):
    global cruiser
    cruiser = (startPos.upper(), endPos.upper())


def placeBattleship(startPos, endPos):
    global battleship
    battleship = (startPos.upper(), endPos.upper())


def placeCarrier(startPos, endPos):
    global carrier
    carrier = (startPos.upper(), endPos.upper())


def placeMove(pos):
    global dataPassthrough, moveMade
    if moveMade: # Only Make 1 Move Per Turn
        print("Error: Your client was disconnected using the GameViewer")
        sys.exit()

    moveMade = True
    sendMsg(pos)
    data = s.recv(1024)
    if "Hit" in data:
        return "Hit"
    elif "Sunk" in data:
        return "Sunk"
    elif "Miss" in data:
        return "Miss"
    else:
        dataPassthrough = data
        return "Miss"

while True:
    connectToServer()
    if s != None:
        try:
            gameMain()
        except socket.error, msg:
            None
    time.sleep(1)
