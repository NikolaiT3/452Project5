from Tkinter import *
from math import *
import graph
import thread
import random
import time
import glob
import re
import pprint

from collections import defaultdict

fieldWidth = 500
fieldHeight = 500

class Graph(object):
    # Graph data structure, undirected by default.
    # http://stackoverflow.com/questions/19472530/representing-graphs-data-structure-in-python
    
    def __init__(self, connections, directed=False):
        self._graph = defaultdict(set)
        self._directed = directed
        self.add_connections(connections)

    def add_connections(self, connections):
        #Add connections (list of tuple pairs) to graph
        for node1, node2 in connections:
            self.add(node1, node2)

    def add(self, node1, node2):
        #Add connection between node1 and node2
        self._graph[node1].add(node2)
        if not self._directed:
            self._graph[node2].add(node1)

    def remove(self, node):
        #Remove all references to node
        for n, cxns in self._graph.iteritems():
            try:
                cxns.remove(node)
            except KeyError:
                pass
        try:
            del self._graph[node]
        except KeyError:
            pass

    def is_connected(self, node1, node2):
        #Is node1 directly connected to node2
        return node1 in self._graph and node2 in self._graph[node1]

    def find_path(self, node1, node2, path=[]):
        #Find any path between node1 and node2 (may not be shortest)
        path = path + [node1]
        if node1 == node2:
            return path
        if node1 not in self._graph:
            return None
        for node in self._graph[node1]:
            if node not in path:
                new_path = self.find_path(node, node2, path)
                if new_path:
                    return new_path
        return None

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, dict(self._graph))

class App:
    def __init__(self, master):

        w = Canvas(master, width=500, height=500)
        w.pack()

        # prevents window from shrinking to fit buttons
        w.grid_propagate(0)

        self.quit = Button(w, text="QUIT", fg="red", command=w.quit)
        self.quit.grid(row=0, column=0)

        self.start = Button(w, text="Start", command=self.run)
        self.start.grid(row=0, column=1)

        thread.start_new_thread(drawPoints, (w, 1))
        thread.start_new_thread(drawBlocks, (w, 2))
        #thread.start_new_thread(seeBlocks, (w, 3))

    def run(self):
        runBot()

# ===============================
# IMPORT FILE FUNCTION
# ===============================
def inputFile(path):
  # print path
  filenames = glob.glob(path+"*.txt")
  # print filenames
  text =[]
  for file in filenames:
      text += open(file,'r')
  return sanitize_input(text)

# ===============================
# SANITIZE INPUT FUNCTION
# ===============================
def sanitize_input(text):
  sanitized_text = []
  for word in text:

		# Get rid of punctuation, convert to lower, remove new line characters
		# text = text.translate(None, string.punctuation).lower()

      sanitize = re.sub("[^\w']|_", " ", word.lower())
      words = list(sanitize.split())

		# List of lists to keep books structure
      sanitized_text.append(words)
      sanitized_text = input_toNumber(sanitized_text)
  return sanitized_text

def input_toNumber(text):
  sanitized_number = []
  for word in text:
      temp = []
      for number in word:
          new = float(number)
          temp.append(new)
      sanitized_number.append(temp)
  return sanitized_number

# =======================================
# CHECK IF REGION IS IN A CELL OR A BLOCK
# =======================================
def inCellsOrBlocks(region,cells,inputBlocks):
	#Check if either the top-left or bottom-right corners of
	#the given region is the corner of an already existing cell
	for cell in cells:
		if(region[0] == cell[0] and region[1] == cell[1]) or (region[2] == cell[2] and region[3] == cell[3]):
			return True

	#Check if either the top-left or bottom-right corners of
	#the given region is inside one of the obstacle blocks
	for block in inputBlocks:
			if((region[0] > block[0] and region[0] < block[2] or region[2] > block[0] and region[2] < block[2])
				and (region[1] > block[1] and region[1] < block[3] or region[3] > block[1] and region[3] < block[3])):
					return True

	return False

# =======================================
# FIND THE NEXT COLLISION FUNCTION
# =======================================
def findCollision(point, inputBlocks):
	#Set our next position out of bounds so we guarantee that we either
	#collide with a box or are at the end
	currentX = point[0]
	currentY = point[1]
	nextX = fieldWidth+1
	nextY = fieldHeight

	#We imagine that the vertical edges of the blocks extend infinitely,
	#and check for the next collision with an edge
	for block in inputBlocks:
		leftX = block[0]
		leftY = block[1]
		rightX = block[2]
		rightY = block[3]

		#If we hit the left edge, we automatically extend the cell downwards
		#If we hit the right edge, we need to check which way to extend
		if leftX < nextX and leftX > currentX:
			nextX = leftX
		if rightX < nextX and rightX > currentX:
			nextX = rightX

			#If we are on top of the block, we need to extend the cell upwards
			#else we extend downwards
			if leftY < nextY and leftY > currentY:
				nextY = leftY
			if rightY < nextY and rightY > currentY:
				nextY = rightY

	#If we're at the bottom of a block, we check for other collisions
	#below (above?) the block, otherwise we extend the cell to the bottom (top?)
	for block in inputBlocks:
		leftX = block[0]
		leftY = block[1]
		rightX = block[2]
		rightY = block[3]

		if leftX < nextX and rightX > nextX and leftY < nextY:
			nextY = leftY
	points = [currentX, currentY, nextX, nextY]
	return points

