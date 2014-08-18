from Lego1D import Lego1D
from LegoPlane import LegoPlane
import matplotlib
matplotlib.use('Agg')
from matplotlib.patches import Rectangle
import random as r
import numpy as np
import matplotlib.pylab as plt


class LedgeProblem:
	
	def __init__(self, l, x_pos=0, y_pos=-1):
		'''
		Constructor
		'''
		self.ledge = Lego1D(n=l, y=y_pos)	#Base piece of the structure
		self.plane = LegoPlane()			#Plane that contains all bricks
		self.bricks = [2, 3, 4]				#Dimensions of allowed bricks
		self.plane.place_brick(self.ledge)

	def print_plot(self, title):
		'''
		Outputs the current grid to a .png file
		'''
		plt.ioff()
		fig, axs = plt.subplots()

		#Default extrema values for x & y dimension
		max_x, min_x = 1, -1
		max_y, min_y = 1, -1

		for brick in self.plane.grid:
			#Draw the brick
			axs.add_patch(Rectangle((brick[0].x, brick[0].y), brick[0].n, brick[0].h))

			#Find extrema
			for pos in brick[0].pos:
				max_x = max([max_x, pos[0]])
				min_x = min([min_x, pos[0]])
				max_y = max([max_y, pos[1]])
				min_y = min([min_y, pos[1]])
		if len(self.plane.grid) > 1:
			plt.title('Chromosome - f=%.3f' %self.eval_func())
		else:
			plt.title('Chromosome - f=000')

		#Create buffer around edge of drawing in the graph
		axs.set_xlim(min_x - 2.5, max_x + 5.0)
		axs.set_ylim(min_y - 2.5, max_y + 5.0)

		fig.savefig(str(title) + '.png')
		plt.close(fig)


	def remove_fragments(self):
		'''
		Any chunks not somehow connected to the ledge are fragments and
		get removed because they "fall"
		'''		
		self.refresh_bricks()

		#Start from ledge, and find every brick connected to ledge
		connected = [self.ledge]
		for i in self.plane.grid:
			for br in connected:
				new_bricks = br.get_attached_bricks()
				connected = np.append(connected, new_bricks)
				connected = np.unique(connected)

		connected = np.unique(connected)

		con_pos = [(b, b.pos) for b in connected]

		#Remove bricks that weren't found connected to ledge
		self.plane.grid = [item for item in self.plane.grid if item in con_pos]


	def refresh_bricks(self):
		'''
		Refreshes brick connections
		'''
		for b in self.plane.grid:
			b[0].clear_brick()
		for b in self.plane.grid:
			self.plane.affix_neighbors(b[0])

	def eval_func(self):
		'''
		Evaluates the stability of the system, the 
		'''
		self.remove_fragments()

		if len(self.plane.grid) < 2:
			return 0

		print self.plane.grid

		#Calculate center of mass & how far the
		#system reaches out
		weighted_x = 0.0
		total_mass = 0.0
		x_reach = 0.0

		for b in self.plane.grid:
			brick = b[0]

			#Skip the ledge
			if brick == self.ledge:
				continue

			x_mid, y_mid = brick.get_middle()
			mass = brick.get_mass()

			#Numerator SUM(mass*position)
			weighted_x += x_mid * mass
			total_mass += mass

			x_reach = max([brick.get_furthest_left_x(), x_reach])

		x_centered = weighted_x / total_mass

		return x_reach * x_centered

	def randomly_place(self):
		'''
		Randomly places brick in on the system
		'''

		for b in self.plane.grid:
			b[0].clear_brick()
			self.plane.affix_neighbors(b[0])

		#Open positions
		studs, tubes = self.plane.get_open_bricks()
		if studs.size == 0 and tubes.size == 0:
			return False
		place = None

		while True:
			#Randomly select brick to use
			s = np.random.choice(self.bricks)

			#Randomly pick between studs and tubes to attach to
			choice = r.randrange(1)
			if choice:
				places = studs
			else:
				places = tubes

			if len(places) == 0:
				continue
			place = np.random.choice(places)

			#Randomly pick the stud to connect to which tube - Time 
			dest = r.randrange(place.n)		
			stud = r.randrange(s)

			#Get new brick position
			x, y = place.get_added_brick_pos(dest, stud, s)

			brick = Lego1D(n=s, x=x, y=y)
			if self.plane.check_if_open(brick):
				self.plane.place_brick(brick)
				self.plane.affix_neighbors(brick)
				break

		for b in self.plane.grid:
			b[0].clear_brick()
			self.plane.affix_neighbors(b[0])
		return True

	def place_splice(self, splice=[]):
		'''
		Places splice in the system
		'''
		#Remove all bricks occupying any spliced bricks spot
		for sp in splice:
			for pos in sp.pos:
				brick = self.plane.get_brick(pos[0], pos[1])

				#If there isn't a brick occupying the position skip
				if brick == None:
					continue

				self.plane.detach_brick(brick)

		#All bricks spaces open
		for sp in splice:
			assert(self.plane.check_if_open(sp))

		#Place in plane
		for sp in splice:
			self.plane.place_brick(sp)

		#Affix neighbors when everyone is in the plane
		for sp in splice:
			self.plane.affix_neighbors(sp)

	def get_random_splice(self, n):
		'''
		Gets splice of n bricks from the grid, removing them from the grid
		'''
		if (n < 1):
			return 0

		spliced = []

		#Randomly select a single brick to be the root of spliced bricks
		bricks = self.plane.get_bricks()
		bricks = np.delete(bricks, 0)
		root_brick = np.random.choice(bricks)
		assert(root_brick != self.ledge)

		#One brick found
		spliced.append(root_brick)
		n -= 1

		#Find remaining bricks from those connect to root
		for i in range(n):
			new_bricks = []

			for b in spliced:
				new_bricks = np.append(new_bricks, b.get_attached_bricks())

			if i == 0:
				self.plane.detach_brick(root_brick)

			new_bricks = np.unique([item for item in new_bricks if item not in spliced])
			new_bricks = np.delete(new_bricks, np.where(new_bricks==self.ledge))

			#No more connected bricks
			if len(new_bricks) == 0:
				return spliced

			new_brick = np.random.choice(new_bricks)
			spliced.append(new_brick)
			self.plane.detach_brick(new_brick)


		#In case only root brick is removed, detach
		try:
			self.plane.detach_brick(root_brick)
		except:
			pass

		return spliced

	def get_splice(self, root_brick, n):
		'''
		Gets splice of n bricks from the grid, removing them from the grid
		'''
		if (n < 1):
			return 0

		assert(root_brick != self.ledge)
		spliced = []

		#One brick found
		spliced.append(root_brick)
		n -= 1

		#Find remaining bricks from those connect to root
		for i in range(n):
			new_bricks = []

			for b in spliced:
				new_bricks = np.append(new_bricks, b.get_attached_bricks())

			if i == 0:
				self.plane.detach_brick(root_brick)

			new_bricks = np.unique([item for item in new_bricks if item not in spliced])
			new_bricks = np.delete(new_bricks, np.where(new_bricks==self.ledge))

			#No more connected bricks
			if len(new_bricks) == 0:
				return spliced

			new_brick = np.random.choice(new_bricks)
			spliced.append(new_brick)
			self.plane.detach_brick(new_brick)


		#In case only root brick is removed, detach
		try:
			self.plane.detach_brick(root_brick)
		except:
			pass

		return spliced

