import heapq
import tkinter as tk
from tkinter import messagebox

def get_heuristic1(goal, initial):
    counter = 0
    for i in range(len(initial)):
        for j in range(len(initial[0])):
            if initial[i][j] != goal[i][j]:
                counter += 1
    return counter

def find(num, initial):
    temp = [0, 0]
    for i in range(len(initial)):
        for j in range(len(initial[0])):
            if num == initial[i][j]:
                temp[0] = i
                temp[1] = j
    return temp

def get_heuristic2(goal, initial):
    counter = 0
    for i in range(len(initial)):
        for j in range(len(initial[0])):
            if goal[i][j] != initial[i][j]:
                location = find(goal[i][j], initial)
                manhattan = abs(i - location[0]) + abs(j - location[1])
                counter += manhattan
    return counter

def tostring(initial):
    for row in initial:
        print(row)

def additon_costPath_Heuristic(heuristic, pathCost):
    return heuristic + pathCost

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

def GenAstar_child(parent, goal, level):
    child = []
    coordinates = findZero(parent)
    x, y = coordinates

    if y >= 0 and y < 2 and x >= 0 and x <= 2:  # Swapping right
        swapCoordinates = [x, y + 1]
        new_child = swap(coordinates, swapCoordinates, parent)
        heuristic = get_heuristic2(goal, new_child)
        tup = (new_child, heuristic, additon_costPath_Heuristic(heuristic, level))
        child.append(tup)

    if y <= 2 and y > 0 and x >= 0 and x <= 2:  # Swapping left
        swapCoordinates = [x, y - 1]
        new_child = swap(coordinates, swapCoordinates, parent)
        heuristic = get_heuristic2(goal, new_child)
        tup = (new_child, heuristic, additon_costPath_Heuristic(heuristic, level))
        child.append(tup)

    if x >= 0 and x < 2 and y >= 0 and y <= 2:  # Swapping down
        swapCoordinates = [x + 1, y]
        new_child = swap(coordinates, swapCoordinates, parent)
        heuristic = get_heuristic2(goal, new_child)
        tup = (new_child, heuristic, additon_costPath_Heuristic(heuristic, level))
        child.append(tup)

    if x <= 2 and x > 0 and y >= 0 and y <= 2:  # Swapping up
        swapCoordinates = [x - 1, y]
        new_child = swap(coordinates, swapCoordinates, parent)
        heuristic = get_heuristic2(goal, new_child)
        tup = (new_child, heuristic, additon_costPath_Heuristic(heuristic, level))
        child.append(tup)

    return child

def tostring1(initial):
    for row in initial:
        print(row)

def Astar_algo(initial, goal):
    level = 0
    current = (initial, get_heuristic2(goal, initial), additon_costPath_Heuristic(get_heuristic2(goal, initial), level))
    nodes_explored = 0
    path = []
    explored_states = set()
    priority_queue = []
    path_final=[]
    path_final.append(initial)

    parent_map={}


    heapq.heappush(priority_queue, (current[2], current))

    while priority_queue:
        _, current = heapq.heappop(priority_queue)

        if current[1] == 0:
            print("Goal State Found: ")
            tostring(current[0])
            print("Total cost (N):", current[2])

            break

        if tuple(tuple(row) for row in current[0]) in explored_states:
            continue

        explored_states.add(tuple(tuple(row) for row in current[0]))
        #path.append(current)
        path_final.append(current)
        nodes_explored += 1

        print("Level:", level)
        print("Current state: ")
        tostring(current[0])

        print("Heuristic:", current[1])
        print("Total cost (N):", current[2])

        level += 1
        children = GenAstar_child(current[0], goal, level)

        for child in children:
            state_tuple = tuple(tuple(row) for row in child[0])


            if state_tuple not in explored_states:
                heapq.heappush(priority_queue, (child[2], child))
                parent_map[state_tuple] = current # Store the parent of the child state

    fpath=[]
    while current[0] != initial:
        fpath.append(current[0])
        current_state_tuple = tuple(tuple(row) for row in current[0])
        current = parent_map[current_state_tuple]

    fpath.append(initial)
    fpath.reverse() # Reverse the path to start from initial node
    print("Final Path")
    for states in fpath:
        print(tostring1(states))
        print("")


    print("Total nodes explored:", nodes_explored)
    print("Levels explored:", len(path)-1)
    return path_final,nodes_explored,level,fpath

def isValid(path_list, state):
    state_tuple = tuple(tuple(row) for row in state[0])
    for path_state in path_list:
        path_state_tuple = tuple(tuple(row) for row in path_state[0])
        if path_state_tuple == state_tuple:
            return False
    return True

def display_tiles(state):
    for i in range(3):
        for j in range(3):
            tiles[i][j].config(text=str(state[i][j]))

def button_clicked():
    # Clear previous output
    output_text.delete(1.0, tk.END)

    # Run the A* algorithm
    path, nodes_explored, level,fpath = Astar_algo(initial, goal)

    # Display the chosen nodes and their heuristicsy
    levels=0
    for state in fpath:
        display_tiles(state)
        output_text.delete(1.0, tk.END)  # Clear the previous heuristic
        output_text.insert(tk.END, f"Heuristic: {get_heuristic2(goal,state)}\n"+f"Level: {levels}\n"+f"Cost: {get_heuristic2(goal,state)+levels}")
        root.update_idletasks()
        levels+=1
        root.after(1000)  # Pause for 1 second to show the steps

    # Show final statistics in a dialog box
    messagebox.showinfo("Results", f"Total nodes explored: {len(path)}\nLevels explored: {len(fpath)-1}")

def main():
    global initial,goal
    initial = [[0] * 3 for _ in range(3)]
    goal = [[0] * 3 for _ in range(3)]

    k = 0

    with open("input.txt", "r") as f:
        for line in f:
            arrayCount = 0
            if k == 0:
                print("Assigning initial values")
                numbers = [int(num) for num in line.split()]
                for i in range(3):
                    for j in range(3):
                        initial[i][j] = numbers[arrayCount]
                        arrayCount += 1
                        print(initial[i][j], end=" ")
                    print("")
            else:
                print("Assigning goal values")
                numbers = [int(num) for num in line.split()]
                for i in range(3):
                    for j in range(3):
                        goal[i][j] = numbers[arrayCount]
                        arrayCount += 1
                        print(goal[i][j], end=" ")
                    print("")
            k += 1

    button_clicked()


if __name__ == "__main__":

    # Create the main window
    root = tk.Tk()
    root.title("A* Algorithm")

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

    # Create a Text widget to display the heuristic
    output_text = tk.Text(root, width=20, height=4, font=("Helvetica", 12))
    output_text.pack(pady=20)

    # Start the main event loop
    root.mainloop()