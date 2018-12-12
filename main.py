from graphics import *
import time
import random
import curses

#### CONSTANTS ###
sw = 5   # column separator width
bw = 75  # column width
bgColor = color_rgb(205, 193, 181)
sepColor = color_rgb(187, 173, 160)
textColor = 'white'
textStyle = 'normal'

# get the rows and columns
rows = int(input("How many rows do you want? >"))
cols = int(input("How many cols do you want? >"))

# create the window
gX = cols * ((sw-1) + bw)
gY = rows * ((sw-1) + bw)
win = GraphWin('Grid', gX, gY)
win.autoflush = True

# set up key inputs
screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)
screen.addstr(0, 0, "STAY CLICKED ON THIS WINDOW")
screen.addstr(1, 0, "TO QUIT, PRESS Q")
screen.addstr(2, 0, "")

# create the background
win.setBackground(bgColor)

"""########--------- LOGIC.PY ----------######"""

###---------- helper methods -------------###


# returns true if a given array is full of 0's or None's
def empty(arr):
    for i in range(0, len(arr)):
        if arr[i] != 0 and arr[i] != None:
            return False
    return True

# returns true if a given array has no zeros or None's
def full(arr):
    for c in range(0, len(arr)):
        if arr[c] == 0 or arr[c] == None:
            return False
    return True

# resets the value of alreadyMerged for each tile
def resetMerges():
    for r in range(len(tiles)):
        for tile in tiles[r]:
            if tile != None:
                tile.alreadyMerged = False

# prints tiles in a grid form
def printVals():
    result = ""
    for r in range(0, len(tiles)):
        for c in range(0, len(tiles[r])):
            if tiles[r][c] != None:
                result += str(tiles[r][c].num) + " "
            elif tiles[r][c] == None:
                result += "N "
            #else:
                #result += "N "
        result += "\n"
    print(result)


###---------- left direction -------------###

def allLeft(arr):
    count = 0
    for c in range(0, len(arr)):
        if arr[c] != None:
            count = count + 1
    if full(arr):
        return True
    elif firstLeftUnfilled(arr) == count:
        return True
    else:
        return False

def firstLeftUnfilled(arr):
    for c in range(0, len(arr)):
        if arr[c] == None:
            return c
    return -1

def closestOnLeft(arr, index):
    # counts down from index-1 to 0
    for c in range(index-1, -1, -1):
        if arr[c] != None:
            return c
    return -1

# returns the last index from the left that's consecutively filled with a non-zero
def rightMostFilled(arr):
    for c in range(0, len(arr)):
        if arr[c] == None:
            return c-1
    return -1


def leftKey():
    for r in range(0, len(tiles)):

        if (not empty(tiles[r])):

            # find the first non-null and move it to the first position
            for c in range(0, len(tiles[r])):
                if tiles[r][c] != None:
                    temp = tiles[r][c]
                    tiles[r][c] = None
                    tiles[r][0] = temp
                    break

            # ensures it's done at least once
            while True:
                for c in range(1, len(tiles[r])):
                    # check if it can merge left
                    cLi = closestOnLeft(tiles[r], c)
                    if tiles[r][c] != None and tiles[r][c].num == tiles[r][cLi].num and ((not tiles[r][c].alreadyMerged) and (not tiles[r][cLi].alreadyMerged)):
                        tiles[r][cLi].num = 2 * tiles[r][c].num
                        tiles[r][c] = None
                        tiles[r][cLi].alreadyMerged = True

                    # if not, just move it to the next available spot
                    else:
                        """ it's vital you do the rearrangement in this order, because if
                            you do tiles[r][c] = None at the end but the tile just stayed in its original
                            spot, you got rid of it when you shouldn't have """
                        temp = tiles[r][c]
                        tiles[r][c] = None
                        tiles[r][cLi+1] = temp
                if( allLeft(tiles[r])):
                    break

###------------- right direction ----------------###

