import numpy as np
import random as r
import bisect
import matplotlib
matplotlib.use('Agg')
from matplotlib.patches import Rectangle
from Lego1D import Lego1D

def clean(pop):
	'''
	Removes chromosomes with insufficient data
	'''
	return [chrom for chrom in pop if len(chrom.plane.grid) > 1]

def add_block(root, plane, s, s_new, n, h=1):
	'''
	Creates a lego object added to the root lego at its sth stud.
	'''

	x, y = root.get_added_brick_pos(s, s_new, n, h)
	newBlock = Lego1D(n, x, y, h)
	
	#Set root's studs to occupied
	pos = s_new - s
	s_temp = 0
	#while ((-1 < pos) and (pos < s_new)):

	return newBlock

def check_union(p1, p2):
	'''
	Checks if there's positions in common between two chromosomes
	'''
	#Get brick positions shared
	p1_pos = p1.plane.get_positions()
	p2_pos = p2.plane.get_positions()

	#Unique solutions
	union_pos = [val for val in p1_pos if val in p2_pos]

	#Randomly choose one
	if len(union_pos) == 0:
		return False
	pos = union_pos[r.randrange(len(union_pos))]

	return True

def random_splice_crossover(p1, p2, n):
	'''
	Randomly splices two ledge chromosomes
	'''

	#Get brick positions shared
	p1_pos = p1.plane.get_positions()
	p2_pos = p2.plane.get_positions()

	#Unique solutions
	union_pos = [val for val in p1_pos if val in p2_pos]

	#Randomly choose one
	pos = union_pos[r.randrange(len(union_pos))]
	if len(union_pos) == 0:
		return False

	p1_brick = p1.plane.get_brick(pos[0], pos[1])
	p2_brick = p2.plane.get_brick(pos[0], pos[1])

	#Splice based off those bricks starting points
	p1_splice = p1.get_splice(p1_brick, n-1)
	p2_splice = p2.get_splice(p2_brick, n-1)


	#Crossover
	p1.place_splice(p2_splice)
	p2.place_splice(p1_splice)

	p1.remove_fragments()
	p2.remove_fragments()
	return True

def selection(pop=[]):
	'''
	Applies selection to the population
	'''
	pop_size = len(pop)
	list = []

	pop = np.unique(pop)
	#Remove empty chromosomes
	pop = [chrom for chrom in pop if len(chrom.plane.grid) > 1]

	#Remove unstable chromosomes
	pop = [chrom for chrom in pop if chrom.eval_func() > 0]

	pop = np.unique(pop)
	#Format for weighted selection
	list = [[chrom.eval_func(), chrom] for chrom in pop]

	if len(list) < 1:
		return []

	return WeightedSelectionWithReplacement(list, pop_size)

def recombination(n, pop=[]):
	'''
	Recombines population using splice length n
	'''
	if len(pop) < 2:
		return pop

	pop = [chrom for chrom in pop if len(chrom.plane.grid) > 1]
	
	initial_pop = pop[:]
	final_pop = []
	pop_size = len(pop)

	#Shift the indexes of mom and dad so they're paired with diff chromosomes
	moms = initial_pop[:]
	moms.pop(0)

	dads = initial_pop[:]
	dads.pop(-1)

	#For those are compatable mate with closer fitness match
	for mom, dad in zip(moms, dads):

		if check_union(mom, dad):

			temp_mom = mom
			temp_dad = dad
			random_splice_crossover(temp_mom, temp_dad, n)
			final_pop = final_pop + [temp_mom] + [temp_dad]

	'''	
	#Fill up remaining population with random matings
	i = 0
	while len(final_pop) < pop_size:
		if i > len(final_pop):
			break
		mom = np.random.choice(initial_pop)
		dad = np.random.choice(initial_pop)

		if check_union(mom, dad):
			random_splice_crossover(mom, dad, n)
			final_pop = final_pop + [mom] + [dad]
		i += 1
	'''

	return final_pop

def mutation(rate, pop=[]):
	'''
	Attempt mutation on every chromosome given mutation rate 

	Mutation: Randomly removes a single brick
	'''
	population = []
	for chrom in pop:
		prob = r.random()
		if prob < rate:
			chrom.plane.remove_random_brick()
			chrom.refresh_bricks()
		population = population + [chrom]
	return population



def WeightedSelectionWithReplacement(l, n):
	'''
	Selects with replacement n random elements from a list of (weight, item) 
	tuples.

	Source: http://stackoverflow.com/questions/352670/weighted-random-selection-
	with-and-without-replacement
	'''
  	cuml = []
  	items = [] 
  	total_weight = 0.0
  	for weight, item in l:
  		total_weight += weight
  		cuml.append(total_weight)
  		items.append(item)
  	return [items[bisect.bisect(cuml,r.random()*total_weight)] for x in range(n)]

def get_f_bar(pop):
	'''
	Gets the average fitness of a population
	'''
	f_bar = 0

	if len(pop) == 0:
		return -1

	for chrom in pop:
		f_bar += chrom.eval_func()

	return f_bar / (1.0 * len(pop))
