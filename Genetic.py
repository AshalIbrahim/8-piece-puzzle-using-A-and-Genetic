import tkinter as tk
from tkinter import messagebox

from enum import Enum
from random import randint
import logging
import numpy as np
# Set up logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



goal = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])

class Direction(Enum):
    up = 1
    right = 2
    down = 3
    left = 4

    def isEqual(self, direction):
        return self == direction

    def isOpposite(self, direction):
        return abs(self.value - direction.value) == 2

    def getOpposite(self):
        return Direction(self.value - 2) if self.value > 2 else Direction(self.value + 2)

    def getDifferent(self):
        enums = list(Direction)
        enums.remove(self)
        return enums[randint(0, 2)]

    def getDifferentAxis(self):
        enums = list(Direction)
        enums.remove(self)
        enums.remove(self.getOpposite())
        return enums[randint(0, 1)]


class Puzzle:

    def __init__(self, board):
        self.puzzle = np.reshape(board, (3,3))

    def findZero(self):
        x=0
        y=0
        for i in range(3):
            for j in range(3):
                if self.puzzle[i][j] == 0:
                    x=i
                    y=j
                    break
        return x,y

    def move(self, direction):

        if not isinstance(direction, Direction):
            raise TypeError('direction must be an instance of Direction Enum')

        x, y = findZero(self.puzzle)
        if direction == Direction.up:
            if x == 0:
                raise IndexError("the x coordinate cannot be a negative value")
            self.__swap([x, y], [x-1, y])
        elif direction == Direction.right:
            if y == 2:
                raise IndexError("the y coordinate exceeds the range of the puzzle.")
            self.__swap([x, y], [x, y+1])
        elif direction == Direction.down:
            if x == 2:
                raise IndexError("the x coordinate exceeds the range of the puzzle.")
            self.__swap([x, y], [x+1, y])
        elif direction == Direction.left:
            if y == 0:
                raise IndexError("the y coordinate cannot be a negative value")
            self.__swap([x, y], [x, y-1])

    def __swap(self, coordinate1, coordinate2):
        tmp = self.puzzle[coordinate1[0], coordinate1[1]]
        self.puzzle[coordinate1[0], coordinate1[1]] = self.puzzle[coordinate2[0], coordinate2[1]]
        self.puzzle[coordinate2[0], coordinate2[1]] = tmp



    def fitness(self):
        mdis = 0
        for i in range(3):
            for j in range(3):
                if (goal[i, j] == 0):
                    continue
                x, y = np.where(self.puzzle == goal[i, j])
                mdis += abs(x[0]-i) + abs(y[0]-j)
        return mdis

    def fitness2(self):
        wrong_tiles = 0
        for i in range(3):
            for j in range(3):
                if(self.puzzle[i][j] != goal[i, j]):
                    wrong_tiles += 1
        return wrong_tiles


    def __str__(self):
        return str(self.puzzle)


