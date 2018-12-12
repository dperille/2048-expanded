from graphics import *

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
class tile:
    # __init__ is python's constructor
    def __init__(self, r, c, num):
        self.r = r
        self.c = c
        self.num = num
        self.color = setColor(self.num)
    def setR(self, r):
        self.r = r
    def setC(self, c):
        self.c = c
    def setNum(self, num):
        self.num = num
    def getR(self):
        return self.r
    def getC(self):
        return self.c
    def getNum(self):
        return self.num
    def getColor(self):
        return self.color

def setColor(n):
    if n == 2:
        return 'yellow'
    elif n == 4:
        return 'red'
    else:
        return 'blue'

# tracks the objects
tiles = []
# set up the tiles array
for r in range(0, rows):
    t = []
    for c in range(0, cols):
        t.append(None)
    tiles.append(t)

# tracks the drawing of the rectangles, allowing us to move them
rects = tiles

# tracks the numbers inside each rectangle so we can move and delete those too
values = tiles


##### There's no need for the tile class really... just store the values in a 2D matrix


b1 = tile(0, 1, 2)
b2 = tile(0, 2, 2)
b5 = tile(0, 3, 4)
b6 = tile(0, 4, 2)
b3 = tile(1, 4, 2)
b4 = tile(1, 3, 2)
tiles[b1.getR()][b1.getC()] = b1
tiles[b2.getR()][b2.getC()] = b2
tiles[b3.getR()][b3.getC()] = b3
tiles[b4.getR()][b4.getC()] = b4
tiles[b5.getR()][b5.getC()] = b5
tiles[b6.getR()][b6.getC()] = b6

def draw():
    for i in range(0, len(tiles)):
        for n in range(0, len(tiles[i])):
            block = tiles[i][n]
            if block != None:
                block.setR(i)
                block.setC(n)

                r = block.getR()
                c = block.getC()


                # set the coordinates for drawing the tile
                xstart = (bw + sw) * c
                xend = xstart + bw
                ystart = (bw + sw) * r
                yend = ystart + bw

                # draw the tile and set its fill color
                rect = Rectangle(Point(xstart, ystart), Point(xend, yend))
                rect.draw(win)
                rect.setFill( block.getColor() )

                # display its number inside the box
                xmid = int((xend - xstart) / 2)
                ymid = int((yend - ystart) / 2)
                #print(str(xmid) + ", " + str(ymid))
                value = Text(Point(xstart + xmid, ystart + ymid), block.getNum())
                value.draw(win)
                value.setTextColor('black')

def moved(oldx, newx, oldy, newy):

def merged(oldx1, oldy1, oldx2, oldy2, newx, newy, newNum):



# returns true if there is at least one None between two non-Nones
# note: will return false if there are no Nones BETWEEN two non-Nones (ie. [None, 3, 3] or [3, None])
def spacesBetween(arr):
    for i in range(0, len(arr)-2):
        for x in range(2, len(arr)-i):
            if ( arr[i] != None and arr[i+1] == None and arr[i+x] != None):
                return True
    return False
def empty(arr):
    for i in range(0, len(arr)):
        if arr[i] != None:
            return False
    return True
def rightmostFilled(arr):
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


            # while spaces remain between entries, ...
            # filled is the index of the farthest column filled, with columns filled consecutively from 0 to filled
            filled = 0
            while( spacesBetween(tiles[r]) and filled < len(tiles[r]) ):
                # starting at the column after the rightmost consecutive filled, search for the next
                # element that is not None - if its number matches the leftmost, combine them
                filled = rightmostFilled(tiles[r])

                for c in range(filled+1, len(tiles[r])):
                    filled = rightmostFilled(tiles[r])

                    # for the first non-None after the filled,
                    if tiles[r][c] != None:

                        # if they're the same number, combine them
                        if tiles[r][c].getNum() == tiles[r][filled].getNum():
                            tiles[r][filled].setNum( 2 * tiles[r][filled].getNum())
                            tiles[r][c] = None

                        # if they're different, just move it
                        else:
                            temp = tiles[r][c]
                            tiles[r][c] = None
                            tiles[r][filled+1] = temp
                        # once you've found the first non-None after filled, break out
                        break




        # if the row is empty, do nothing


def printTiles():
    result = ""
    for r in range(0, len(tiles)):
        for c in range(0, len(tiles[r])):
            if tiles[r][c] != None:
                result += str(tiles[r][c].getNum()) + " "
            elif tiles[r][c] == None:
                result += "N "
        result += "\n"
    print(result)

draw()
printTiles()
leftKey()
printTiles()
draw()








win.getMouse() # waits for a click
win.close()
