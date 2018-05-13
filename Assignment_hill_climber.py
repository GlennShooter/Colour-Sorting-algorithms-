""" A hill climber algorithm, you can select a colour sample and a numeric stopping criteria.  The algorithm will print the best solution it finds and will print the sorted colours on screen"""

# Import required libraries 
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from random import randint
from random import shuffle
import math 

###########Functions#################

##### 1. Setup Functions: These Functions read the data and create datasets of various sizes #####

#Takes in the file name returns files size and a dataframe of colours. 
def read_file(file):
 	with open (file, "rU") as cfile:
 		lines  = cfile.readlines()
 	f_size = lines[0]
 	data = lines[1:]
 	colours = []
 	for colour in data:
 		colour = colour.split(" ")
 		colour = list(map(float, colour))
 		colours.append(colour)
 	
 	return f_size, colours

#Takes only the first n colours in the file please note index starts at 1
def take(dataset, size):
	n_colours = []
	for i in range(size):
		n_colours.append(dataset[i])
	return n_colours

##### 2 Algorithm: These Functions are all needed for the random search algorithm #####

#Finds the sum echlidian distance of a solution 
def evaluate(solution):
	Sum_echlidian_dist = 0
	#For to find the sum echlidian distance for the solution
	for i in range(len(solution) - 2):
		place1 = solution[i]
		place2 = solution[i + 1]
		red1 = place1[0]
		red2 = place2[0]
		green1 = place1[1]
		green2 = place2[1]
		blue1 = place1[2]
		blue2 = place2[2]

		echlidian_dist = math.sqrt(math.pow(red1 - red2,2) + math.pow(green1 - green2,2) + math.pow(blue1 - blue2,2))
		Sum_echlidian_dist = Sum_echlidian_dist + echlidian_dist
	return solution, Sum_echlidian_dist

#Randomly mutate solution 
def random_mutation(solution):
#Inverts solution creating a random 2 flip neighbour
	pos1 = randint(0, len(solution)-1) 
	pos2 = randint(0,len(solution)-1)
	if pos1 < pos2:
		solution[pos1:pos2] = solution[pos1:pos2][::-1]
	if pos2 < pos1:
		solution[pos2:pos1] = solution[pos2:pos1][::-1]
	mutated_data = solution
	
	return mutated_data

	
    

#Function takes in a list of solutions finds the solution with the lowest echlidian disatance and returns it 
def sort_list(solutions):
	best_sol = solutions[0][0:-1]
	best_dist = solutions[0][-1]
	for i in range(len(solutions) - 1):
		if solutions[i][-1] < best_dist:
			best_dist = solutions[i][-1]
			best_sol = i
	return best_sol, best_dist



#### 3 Display: Functions needed to display final output as a picture #####

# Display the colours in the order of the permutation in a pyplot window 
def plot_colours(colours, permutation):

	assert len(colours) == len(permutation)
	
	ratio = 10 # ratio of line height/width, e.g. colour lines will have height 10 and width 1

	img = np.zeros((ratio, len(colours), 3))

	for i in range(0, len(colours)):
		img[:, i, :] = colours[permutation[i]]

	fig, axes = plt.subplots(1, figsize=(8,4)) # figsize=(width,height) handles window dimensions
	axes.imshow(img, interpolation='nearest')
	axes.axis('off')
	plt.show()



######### Setup #######
data = read_file("C:\\Users\\Glenn's pc\\Documents\\Uni\\ITNPBD8\\Assignment\\colours.txt") #Read in data file

#Create 3 data sets,10, 100 and 1000 colour datasets
f_size = data[0]
data = data[1] #1000 colour sample
size = len(data)
permutations = np.arange(size) #important for visulization 

data_ten = take(data,10) #10 colour sample
size_ten = len(data_ten)
permutations_ten = np.arange(size_ten)


data_hundred = take(data,100) #100 colour sample
size_hundred = len(data_hundred)
permutations_hundred = np.arange(size_hundred)


#######SET STOPPING CRITERIA AND CHOOSE COLOUR SAMPLE######
stopping_criteria = 10000 #Number of iterations before the algorithm stops 1170.81
sample = data  #Select data for 1000 colour sample data_hundred for the 100 colour sample and data 10 for the 10 colour sample

#Setting the permutations important for graphing
if sample == data:
	per = permutations
if sample == data_ten:
	per = permutations_ten
if sample == data_hundred:
	per = permutations_hundred

###### Main ######
x = 0
result_dist = 10000 #create a variable to hold the lowest echlidian distance found so far
init_solution = random_mutation(sample) #Create a random initial solution
while x < stopping_criteria : #Stopping criteria when x reaches 1000
#I create an initial solution and initial evaluation
	init_evaluation = evaluate(init_solution)
	init_dist = init_evaluation[-1]
#Produce a random neighbour and evaluate it 
	neighbour = random_mutation(init_solution)
	neighbour_evaluation = evaluate(neighbour)
	neighbour_dist = neighbour_evaluation[-1]

#Compair with best solution if the euchlidian distance is less than current best solution the neighbour becomes the best solution 
	if init_dist < neighbour_dist:
		test = init_solution
		test_dist = init_dist

	if neighbour_dist <= init_dist:
		init_solution = neighbour
		test = neighbour
		test_dist = neighbour_dist

	if test_dist < result_dist:
		result = test
		result_dist = test_dist
	

	x = x + 1 #next hill climb

print("Solution: ", result," Echlidian Distance: ", result_dist) #print best result on screen
plot_colours(result, per) #print colour chart

