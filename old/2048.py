from graphics import *
import keyboard

#### CONSTANTS ###
sw = 5   # column separator width
bw = 75  # column width

# get the rows and columns
rows = int(input("How many rows do you want? >"))
cols = int(input("How many cols do you want? >"))

gX = cols * (sw + (bw-1)) - 5
gY = rows * (sw + (bw-1)) - 5
win = GraphWin('Grid', gX, gY)

# set the background color
bgColor = 'brown'
rect = Rectangle(Point(0, 0), Point(gX-1, gY-1))
rect.draw(win)
rect.setOutline(bgColor)
rect.setFill(bgColor)


"""
pt = Point(100, 50)
cir = Circle(pt, 25)
cir.draw(win)

all graphics objects (Point, Rectangle, Circle, etc.) require Point(s) as parameters

line.move(x, y) moves it right x pixels and down y pixels
"""

""" **** SETTINGS ****
- boxes are 75 pixels wide
- column and row separators are 5px wide
- row 0 is defined as the top row, column 0 is the left column
"""

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

######################## START ACTUAL GAMEPLAY PROGRAMMING #####################

def getColor(n):
    if n == 2:
        return 'yellow'
    elif n == 4:
        return 'red'
    elif n == 8:
        return 'blue'


tiles = [] #tracks the values in the game
rects = [] #tracks the drawing of the rectangles
values = [] #tracks the numbers drawn inside each so we can move those too
# set up the tiles array
for r in range(0, rows):
    t = []
    t2 = []
    t3 = []
    for c in range(0, cols):
        t.append(0)
        t2.append(None)
        t3.append(None)
    tiles.append(t)
    rects.append(t2)
    values.append(t3)



tiles[0][1] = 2
tiles[0][2] = 2
tiles[0][3] = 4
tiles[0][4] = 2
tiles[1][4] = 2
tiles[1][3] = 2

def draw():
    for i in range(0, len(tiles)):
        for n in range(0, len(tiles[i])):
            block = tiles[i][n]
            if block != 0:
                r = i
                c = n


                # set the coordinates for drawing the tile
                xstart = (bw + sw) * c
                xend = xstart + bw
                ystart = (bw + sw) * r
                yend = ystart + bw

                # draw the tile and set its fill color
                rect = Rectangle(Point(xstart, ystart), Point(xend, yend))
                rect.draw(win)
                rect.setFill( getColor(block) )
                rects[r][c] = rect

                # display its number inside the box
                xmid = int((xend - xstart) / 2)
                ymid = int((yend - ystart) / 2)

                #print(str(xmid) + ", " + str(ymid))
                value = Text(Point(xstart + xmid, ystart + ymid), block)
                value.draw(win)
                value.setTextColor('black')
                values[r][c] = value

# takes a rectangle as its parameter
def draw2(rec, oldx, oldy, newx, newy):
    rec.move( (newx-oldx)*(bw+sw), (newy-oldy)*(bw+sw)   )


"""def moved(oldx, newx, oldy, newy):

def merged(oldx1, oldy1, oldx2, oldy2, newx, newy, newNum):"""

def empty(arr):
    for i in range(0, len(arr)):
        if arr[i] != 0:
            return False
    return True
def full(arr):
    for c in range(0, len(arr)):
        if arr[c] == 0:
            return False
    return True

# returns true if there are no zeroes before a non-zero ([0, 2, 3] is false, [2, 3, 0] is true)
def allLeft(arr):
    count = 0
    for c in range(0, len(arr)):
        if arr[c] != 0:
            count = count + 1
    if full(arr):
        return True
    elif firstLeftUnfilled(arr) == count:
        return True
    else:
        return False

# returns the leftmost unfilled index
def firstLeftUnfilled(arr):
    for c in range(0, len(arr)):
        if arr[c] == 0:
            return c
    return -1
# get rid of all 0s, shift everything left accordingly
def getRidOfSpaces(arr, r):
    copy = arr
    while( not allLeft(copy)):
        for c in range(0, len(arr)-1):
            if copy[c] == 0:
                # move everything left accordingly, put a 0 at the end
                for i in range(c, len(arr)-1):
                    copy[i] = copy[i+1]

                    # controls moving drawings and updating those arrays
                    if rects[r][i+1] != None:
                        rects[r][i+1].move( -(bw+sw), 0 )
                        values[r][i+1].move( -(bw+sw), 0)
                    rects[r][i] = rects[r][i+1]
                    rects[r][len(rects[r])-1] = None

                    values[r][i] = values[r][i+1]
                    values[r][len(values[r])-1] = None

                copy[len(arr)-1] = 0

    return copy

def leftKey():
    for r in range(0, len(tiles)):
        # get rid of spaces
        tiles[r] = getRidOfSpaces(tiles[r], r)

        # control merges
        if not empty(tiles[r]):
            stack = Stack()
            row = []
            for c in range(0, len(tiles[r])-1):
                if tiles[r][c] == tiles[r][c+1]:
                    tiles[r][c] = 2 * tiles[r][c]
                    tiles[r][c+1] = 0

                    # get rid of the one that was there
                    rects[r][c+1].move(gX, gY)
                    rects[r][c+1] = None

                    # set the new text and get rid of the old one
                    values[r][c].setText(str(tiles[r][c]))
                    values[r][c+1].setText('')
                    values[r][c+1] = None

                    tiles[r] = getRidOfSpaces(tiles[r], r)



def printTiles():
    result = ""
    for r in range(0, len(tiles)):
        for c in range(0, len(tiles[r])):
            if tiles[r][c] != 0:
                result += str(tiles[r][c]) + " "
            elif tiles[r][c] == 0:
                result += "N "
            #else:
                #result += "N "
        result += "\n"
    print(result)


draw()
win.getMouse()
printTiles()
leftKey()
printTiles()





win.getMouse() # waits for a click
win.close()