class Solver:
    def __init__(self, MAX_GENERATION, POPULATION_SIZE, board):
        self.board = board
        self.MAX_GENERATION = MAX_GENERATION
        self.POPULATION_SIZE = POPULATION_SIZE
        self.CHROMOSOME_LENGTH = 11
        self.NUMBER_OF_SELECTED_CHROMOSOME = 5
        self.INCREMENT_RANGE_FOR_CHROMOSOME_LENGTH = 50
        self.INCREMENT_SIZE_FOR_CHROMOSOME_LENGTH = 5
        self.bestSelection = None
        self.bestGenerations = None

    def createChromosome(self, length=11):
        enums = list(Direction)
        chromosome = [enums[randint(0, 3)] for _ in range(length)]
        logging.info(f'Created chromosome: {self.getStrOfChromosome(chromosome)}')
        return chromosome

    def initializePopulation(self):
        population = [self.createChromosome(self.CHROMOSOME_LENGTH) for _ in range(self.POPULATION_SIZE)]
        return population

    def mutation(self, chromosome):
        length = len(chromosome)

        if length < 2:
            return chromosome

        if length < self.CHROMOSOME_LENGTH:
            chromosome += self.createChromosome(self.CHROMOSOME_LENGTH-length)

        if chromosome[0].isOpposite(chromosome[1]):
            chromosome[1] = chromosome[1].getDifferent()

        for i in range(2, self.CHROMOSOME_LENGTH):
            if chromosome[i].isEqual(chromosome[i-2]) and chromosome[i].isEqual(chromosome[i-1]):
                chromosome[i] = chromosome[i-1].getDifferentAxis()
            elif chromosome[i].isOpposite(chromosome[i-1]):
                chromosome[i] = chromosome[i-1].getDifferent()

        logging.info(f'Mutated chromosome: {self.getStrOfChromosome(chromosome)}')
        return chromosome

    def applyChromosomeToPuzzle(self, chromosome):
        puzzle = Puzzle(self.board)
        i = 0
        while i < len(chromosome):
            try:
                if puzzle.fitness2() == 0:
                    return [chromosome[:i], puzzle]
                puzzle.move(chromosome[i])
                i += 1
            except IndexError:
                chromosome[i] = chromosome[i].getDifferentAxis()
        return [chromosome, puzzle]

    def crossover(self, chromosomes, index=0):
        if self.NUMBER_OF_SELECTED_CHROMOSOME == index+1:
            return
        for i in range(index+1, self.NUMBER_OF_SELECTED_CHROMOSOME):
            chromosomes += self.crossing(chromosomes[index], chromosomes[i])
        self.crossover(chromosomes, index+1)

    def crossing(self, chromosome1, chromosome2):
        i = randint(0, self.CHROMOSOME_LENGTH//2-1)
        j = randint(self.CHROMOSOME_LENGTH//2, self.CHROMOSOME_LENGTH)

        c1 = chromosome1[:i] + chromosome2[i:]
        c2 = chromosome2[:i] + chromosome1[i:]

        c3 = chromosome1[:j] + chromosome2[j:]
        c4 = chromosome2[:j] + chromosome1[j:]

        c5 = chromosome1[:i] + chromosome2[i:j] + chromosome1[j:]
        c6 = chromosome2[:i] + chromosome1[i:j] + chromosome2[j:]

        c7 = chromosome1[j:] + chromosome1[:i] + chromosome2[i:j]
        c8 = chromosome2[j:] + chromosome2[:i] + chromosome1[i:j]

        c9 = chromosome2[i:j] + chromosome1[:i] + chromosome1[j:]
        c10 = chromosome1[i:j] + chromosome2[:i] + chromosome2[j:]

        return [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10]

    def selection(self, chromosomes):
        res = []
        for chromosome in chromosomes:
            tmp = self.applyChromosomeToPuzzle(chromosome)
            res.append([tmp[0], tmp[1]])
        res.sort(key=lambda x: x[1].fitness2())
        selected = res[:self.NUMBER_OF_SELECTED_CHROMOSOME]
        logging.info(f'Selected parents: {[self.getStrOfChromosome(ch[0]) for ch in selected]}')

        return selected

    def getStrOfChromosome(self, chromosome):
        return [x.name for x in chromosome]

    def solution(self):
        generation, numOfIncrement, bestmdis = 0, 0, 36
        bestSelection = []
        bestG = []

        population = self.initializePopulation()
        while generation < self.MAX_GENERATION:
            generation += 1

            for item in population:
                self.mutation(item)

            slct = self.selection(population)
            mdis = slct[0][1].fitness2()
            population = [item[0] for item in slct]

            if mdis < bestmdis:
                bestmdis = mdis
                bestSelection = slct[0]
                bestG.append((generation, mdis, self.getStrOfChromosome(slct[0][0])))

            if generation//self.INCREMENT_RANGE_FOR_CHROMOSOME_LENGTH > numOfIncrement:
                numOfIncrement += 1
                self.CHROMOSOME_LENGTH += self.INCREMENT_SIZE_FOR_CHROMOSOME_LENGTH

            yield f"generation: {generation} | fitness: {mdis}"

            if mdis == 0:
                self.bestSelection = bestSelection
                self.bestGenerations = bestG
                break

            self.crossover(population)

def findZero(parent):
    coordinates = [0, 0]
    for i in range(len(parent)):
        for j in range(len(parent[0])):
            if parent[i][j] == 0:
                coordinates = [i, j]
                break
    return coordinates
def swap(c0, cnum, parent):
    x1, y1 = c0
    x2, y2 = cnum
    parent_copy = [row[:] for row in parent]  # Create a deep copy of parent
    parent_copy[x1][y1], parent_copy[x2][y2] = parent_copy[x2][y2], parent_copy[x1][y1]
    return parent_copy

def Gen_child(parent, direction):
    child = []
    coordinates = findZero(parent)
    x, y = coordinates

    if direction=="right":  # Swapping right
        swapCoordinates = [x, y + 1]
        new_child = swap(coordinates, swapCoordinates, parent)

        return new_child

    elif direction=="left":  # Swapping left
        swapCoordinates = [x, y - 1]
        new_child = swap(coordinates, swapCoordinates, parent)

        return new_child

    elif direction=="down":  # Swapping down
        swapCoordinates = [x + 1, y]
        new_child = swap(coordinates, swapCoordinates, parent)

        return new_child

    else: # Swapping up
        swapCoordinates = [x - 1, y]
        new_child = swap(coordinates, swapCoordinates, parent)

        return new_child

def tostring1(initial):
    for row in initial:
        print(row)


def display_tiles(state):
    for i in range(3):
        for j in range(3):
            tiles[i][j].config(text=str(state[i][j]))

def tostringbestgeneration(list_of_tuples):
    result = ""
    for item in list_of_tuples:
        result += "\n"+f"({item[0]}, {item[1]}, {item[2]})\n"
    return result

def button_clicked(child1,bestGenerations):
    # Clear previous output


    # Run the A* algorithm


    # Display the chosen nodes and their heuristicsy

    for state in child1:
        display_tiles(state)

        root.update_idletasks()

        root.after(1000)  # Pause for 1 second to show the steps

    # Show final statistics in a dialog box
    messagebox.showinfo("Results", f"Best Generations found:\n {tostringbestgeneration(bestGenerations)}")

def main():

    solver = Solver(100, 5, [1, 8, 2, 7, 4, 3, 0, 6, 5])
    iterations = solver.solution()
    for iteration in iterations:
        print(iteration)
    bestSelection = solver.bestSelection
    bestGenerations = solver.bestGenerations
    print("---------------------------")
    print(goal)
    print("---------------------------")
    print(f"fitness: {bestSelection[1].fitness2()}")
    print(f"best chromosome\n{solver.getStrOfChromosome(bestSelection[0])}")
    print("length of best selection out of all: ", len(bestSelection[0]))
    string = solver.getStrOfChromosome(bestSelection[0])

    # Initialize an empty 2D array
    initial = []

    # Convert 1D array to 2D array of size 3x3 using a for loop
    for i in range(0, len(solver.board), 3):
        initial.append(solver.board[i:i + 3])

    child_list = []
    child1 = []
    child1.append(initial)

    for i in range(len(string)):
        child_list.append(Gen_child(child1[0], string[i]))
        tostring1(child1[0])
        print("")
        child1.pop()
        child1.append(child_list[i])

    button_clicked(child_list,bestGenerations)

if __name__ == "__main__":

    # Create the main window
    root = tk.Tk()
    root.title("Genetic Algorithm")

    # Create a frame to display the tiles
    frame = tk.Frame(root)
    frame.pack(pady=20)

    tiles = [[None for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            tiles[i][j] = tk.Label(frame, text="", font=("Helvetica", 24), width=4, height=2, borderwidth=2,
                                   relief="solid")
            tiles[i][j].grid(row=i, column=j)

    # Create a "Run" button
    run_button = tk.Button(root, text="Run", command=main, font=("Helvetica", 14))
    run_button.pack(pady=20)


    # Start the main event loop
    root.mainloop()
