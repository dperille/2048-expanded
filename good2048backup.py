from graphics import *
import time

#### CONSTANTS ###
sw = 5   # column separator width
bw = 75  # column width

# get the rows and columns
rows = int(input("How many rows do you want? >"))
cols = int(input("How many cols do you want? >"))

# create the window
gX = cols * (sw + (bw-1)) - 5
gY = rows * (sw + (bw-1)) - 5
win = GraphWin('Grid', gX, gY)

# create the background
bgColor = 'brown'
rect = Rectangle(Point(0, 0), Point(gX-1, gY-1))
rect.draw(win)
rect.setOutline(bgColor)
rect.setFill(bgColor)

# draw column separators
for c in range(0, cols-1):
    xstart = (bw * (c+1) + sw * c)
    xend = xstart + sw
    p1 = Point(xstart, 0)
    p2 = Point(xend, gY)
    rect = Rectangle(p1, p2)
    rect.draw(win)
    rect.setFill('black')
#draw row separators
for r in range(0, rows-1):
    ystart = (bw * (r+1) + sw * r)
    yend = ystart + sw
    p1 = Point(0, ystart)
    p2 = Point(gX, yend)
    rect = Rectangle(p1, p2)
    rect.draw(win)
    rect.setFill('black')


class Tile:
    def __init__(self, num):
        self.num = num
        self.alreadyMerged = False

tiles = [ [None for c in range(cols)] for r in range(rows)]


###---------- helper methods -------------###

# returns the color for a certain number
def getColor(n):
    if n == 2:
        return 'yellow'
    elif n == 4:
        return 'red'
    elif n == 8:
        return 'blue'

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
        for tile in tiles:
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

def closestOnRight(arr, index):
    for c in range(index+1, len(arr)):
        if arr[c] != None:
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
            # filled is the index of the farthest column consecutively filled with a non-zero from the left
            filled = 0
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
    newmat = [ [0 for c in range(len(matrix[r]))] for r in range(len(matrix))]
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

###------------- actual gameplay / misc. ---------------###



tiles[0][0] = Tile(4)
tiles[0][1] = Tile(2)
tiles[0][5] = Tile(2)
tiles[0][2] = Tile(2)
tiles[0][3] = Tile(2)
tiles[0][4] = Tile(4)
tiles[1][0] = Tile(4)
tiles[2][0] = Tile(4)
tiles[3][0] = Tile(2)
tiles[4][0] = Tile(2)


win.getMouse()
printVals()
downKey()
rightKey()
printVals()
win.getMouse()
