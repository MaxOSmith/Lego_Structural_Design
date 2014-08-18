################################
# User Inputs

#Size of the population, divisable by the number of processors
pop_size = 24

#Number of bricks intially in each individual
brick_count = 30

#Number of generations to calculate
generations = 20

#Size of the ledge to build off of
ledge_size = 10

#Rate at which a chromosome may be mutated [0, 1)
mutation_rate = .05

#Crossover size, less than the brick_count
splice_size = 4

#Directory to save ouput, directory must exist and contain 
#two folders called: initial, final
directory = 'png/run14/'
save_dir = 'txt/run14/'

################################
import matplotlib
matplotlib.use('Agg')
import matplotlib.pylab as plt
from py.LedgeProblem import LedgeProblem
from py.helper_funcs import *
from mpi4py import MPI
import pickle
import sys

sys.setrecursionlimit(2000)		#Change recursion limit to allow pickle 

comm = MPI.COMM_WORLD			#Communication link between processors
rank = comm.Get_rank()			#Rank of each processor
plt.ioff()				#Turns off interative mode, so no figures pop up

current_pop = []			#Current states of the population
gen = []				#Array full of generation values
f_bar = []				#Array full of average fitness value

#Generate initial population
#Assumption, pop_size is divisable by the comm.size
for i in range(pop_size / comm.size):
	problem = LedgeProblem(ledge_size)
	for j in range(brick_count):
		problem.randomly_place()
	current_pop.append(problem)

#Combine population in the root processor
if rank != 0:
	comm.send(current_pop, dest=0)
else:
	for i in range(1, comm.size):
		current_pop = current_pop + comm.recv(source=i)

#Take before images, apply generations, take after images
if rank == 0:
	gen.append(0)
	f_bar.append(get_f_bar(current_pop))

	#Print initial images
	i = 0
	for p in current_pop:
		p.print_plot(directory + 'initial/Initial - ' + str(i))
		i += 1

	#Put the population through generations
	for i in range(generations):
		print 'Generation - ', i, ' ----------------------------------------'
		print 'Current_pop Length: ', len(current_pop)
		print '-Selection'
		current_pop = selection(current_pop)
		if len(current_pop) > 1:
			break
		print '-Recombination'
		current_pop = recombination(splice_size, current_pop)
		if len(current_pop) > 1:
			break
		print '-Mutation'
		current_pop = mutation(mutation_rate, current_pop)
		if len(current_pop) > 1:
			break

		#Need an even number for crossover
		if len(current_pop) % 2 == 1:
			current_pop.pop(-1)

		gen.append((i+1))
		f_bar.append(get_f_bar(current_pop))

		#Not enough chromosomes to continue
		if len(current_pop) < 2:
			break
		f = open(save_dir + str(i) + '.dat', 'w+')
		pickle.dump(current_pop, f)
		
		f_fit = open(save_dir + 'fit' + str(i) + '.dat', 'w+')
		pickle.dump(f_bar, f_fit)


	#Print final images
	i = 0
	for p in current_pop:
		p.print_plot(directory + 'final/Final - ' + str(i))
		i += 1
	if len(current_pop) > 1:
		best = current_pop[0]
		for chrom in current_pop:
			if chrom.eval_func() > best.eval_func():
				chrome = best
		best.print_plot(directory + 'Most Fit')
	else:
		print 'Everybody died'

	fig = plt.figure()
	plt.plot(gen, f_bar, 'b-')
	plt.title('Fitness of Population')
	plt.xlabel('Generation')
	plt.ylabel('Average Fitness')
	fig.savefig(directory + 'Fitness')

