import cellDecomp

fieldWidth = 500
fieldHeight = 500

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
		
		if leftX < nextX and rightX > nextX:
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
	
	#Function is finished when we hit the bottom-right (top-right?) of the field
	while currentY < fieldHeight:
		
		#Find the next collision with a block and retrieve the needed points
		points = findCollision([currentX,currentY],inputBlocks)
		currentX = points[0]
		currentY = points[1]
		nextX = points[2]
		nextY = points[3]

		if not inCellsOrBlocks(points,cells,inputBlocks):
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
	return cells
	
inputBlocks = cellDecomp.inputFile("./inputs/Blocks/")
print inputBlocks
print makeBlocks(inputBlocks)