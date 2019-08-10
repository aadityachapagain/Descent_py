import numpy as np
import random
import random
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('TKAgg')
TOTAL_POP = 100

MSG = "PYTHON"
TARGET = ' '.join(format(ord(m), 'b') for m in MSG)
GENES = '01 '

def chromosome():
    global TARGET
    return [mutation() for t in range(len(TARGET))]
def mutation():
    global GENES
    return random.choice(GENES)

def DNA_mismatch(population):
    global TARGET
    errors = []
    for p in population:
        error = 0
        for i in range(len(TARGET)):
            if p[i] != TARGET[i]:
                error += 1
        errors.append(error)
    return list(zip(population,errors))


def CrossOverWithoutMutation(p1,p2):
    child_chromosome = []
    for i in range(len(TARGET)):
        prob = random.random()
        if prob <0.5:
            child_chromosome.append(p1[i])
        else :
            child_chromosome.append(p2[i])
    return child_chromosome


def CrossOverWithMutation(p1,p2):
    child_chromosome = []
    for i in range(len(TARGET)):
        prob = random.random()
        if prob <0.45:
            child_chromosome.append(p1[i])
        elif prob <0.90:
            child_chromosome.append(p2[i])
        else:
            child_chromosome.append(mutation())
    return child_chromosome

def onePointCrossOver(p1,p2):
    global TARGET
    child_chromosome_1,child_chromosome_2= p1,p2
    shuffle_index = np.random.choice(np.arange(0,len(TARGET)))
    for s in range(shuffle_index):
        child_chromosome_1[s],child_chromosome_2[s] = child_chromosome_2[s],child_chromosome_1[s]
    return [child_chromosome_1,child_chromosome_2]


def twoPointCrossOver(p1,p2):
    global TARGET
    child_chromosome_1,child_chromosome_2= p1,p2
    shuffle_index = random.choice(np.arange(0,len(TARGET)))
    shuffle_after_index = random.randint(shuffle_index,len(TARGET))
    for s in range(shuffle_index,shuffle_after_index):
        child_chromosome_1[s],child_chromosome_2[s] = child_chromosome_2[s],child_chromosome_1[s]
    return [child_chromosome_1,child_chromosome_2]

def uniformCrossOver(p1,p2):
    global TARGET
    child_chromosome_1,child_chromosome_2= p1,p2
    for index in range(len(TARGET)):
        p = random.random()
        if p < 0.8:
            child_chromosome_1[index],child_chromosome_2[index] = child_chromosome_2[index],child_chromosome_1[index]
        else:
            child_chromosome_1[index],child_chromosome_2[index] = mutation(),mutation()
    return [child_chromosome_1,child_chromosome_2]


#Here we are creating random population at first these lines do that
population = []
for t in range(TOTAL_POP): 
    individual = chromosome()
    population.append(individual)
 
#Here we are creating the DNA Score of the random population created
population = DNA_mismatch(population)
population = sorted(population,key=lambda x:x[1])
error_rate = []
generation = 1
Found = False
    
while not Found and generation <=200: #sometimes it get sketchy and doesn't end so i am not going to run this loop forever
    print("Children :> {} : Error {:2} in Generation : {:2}".format("".join(population[0][0]),population[0][1],generation))
    error_rate.append(population[0][1])
    if population[0][1] <= 0:
        Found = True
    ellitism = int(0.1*TOTAL_POP)
    new_generation = [population[i][0] for i in range(ellitism)] #only 10% of the fittest go to next generation
    offsprings = int((0.9*TOTAL_POP)) #90 new offsprings will be created by top 50 of the current generation.
    for _ in range(offsprings):
        p1,p2 = random.randint(0,50),random.randint(0,50)
        for i in range(2):
            child = CrossOverWithoutMutation(population[p1][0],population[p2][0])
            new_generation.append(child)
    population = new_generation
    population = DNA_mismatch(population) #calculate the dna mismatch in the generation obtained. 
    population = sorted(population,key=lambda x:x[1]) #sorting them from lowest error to highest.
    generation +=1

generation = [x for x in range(len(error_rate))]
plt.figure(figsize=(12,8))
plt.title("Cross Over without Mutation")
plt.ylabel("Error Rate")
plt.plot(generation,error_rate)
plt.yticks(np.arange(0,30,4))
plt.show()