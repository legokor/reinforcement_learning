import retro
import numpy as np
#import Agent

from pathlib import Path
from time import sleep

import datetime

# IMPORTANT !!!
# Have to do: pip install https://github.com/chovanecm/python-genetic-algorithm/archive/master.zip#egg=mchgenalg
from mchgenalg import GeneticAlgorithm

env_name = 'MortalKombatII-Genesis'
state_name = 'AFK.SubZeroVsJax'
state_path = Path(f'../states/{state_name}.state').resolve()

env = retro.make(env_name,
    use_restricted_actions=retro.Actions.ALL,
    state=str(state_path),
    players=2)

class RandomAgent(object):
    def __init__(self, action_space):
        self.action_space = action_space
    
    #return a random move
    def act(self, observation, reward, done):
        lst = []
        for i in range(12):
            x = np.random.randint(2)
            lst.append(x)
        return np.asarray(lst)

class Daredevil(object):

    dna = []
    genome = []

    def __init__(self, action_space):
        self.action_space = action_space

    def dna2genome(self):
        self.genome = []
        for gene in self.dna:
            for letter in gene:
                if letter == 0:
                    self.genome.append(False)
                else:
                    self.genome.append(True)
    
    def genome2dna(self):
        self.dna = []
        cursor = 0
        while cursor < len(self.genome):
            s = ''
            for i in range(12):
                if self.genome[cursor] == False:
                    s = s + '0'
                else:
                    s = s + '1'
                cursor = cursor+1
            self.dna.append(s)



    def write_DNA_to_file(self,DNA_file):
        with open(DNA_file, 'w') as file:
            for gene in self.dna:
                file.write(gene + "\n")


    def set_DNA_from_file(self,DNA_file):
         with open(DNA_file) as file:
            rawdna = file.readlines()
            self.dna = [x.strip() for x in rawdna]
    
    #return a move
    def act(self, observation, reward, done, time):
        gene = self.dna[time%len(self.dna)]
        move = []
        for x in range(12):
            y = ord(gene[x])-ord('0')
            move.append(y)
        return np.asarray(move)

def run_simulation(agent1,agent2):
    state = env.reset()
    action1 = f'{0|2048:012b}'
    action2 = f'{0|2048:012b}'
    ob, reward, done, _ = env.step( action1 + action2 )
    while True:
        for i in range(100000):
            action1 = agent1.act(ob, reward, done,i)
            action2 = agent2.act(ob, reward, done,i)
            x = np.concatenate((action1,action2))
            #print(x)

            #ob: [224,300,3] array of pixels
            #done becomes true when someone collects 2 wins
            ob, reward, done, asd = env.step(x)
            env.render()
            #sleep(1/66)

            #if won/lost a fight, return with health difference
            if (asd['rounds_won'] + asd['enemy_rounds_won']) > 0:
                env.reset()
                return asd['health']-asd['enemy_health']

        

def fitness_function(genome):
    agent = Daredevil(env.action_space)
    agent.genome = genome
    agent.genome2dna()
    #enemy = RandomAgent(env.action_space)

    enemy = Daredevil(env.action_space)
    enemy.set_DNA_from_file("actualbest.txt")
    enemy.dna2genome()

    reward = run_simulation(agent,enemy)
    return reward

#dd = Daredevil(env.action_space)
#dd.set_DNA_from_file("dna0.txt")
#run_simulation(dd,RandomAgent(env.action_space))

########### GA ############

population_size = 5
#steps
dna_length = 100
genome_length = 12*dna_length
ga = GeneticAlgorithm(fitness_function)
ga.generate_binary_population(size=population_size, genome_length=genome_length)
# How many pairs of individuals should be picked to mate
ga.number_of_pairs = 3
# Selective pressure from interval [1.0, 2.0]
# the lower value, the less will the fitness play role
ga.selective_pressure = 1.5
ga.mutation_rate = 0.1
# If two parents have the same genotype, ignore them and generate TWO random parents
# This helps preventing premature convergence
ga.allow_random_parent = True # default True
# Use single point crossover instead of uniform crossover
ga.single_point_cross_over = False # default False
ga.run(10)

best_genome, best_fitness = ga.get_best_genome()

# Write last population to file 
now = datetime.datetime.now()
t = now.strftime('%Y%m%d_%H%M%S')
counter = 0
for gen in ga.population:
    d = Daredevil(env.action_space)
    d.genome = gen
    d.genome2dna()
    d.write_DNA_to_file(t + "-" + str(counter) + ".txt")
    counter = counter+1

pass