# flips the matrix horizontally
# used to turn a rightKey() call into a leftKey() one
def flipLeftRight(matrix):
    newmat = [ [ 0 for c in range(len(matrix[r])) ] for r in range(len(matrix))]
    for r in range(len(matrix)):
        for c in range(len(matrix[r])):
            newmat[r][len(matrix[r])-c-1] = matrix[r][c]
    return newmat

def rightKey():
    global tiles

    # just flip the matrix horizontally, do the leftKey() op then flip it back
    tiles = flipLeftRight(tiles)
    leftKey()
    tiles = flipLeftRight(tiles)


###------------ up direction -----------------###

# for every element at row m, column n - moves it to row n, column m
# used to turn the upKey() call into a leftKey() one
def transpose(matrix):
    newmat = [ [0 for c in range(len(matrix))] for r in range(len(matrix[0]))]
    for r in range(len(matrix)):
        for c in range(len(matrix[r])):
            newmat[c][r] = matrix[r][c]
    return newmat

def upKey():
    global tiles

    tiles = transpose(tiles)
    leftKey()
    tiles = transpose(tiles)

###----------- down direction ------------###
def downKey():
    global tiles

    tiles = transpose(tiles)
    tiles = flipLeftRight(tiles)
    leftKey()
    tiles = flipLeftRight(tiles)
    tiles = transpose(tiles)



class Tile:
    def __init__(self, num):
        self.num = num
        self.alreadyMerged = False

""" #################
        ACTUAL
        FILE
    #################
   """

def drawSeparators():
    # draw column separators
    for c in range(0, cols-1):
        xstart = (bw * (c+1) + sw * c)
        xend = xstart + sw
        p1 = Point(xstart, 0)
        p2 = Point(xend, gY)
        rect = Rectangle(p1, p2)
        rect.draw(win)
        rect.setOutline(sepColor)
        rect.setFill(sepColor)
    #draw row separators
    for r in range(0, rows-1):
        ystart = (bw * (r+1) + sw * r)
        yend = ystart + sw
        p1 = Point(0, ystart)
        p2 = Point(gX, yend)
        rect = Rectangle(p1, p2)
        rect.draw(win)
        rect.setOutline(sepColor)
        rect.setFill(sepColor)
drawSeparators()

# set up tiles
tiles = [ [None for c in range(cols)] for r in range(rows)]
rects = [ [None for c in range(cols)] for r in range(rows)]
newtile = [ [False for c in range(cols)] for r in range(rows)]


def spawnRandom():
    global newtile

    randr = random.randint(0, rows-1)
    while(full(tiles[randr])):
        randr = random.randint(0, rows-1)

    randc = random.randint(0, cols-1)
    while(tiles[randr][randc] != None):
        randc = random.randint(0, cols-1)


    # generate two random numbers 1 through 10
    rand1 = random.randint(1, 10)
    rand2 = random.randint(1, 10)

    # if they're equal, make it a 4 --- since there's a 10% chance of the new tile being a 4
    if rand1 == rand2:
        n = 4
    else:
        n = 2

    tiles[randr][randc] = Tile(n)
    newtile = [ [False for c in range(cols)] for r in range(rows)]
    newtile[randr][randc] = True

def boardFull():
    for row in tiles:
        for tile in row:
            if tile == None:
                return False
    return True

