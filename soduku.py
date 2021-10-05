import copy
from functools import partial
from pprint import PrettyPrinter
from random import choice
from random import randrange
from random import shuffle

import random
import time

"""
    Soduku Solver

    This Soduku Solver uses genetic algorithms to determine the values in the 9 3x3 grid sections.
    We first evaluate what values are missing in each section. Second, we create parents with different combination of grid choices.
    The offsprings are 1-grid mutated difference from parent. There is no crossover (maybe it will help?)...
    The parents and offsprings are combined as candidates, then the best M candidates are used as parents.
"""

random.seed(time.time())

unsolved_soduku = [
    [4,7,9,6,0,0,1,3,0],
    [5,0,8,0,1,9,7,6,0],
    [1,0,0,7,3,0,5,0,8],
    [0,0,3,5,6,0,4,0,7],
    [2,5,0,0,9,0,0,0,3],
    [0,0,0,0,4,2,9,1,5],
    [0,2,6,0,0,1,0,0,9],
    [0,0,0,0,0,6,0,0,0],
    [0,0,0,4,0,0,0,0,6]
]

def soduku_solution_gen(new_solution = None, missing_values =[]):
    count = 0
    if not new_solution:
        new_solution = copy.deepcopy(unsolved_soduku)
        for grid_i in range(3):
            for grid_j in range(3):
                gen_grid_solution(grid_i, grid_j, new_solution, missing_values[count])
                count += 1
        return new_solution
    temp = copy.deepcopy(new_solution)
    grid_i = randrange(3)
    grid_j = randrange(3)
    count += grid_i*3
    count += grid_j
    gen_grid_solution(grid_i, grid_j, temp, missing_values[count])
    return temp

def gen_grid_solution(grid_i, grid_j, solution, list_missing_values):
    remaining_values = list_missing_values.copy()
    shuffle(remaining_values)
    for i in range(3):
        for j in range(3):
            if not unsolved_soduku[grid_i*3 + i][ grid_j*3 + j]:
               solution[grid_i*3 + i][ grid_j*3 + j] = remaining_values.pop()

def find_missing_values_in_grids():
    # this will be a nested list of list
    values_missing_in_each_3by3_grid = []

    #check what each grids is missing in numbers
    for grid_i in range(3):
        for grid_j in range(3):
            found = []
            for i in range(3):
                for j in range(3):
                    if unsolved_soduku[grid_i*3 + i][ grid_j*3 + j] != 0:
                        found.append(unsolved_soduku[grid_i*3 + i][ grid_j*3 + j])
            values_missing_in_each_3by3_grid.append(list(filter(lambda v: v not in found, list(range(1, 10)))))
    return values_missing_in_each_3by3_grid


def soduku_ff(solution):
    total_duplicate_values_caught = 0
    #check rows
    for i in range(9):
        row = []
        for j in range(9):
            row.append(solution[i][j])
        # have we found duplicate in the rows
        if len(row) != len(set(row)):
            total_duplicate_values_caught += 1

    #check columns
    for i in range(9):
        col = []
        for j in range(9):
            col.append(solution[j][i])
        # have we found duplicate in the rows
        if len(col) != len(set(col)):
            total_duplicate_values_caught += 1

    #check grids
    for grid_i in range(3):
        for grid_j in range(3):
            grid = []
            for i in range(3):
                for j in range(3):
                    grid.append(solution[grid_i*3 + i][ grid_j*3 + j])
            if len(grid) != len(set(grid)):
                total_duplicate_values_caught += 1
    return total_duplicate_values_caught


def ev(generations, num_solutions, solution_gen, ff):
    """ Evolutionary Programming  Parents == Offspring Size """
    parents=[]
    # create initial parent solutions
    for _ in range(num_solutions):
        solution = solution_gen()
        parents.append({'S': solution, 'FF': ff(solution)})
    for _ in range(generations):
        # generate offsprings
        offsprings=[]
        for parent in parents:
            solution = solution_gen(new_solution=parent['S'])
            offsprings.append({'S': solution, 'FF': ff(solution)})
        candidates = parents + offsprings
        # get the best fit
        candidates = sorted(candidates, key=lambda candidate: candidate['FF'])
        parents = candidates[:num_solutions]

        #if we found solution, we don't need to waste any more generations searching
        if parents[0]['FF'] == 0:
            return parents
    # as close to the solution as we got
    return parents

def main():
    values = find_missing_values_in_grids()
    parents = ev(1000, 100, partial(soduku_solution_gen, missing_values=find_missing_values_in_grids()), soduku_ff)
    pp = PrettyPrinter(indent=4)
    pp.pprint(parents[0])

if __name__ == "__main__":
    main()
