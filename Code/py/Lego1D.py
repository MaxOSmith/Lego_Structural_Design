import numpy as np

class Lego1D:
	def __init__(self, n=2, x=0, y=0, h=1):
		'''
		Constructor
		'''
		self.n = n 								#Number of studs
		self.studs = np.empty(n, dtype=object)	#Array of studs
		self.tubes = np.empty(n, dtype=object)	#Array of tubes
		self.x = x 								#X position of bottom left corner
		self.y = y 								#Y position of bottom left corner
		self.h = h 								#Height
		#All of the positions occupied by the brick
		self.pos = [[self.x+i+.5, self.y+.5] for i in range(n)]

	def get_added_brick_pos(self, s, s_new, n_new, h_new=1):
		'''
		Calculates the brick position when added to the sth stud
		with 0 being the furthest left stud.
		'''
		#Get position of sth stud on brick
		x = self.x + s
		y = self.y + self.h

		#Get bottom left corner of new brick
		x -= (s_new - 1)+1
		return x,y

	def get_attached_bricks(self):
		'''
		Gets an array of all the bricks connected othe studs or 
		tubes of the brick
		'''		
		bricks = []

		for b in self.studs:
			bricks.append(b)
		for b in self.tubes:
			bricks.append(b)

		#Remove any null objects
		i = 0
		while i < len(bricks):
			if bricks[i] == None:
				bricks.pop(i)
				i -= 1
			i += 1

		return np.unique(bricks)

	def get_middle(self):
		'''
		Calculates the middle coordinate of the brick
		'''
		mid_x, mid_y = self.x, self.y
		mid_y += .5
		mid_x += self.n*.5

		return mid_x, mid_y

	def get_furthest_left_x(self):
		'''
		Returns the furthest left x value of the brick
		'''
		return self.x + self.n

	def get_mass(self):
		'''
		Calculates the mass of the brick, assuming each stud in length
		is one unit of mass
		'''
		return self.n

	def clear_brick(self):
		'''
		Removes any bricks connected to it
		'''
		for s in self.studs:
			s = None
		for t in self.tubes:
			t = None