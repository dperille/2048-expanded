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

#prints out the array of values
def printVals():
    result = ""
    for r in range(0, len(vals)):
        for c in range(0, len(vals[r])):
            if vals[r][c] != 0:
                result += str(vals[r][c]) + " "
            elif vals[r][c] == 0:
                result += "N "
            #else:
                #result += "N "
        result += "\n"
    print(result)
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

# set up tiles as a 2D array of Tile objects
tiles = []
vals = []
for r in range(0, rows):
    t1 = []
    a2 = []
    for c in range(0, cols):
        t1.append(None)
        a2.append(0)
    tiles.append(t1)
    vals.append(a2)

class Tile:
    def __init__(self, r, c, num):
        self.r = r
        self.c = c
        self.num = num
        self.alreadyMerged = false
        self.rect = Rectangle(Point( (bw+sw)*c, (bw+sw)*r ), Point((bw+sw)*c+bw, (bw+sw)*r+bw) )
        self.text = Text(Point((2*(bw+sw)*c+bw)/2, (2*(bw+sw)*r+bw)/2), str(num))
        self.color = getColor(num)
        self.rect.draw(win)
        self.rect.setFill(self.color)
        self.text.draw(win)
        self.text.setFill('blue')

    def moveTile(self, newc, newr):
        self.rect.move( (newc-self.c)*(bw+sw), (newr-self.r)*(bw+sw))
        self.text.move( (newc-self.c)*(bw+sw), (newr-self.r)*(bw+sw))
        self.r = newr
        self.c = newc

    def moveTilePixels(self, dx, dy):
        self.rect.move(dx, dy)

    def remove(self):
        self.r = -1
        self.c = -1
        self.rect.move(gX, gY)
        self.text.move(gX, gY)
        self.rect = None
        self.text = None

t1 = Tile(0, 2, 2)
tiles[t1.r][t1.c] = t1
t2 = Tile(0, 3, 2)
tiles[t2.r][t2.c] = t2

win.getMouse()

def getRidOfSpaces(arr):
    copy = arr
    while( not allLeft(copy)):
        for c in range(0, len(arr)-1):
            if copy[c] == None:
                for i in range(c, len(arr)-1):
                    copy[i] = copy[i+1]
                copy[len(arr)-1] = None
            elif copy[c] == 0:
                for i in range(c, len(arr)-1):
                    copy[i] = copy[i+1]
                copy[len(arr)-1] = 0
    return copy

def allLeft(arr):
    count = 0
    for c in range(0, len(arr)):
        if arr[c] != None and arr[c] != 0:
            count = count + 1
    if full(arr):
        return True
    elif firstLeftUnfilled(arr) == count:
        return True
    else:
        return False

def firstLeftUnfilled(arr):
    for c in range(0, len(arr)):
        if arr[c] == None or arr[c] == 0:
            return c
    return -1

def updateVals():
    for r in range(0, len(tiles)):
        for c in range(0, len(tiles[r])):
            if tiles[r][c] != None:
                vals[r][c] = tiles[r][c].num
            else:
                vals[r][c] = 0

# returns the index of the closest element on its right
def closestOnRight(arr, index):
    for c in range(index+1, len(arr)):
        if arr[c] != 0 and arr[c] != None:
            return c
    return -1
def closestOnLeft(arr, index):
    # counts down from index-1 to 0
    for c in range(index-1, -1, -1):
        if arr[c] != 0 and arr[c] != None:
            return c
    return -1

def leftKey1():
    updateVals()
    # figure out the ending position of everything, then move the
    # tiles as necessary

    # get rid of spaces in between everything
    for r in range(0, 1):
        row = vals[r]

        # set up colEndsUp, representing the column index each element goes to
        colEndsUp = [c for c in range(len(tiles[r]))]

        #updates colEndsUp
        for c in range(0, len(tiles[r])):
            count = 0
            for x in range(0, c):
                if tiles[r][x] == None:
                    count = count + 1
            colEndsUp[c] = colEndsUp[c] - count
        print(colEndsUp)

        # handle the merging
        """ 1) an idea: get rid of all spaces. then, go down the line FROM THE LEFT
        and if it equals the one to its right, double it and get rid of the one to its right
        then continue checking without closing up the hole left from that merge
        as long as there's space between blocks, iterate through from the left again until those holes are closed"""

        """ 2) or, what if you used a queue? if the front can't merge with the one on top of it, remove it
        and if two things merge, combine them and remove from the queue"""

        """ 3) or, do it graphically with no array representation - eg., if a "2" block collides (graphic
        check) with another 2, combine them into a 4"""

def leftKey3():
    # find the ones that move left for one space, then iterate through for a second, and so on ?
    # boolean array for every tile that can move left
    canMoveLeft = [ [] for x in range(len(tiles))]
    for i in range(len(tiles)):
        for c in range(len(tiles[r])):



win.getMouse()

""" this will animate the tile moving with f frames at f/t frames per second"""
""" moving c columns over, r columns down"""
"""
f = 7
t = .010
c = 4
r = 4
for i in range(0, f+1):
    tiles[0][0].moveTile(c*i/f, r*i/f)
    time.sleep(t)
tiles[1][1] = tiles[0][0]
tiles[0][0] = None
win.getMouse()
"""