# returns true if no more moves can be made (hint: finding one false should return false, hence why we just "pass" for ones that should be return True)
#currently, itt won't work if the board has 1 row or 1 col
def checkLose():
    if boardFull():
        for r in range(len(tiles)):
            for c in range(len(tiles[r])):
                n = tiles[r][c].num

                if r == 0:
                    if c == 0 and n!=tiles[r][c+1].num and n!=tiles[r+1][c].num:
                        pass
                    elif c == len(tiles[r])-1 and n!=tiles[r][c-1].num and n!=tiles[r+1][c].num:
                        pass
                    elif c != 0 and c != len(tiles[r])-1 and n!=tiles[r][c-1].num and n!=tiles[r][c+1].num and n!=tiles[r+1][c].num:
                        pass
                    else:
                        return False
                elif r == len(tiles)-1:
                    if c == 0 and n!=tiles[r][c+1].num and n!=tiles[r-1][c].num:
                        pass
                    elif c == len(tiles[r])-1 and n!=tiles[r][c-1].num and n!=tiles[r-1][c].num:
                        pass
                    elif c!=0 and c!=len(tiles[r])-1 and n!=tiles[r][c-1].num and n!=tiles[r][c+1].num and n!=tiles[r-1][c].num:
                        pass
                    else:
                        return False
                elif c == 0:
                    if n!=tiles[r+1][c].num and n!=tiles[r-1][c].num and n!=tiles[r][c+1].num:
                        pass
                    else:
                        return False
                elif c == len(tiles[r])-1:
                    if n!=tiles[r+1][c].num and n!=tiles[r-1][c].num and n!=tiles[r][c-1].num:
                        pass
                    else:
                        return False
                else:
                    if n!=tiles[r+1][c].num and n!=tiles[r-1][c].num and n!=tiles[r][c+1].num and n!=tiles[r][c-1].num:
                        pass
                    else:
                        return False
        return True

    else:
        return False

# returns if a given index has changed value in tiles
def changedInTiles(r, c):
    global tilescopy
    if tilescopy[r][c] == None and tiles[r][c] == None:
        return False
    elif tilescopy[r][c] == None or tiles[r][c] == None:
        return True
    elif tilescopy[r][c].num != tiles[r][c].num:
        return True
    else:
        return False

#maybe it would be good to have an array of all the rectangle objects...
#bc you can move them and then let the screen update // undraw if necessary
"""You have to do something for everything in the window. However because GraphWin is a subclass of a Tkinter.canvas widget it means it has find_all() and delete() methods since GraphWin doesn't override them (from looking at the source for the module). The former will return a list of all the object ID numbers on the canvas. You can then iterate through these numbers in the list and call the delete() method on each one."""
outline = Rectangle(Point(0, 0), Point(0, 0))
outline.draw(win)
def drawUpdate():
    global outline
    outline.undraw()

    win.autoflush = False
    # there is also an undraw() method
    # or what if instead of going through every object, you have a dictionary of each tile and then it's (r, c) - then just loop through that

    for r in range (len(tiles)):
        for c in range(len(tiles[r])):
            global newtile

            # set the coordinates
            xstart = (bw + sw) * c
            xend = xstart + bw
            ystart = (bw + sw) * r
            yend = ystart + bw


            # midpoint coordinates
            xm = int((xend - xstart) / 2) + xstart
            ym = int((yend - ystart) / 2) + ystart

            # if the tile has changed, update it
            if changedInTiles(r, c) or newtile[r][c]:
                # undraw everything that's changed
                if rects[r][c] != None:
                    rects[r][c].undraw()


                #update the rects array and draw

                # any nones, undraw what was there and update rects
                if tiles[r][c] == None:
                    if rects[r][c] != None:
                        rects[r][c].undraw()
                        rects[r][c] = None
                #any new tiles, animate them
                elif newtile[r][c]:
                    rects[r][c] = Image(Point(xm, ym), "images/"+str(tiles[r][c].num)+"tile.png")
                    rects[r][c].draw(win)

                    outline = Rectangle(Point(xstart-2, ystart-2), Point(xend+2, yend+2))
                    outline.draw(win)
                    outline.setOutline('red')

                else:
                    rects[r][c] = Image(Point(xm, ym), "images/"+str(tiles[r][c].num)+"tile.png")
                    rects[r][c].draw(win)




    win.update()
    win.autoflush = True

def drawInit():
    win.autoflush = False
    # there is also an undraw() method
    # or what if instead of going through every object, you have a dictionary of each tile and then it's (r, c) - then just loop through that
    for r in range (len(tiles)):
        for c in range(len(tiles[r])):
            if tiles[r][c] != None:

                # set the coordinates
                xstart = (bw + sw) * c
                xend = xstart + bw
                ystart = (bw + sw) * r
                yend = ystart + bw

                # midpoint coordinates
                xm = int((xend - xstart) / 2) + xstart
                ym = int((yend - ystart) / 2) + ystart

                rects[r][c] = Image(Point(xm, ym), "images/"+str(tiles[r][c].num)+"tile.png")
                rects[r][c].draw(win)


    win.update()
    win.autoflush = True

