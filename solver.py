from collections import defaultdict
import pyautogui


class Solver:
    def __init__(self, grid, words):
        self.grid = grid
        self.words = words
        self.solution = defaultdict(list)

    def preprocess_indices(self, matrix):
        indices_dict = defaultdict(list)
        for row_index, row in enumerate(matrix):
            for col_index, element in enumerate(row):
                indices_dict[element].append((row_index, col_index))
        return indices_dict

    def find_element_indices(self, indices_dict, target):
        return indices_dict.get(target, [])

    def solve(self):
        indices_dict = self.preprocess_indices(self.grid)
        for word in self.words:
            self.solve_word(word, indices_dict)
        return self.solution

    def solve_word(self, word, indices_dict):
        first = word[0]
        indices = self.find_element_indices(indices_dict, first)
        for index in indices:
            x = index[0]
            y = index[1]
            neighbors, neighbor_indices, directions = self.neighbors(x, y)
            self.solution[word].append((x, y))
            if word[1] not in neighbors:
                self.solution[word] = []
                continue
            match_directions = []
            for i, neighbor in enumerate(neighbors):
                if neighbor == word[1]:
                    match_directions.append(directions[i])
            for direction in match_directions:
                for i in range(1, len(word)):
                    #start_x, start_y = 670 + 35/2 + x*35, 207 + 35/2 + y*35
                    #pyautogui.moveTo(start_x, start_y)
                    x += direction[0]
                    y += direction[1]
                    if x >= len(self.grid) or x < 0 or y >= len(self.grid[x]) or y < 0:
                        break
                    if self.grid[x][y] != word[i]:
                        break
                    self.solution[word].append((x, y))
                else:
                    print(f"Solved {word}")
                    return
                x, y = index
                self.solution[word] = []
                self.solution[word].append((x, y))
            else:
                self.solution[word] = []

    def neighbors(self, x, y):
        neighbors = []
        indices = []
        directions = []
        # left
        if y - 1 >= 0:
            neighbors.append(self.grid[x][y-1])
            indices.append((x, y-1))
            directions.append((0, -1))
        # bottom-left
        if x + 1 < len(self.grid[x]) and y - 1 >= 0:
            neighbors.append(self.grid[x+1][y-1])
            indices.append((x+1, y-1))
            directions.append((1, -1))
        # bottom
        if x + 1 < len(self.grid[x]):
            neighbors.append(self.grid[x+1][y])
            indices.append((x+1, y))
            directions.append((1, 0))
        # bottom-right
        if x + 1 < len(self.grid[x]) and y + 1 < len(self.grid):
            neighbors.append(self.grid[x+1][y+1])
            indices.append((x+1, y+1))
            directions.append((1, 1))
        # right
        if y + 1 < len(self.grid):
            neighbors.append(self.grid[x][y+1])
            indices.append((x, y+1))
            directions.append((0, 1))
        # top-right
        if x - 1 >= 0 and y + 1 < len(self.grid):
            neighbors.append(self.grid[x-1][y+1])
            indices.append((x-1, y+1))
            directions.append((-1, 1))
        # top
        if x - 1 >= 0:
            neighbors.append(self.grid[x-1][y])
            indices.append((x-1, y))
            directions.append((-1, 0))
        # top-left
        if x - 1 >= 0 and y - 1 >= 0:
            neighbors.append(self.grid[x-1][y-1])
            indices.append((x-1, y-1))
            directions.append((-1, -1))
        return neighbors, indices, directions