def makeBlocks(inputBlocks):
	#Blocks are made by scanning the field in row-major order
	#(go across horizontally, step down (up? idk how Python does it), go across again, etc.)

	#Initialize current position and empty list of cells
	currentX = 0
	currentY = 0
	cells = []
	index = 0

	#Function is finished when we hit the bottom-right (top-right?) of the field
	while currentY < fieldHeight:

		#Find the next collision with a block and retrieve the needed points
		points = findCollision([currentX,currentY],inputBlocks)
		currentX = points[0]
		currentY = points[1]
		nextX = points[2]
		nextY = points[3]

		if not inCellsOrBlocks(points,cells,inputBlocks):
			points.append(index)
			cells.append(points)

		#Move our x point forward
		currentX = nextX

		#When we hit the right edge of the screen, we need to move our y
		#position to the next lowest (highest?) block edge
		if(currentX >= (fieldHeight-1)):
			nextY = fieldHeight+1
			for block in inputBlocks:
				if block[1] < nextY and block[1] > currentY:
					nextX = block[0]
					nextY = block[3]
				if block[3] < nextY and block[3] > currentY:
					nextX = block[2]
					nextY = block[3]
			currentX = 0
			currentY = nextY
			index = index - 1

		index = index + 1

	return cells

# =======================================
# Draw Blocks, start points, and free space
# =======================================
def drawBlocks(canvas, n):
  	x1 = inputBlocks[0][0]
	y1 = inputBlocks[0][1]
	x2 = inputBlocks[0][2]
	y2 = inputBlocks[0][3]
	rect1 = canvas.create_rectangle(x1, y1, x2+1, y2+1, fill='#fff')

  	x1 = inputBlocks[1][0]
	y1 = inputBlocks[1][1]
	x2 = inputBlocks[1][2]
	y2 = inputBlocks[1][3]
	rect2 = canvas.create_rectangle(x1, y1, x2+1, y2+1, fill='#fff')

	x1 = inputBlocks[2][0]
	y1 = inputBlocks[2][1]
	x2 = inputBlocks[2][2]
	y2 = inputBlocks[2][3]
	rect3 = canvas.create_rectangle(x1, y1, x2+1, y2+1, fill='#fff')

def drawPoints(canvas, n):
	x1 = startPoint[0][0]
	y1 = startPoint[0][1]
	firstPoint = canvas.create_rectangle(x1, y1 , x1+10, y1+10, fill="blue")
	canvas.tag_raise(firstPoint)
	canvas.tag_raise(firstPoint)

	x2 = endPoint[0][0]
	y2 = endPoint[0][1]
	secondPoint = canvas.create_rectangle(x2, y2 , x2+10, y2+10, fill="red")
	canvas.tag_raise(secondPoint)
	canvas.tag_raise(secondPoint)

def seeBlocks(canvas, n):
	for block in splitBlocks:
		# print block
		canvas.create_rectangle(block[0], block[1] , block[2], block[3], fill="yellow")

# =======================================
# STORE BLOCKS INTO GRAPH
# =======================================
def storeVerticalBlocks(splitBlocks):
	size = len(splitBlocks)
	c = []
	connections = []
	index = 0
	for block in splitBlocks:
		for i in range (0, size):
			if i != index:
				# increment i and store it in c
				c.append(i)
		connections.append(c)
		index = index + 1
		c = []
	g = convertToTuples(connections, size)
	return g

def convertToTuples(connections, size):
	c = []
	conSize = len(connections[0])
	for j in range (0, size):
		for k in range (0, conSize):
			tup = (j, connections[j][k])
			c.append(tup)
	g = Graph(c)
	return g

# =======================================
# RUN THE ROBOT
# =======================================
def runBot():
	print "Succesful Function Call"

# =======================================
# Run Point Robot Simulator
# =======================================
inputBlocks = inputFile("./inputs/Blocks/")
print inputBlocks
splitBlocks = makeBlocks(inputBlocks)
print splitBlocks
g = storeVerticalBlocks(splitBlocks)
# pprint(g._graph)
print g

print g.find_path(0, 5)

startPoint = inputFile("./inputs/Start/")
# print startPoint

endPoint = inputFile("./inputs/End/")
# print endPoint

master = Tk()

app = App(master)

master.mainloop()