# returns a copy of the tiles array
def copyTiles():
    copy = [ [None for c in range(len(tiles[0]))] for r in range(len(tiles))]
    for r in range(len(tiles)):
        for c in range(len(tiles[r])):
            if tiles[r][c] != None:
                copy[r][c] = Tile(tiles[r][c].num)
            else:
                copy[r][c] = None
    return copy

# checks if a certain matrix of Tile objects is equal to the tiles matrix
def equalToTiles(matrix):
    for r in range(len(tiles)):
        for c in range(len(tiles[r])):
            if matrix[r][c] == None and tiles[r][c] == None:
                pass
            elif matrix[r][c] == None or tiles[r][c] == None:
                return False
            elif matrix[r][c].num != tiles[r][c].num:
                return False
    return True

### MAIN GAMEPLAY METHOD
def main():
    global tilescopy
    tilescopy = copyTiles()

    spawnRandom()
    spawnRandom()
    drawInit()
    # while notlost

    count = 0
    # wait until you get a key press
    while True:
        if checkLose():
            break


        char = screen.getch() #get their input (if you want to print it, use screen.addstr(0, 0, 'text') cause print doesn't work w this)

        # once you get an arrow key
        if char == curses.KEY_RIGHT or char == curses.KEY_LEFT or char == curses.KEY_UP or char == curses.KEY_DOWN:
            resetMerges()
            tilescopy = copyTiles()

        # quit key
        if char == ord('q'):
            curses.nocbreak(); screen.keypad(0); curses.echo()
            curses.endwin()
            break

        # checks for right arrow key
        elif char == curses.KEY_RIGHT:
            oldtiles = copyTiles()
            rightKey()
            if not equalToTiles(oldtiles):
                spawnRandom()
                drawUpdate()

        # checks for left arrow key
        elif char == curses.KEY_LEFT:
            oldtiles = copyTiles()
            leftKey()
            if not equalToTiles(oldtiles):
                spawnRandom()
                drawUpdate()

        # checks for up arrow key
        elif char == curses.KEY_UP:
            oldtiles = copyTiles()
            upKey()
            if not equalToTiles(oldtiles):
                spawnRandom()
                drawUpdate()

        # checks for down arrow key
        elif char == curses.KEY_DOWN:
            oldtiles = copyTiles()
            downKey()
            if not equalToTiles(oldtiles):
                spawnRandom()
                drawUpdate()

    # end the game
    screen.nodelay(True) #makes getch not blocking
    while True:
        if screen.getch() == ord('q'):
            curses.nocbreak(); screen.keypad(0); curses.echo()
            curses.endwin()
            break
        else:
            drawEnd()


# flashes "You lose"
def drawEnd():
    value3 = Text(Point(gX/2, gY/2), 'YOU LOSE!')
    value3.setFill('black')
    value3.setStyle('bold')
    value3.setSize(27)
    value3.draw(win)
    time.sleep(0.2)
    value3.undraw()
    time.sleep(0.2)

# method to have the computer play for you
def machineMain():
    global tilescopy

    tilescopy = copyTiles()
    spawnRandom()
    spawnRandom()
    drawInit()

    while True:
        resetMerges()
        tilescopy = copyTiles()

        if checkLose():
            break

        oldtiles = copyTiles()
        rightKey()
        if equalToTiles(oldtiles):
            downKey()
            if equalToTiles(oldtiles):
                leftKey()
                if equalToTiles(oldtiles):
                    upKey()
                    drawUpdate()
                else:
                    spawnRandom()
                    drawUpdate()
            else:
                spawnRandom()
                drawUpdate()
        else:
            spawnRandom()
            drawUpdate()

# end the game
    screen.nodelay(True) #makes getch not blocking
    while True:
        if screen.getch() == ord('q'):
            curses.nocbreak(); screen.keypad(0); curses.echo()
            curses.endwin()
            break
        else:
            drawEnd()

main()
