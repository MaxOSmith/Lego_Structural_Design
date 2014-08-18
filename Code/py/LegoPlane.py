import helper_funcs as func
import numpy as np
import random as r
from Lego1D import Lego1D

class LegoPlane:

	def __init__(self):
		'''
		Constructor
		'''
		self.grid =[]	#Array of tuples containing first the brick and then
						#all positions occupied by that brick

	def place_brick(self, brick):
		'''
		Places a brick into the plane if the area is already unoccupied
		'''
		found = False
		new_pos = brick.pos

		#For each brick in the grid
		for bricks in self.grid:
			#For each position for each brick
			for pos in bricks[1]:
				try:
					new_pos.index(pos)
					found = True
				except:
					pass
		if found:
			return False

		self.grid.append((brick, new_pos))
		return True

	def get_brick(self, x, y):
		'''
		Returns brick at given coordinates
		'''
		for brick in self.grid:
			for pos in brick[0].pos:
				if (pos == [x, y]):
					return brick[0]
		return None

	def get_brick_index(self, brick):
		'''
		Returns the index of the brick
		'''
		i = 0
		for brick in self.grid:
			if brick[0] == brick:
				return i

			i += 1

		return -1

	def remove_brick_by_index(self, i):
		'''
		Removes brick based on index
		'''
		self.grid.pop(i)

		#Needs to unattach bricks

	def remove_random_brick(self):
		'''
		Randomly removes a brick
		'''
		size = len(self.grid)
		if size < 2:
			return
		self.remove_brick_by_index(r.randrange(size))

	def affix_neighbors(self, brick):
		'''
		Attaches any bricks attached above and below the brick
		'''
		#Find brick in grid
		found = False
		while not(found):
			for bricks in self.grid:
				if bricks[0] == brick:
					brick = bricks
					found = True
					break
			if found:
				break
			self.place_brick(brick)

		#For every position in the given brick
		for pos in brick[0].pos:
			#Check Above
			pos[1] += 1
			
			#For every brick in the grid
			for i in range(len(self.grid)):
				#Skip itself
				if self.grid[i][0] == brick[0]:
					continue
				#Check all coordinates of the grid's brick for a match
				for coord in self.grid[i][1]:
					if pos == coord:
						brick[0].studs[bricks[1].index(pos)] = self.grid[i][0]
			pos[1] -= 1

			#Check Below 
			for i in range(len(self.grid)):
				#Skip itself
				if self.grid[i][0] == brick[0]:
					continue
				#Check all coordinates of the grid's brick for a match
				for coord in self.grid[i][1]:
					coord[1] -= 1
					if pos == coord:
						coord[1] += 1
						self.grid[i][0].tubes[self.grid[i][0].pos.index(coord)] = brick[0]

					else:
						coord[1] += 1

	
	def detach_brick(self, brick):
		'''
		Removes brick from any other bricks studs or tubes
		'''

		try:
			self.grid.pop(self.grid.index((brick, brick.pos)))
		except:
			#If somewhere prior to calling detach_brick removes the brick
			#Carry on
			pass

		for stud in brick.studs:
			stud = None
		
		for tube in brick.tubes:
			tube = None

		for b in self.grid:
			br = b[0]

			br.studs = [stud if stud != brick else None for stud in br.studs]
			br.tubes = [tube if tube != brick else None for tube in br.tubes]


	def check_if_open(self, brick):
		'''
		Checks if you're able to place brick in plane without overlapps
		'''

		for pos in brick.pos:
			for b in self.grid:
				for check_pos in b[1]:
					if pos == check_pos:
						return False
		return True
		
	def get_bricks(self):
		'''
		Gets an array of all unique bricks
		'''
		bricks = []
		for b in self.grid:
			bricks.append(b[0])

		return bricks

	def get_positions(self):
		'''
		Gets an array of all unique occupied positions, skipping first
		'''
		bricks = self.get_bricks()

		#If no bricks return none
		if len(bricks) < 2:
			return []

		#Skip ledge
		bricks.pop(0)

		positions = []
		for b in bricks:
			positions = positions + b.pos

		return positions

	def get_open_bricks(self):
		'''
		Returns the bricks with open studs/tubes
		'''

		open_studs = []
		open_tubes = []

		all_bricks = self.get_bricks()

		for br in all_bricks:
			#Check Studs
			for stud in br.studs:
				if isinstance(stud, Lego1D):
					continue
				else:
					open_studs.append(br)
					break
			
			#Check Tubes
			for tube in br.tubes:
				if isinstance(stud, Lego1D):
					continue
				else:
					open_tubes.append(br)
					break

		return np.unique(open_studs), np.unique(open_tubes)

