Assume
	-'test' is the name of your next run
Recall
	-Each Lego Structure is a chromosome
	-Population is a group of chromosomes

------------------------------------------------
Procedure
------------------------------------------------

1. Create two subdirectories 'png/test/' & 'txt/test/', these will contain the respected file types of output from your run. Inside the 'png/test/' directory create two folders 'initial' & 'final'

2. Open the driver.py file in the text editor of your choice.

3. Locate the portion of the code entitled 'User Inputs'

4. Specify your input variables for the run (Recommended values in parens, to ensure it's running properly):

	a. pop_size: Int size of the population, or the number of chromosomes you would like generated. Ensure that this value is divisable by the number of processors you intend on using (24).

	b. brick_count: Int size of the chromosome, the number of data values (bricks) that each chromosome will start with (30).

	c. generations: Int size of the number of generations that you wish to produce in this run (20).

	d. ledge_size: Int size of the ledge (starting brick) for each chromosome (10).

	e. mutation_rate: Probability that each chromosome has of experiencing a mutation during a generation (.05).

	f. splice_size: Int number of bricks that each splice will contain, this value must be less than brick_count (4).

	g. directory: String containing 'png/' concatenated with the name of the run, for this example: 'png/test/'. This directory is where the png output files will be stored.

	h. save_dir: String containg 'txt/' concatenated with the name of the run, for this example: 'txt/test/'. This directory is where the txt output files will be stored.

5. Run the program using MPI or python through your preferred method.

------------------------------------------------

Output

Located in the 'png/<run name>/' folder should be two *.png files along with the 'final' & 'initial' folders you created before running the program. The two folders contain images of the entire population entitled after their respective time during running (eg. 'initial' before the program executes). The first image is 'Fitness.png', this is a chart showing the average fitness of the population through each generation that it went through - buggy not currently working as desired. The second image is 'Most Fit.png' this is the chromosome that had the highest fitness of the final population, the "answer" so to speak.

The output in the 'txt' file are *.dat files that contain save points throughout the run. Opening them in a text editor is meaningless, use pickle to unpack the object.