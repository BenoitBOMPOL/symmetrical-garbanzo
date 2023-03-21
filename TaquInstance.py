#!/usr/bin/env python3
"""
    Better version
"""
from functools import reduce
from random import shuffle
from copy import deepcopy

class TaquInstance:
    """
        Instance of the taquin
    """
    def __init__(self, size):
        """
            Constructor
        """
        vals = list(range(1, size**2)) + [None]
        shuffle(vals)

        self.size = size
        self.char_len = len(str(size**2 - 1))
        self.grid = [[vals[i * size + j] for j in range(size)] for i in range(size)]

    def duplicate(self):
        """
            Duplication of the taquin
        """
        new = TaquInstance(self.size)
        new.char_len = self.char_len
        new.grid = deepcopy(self.grid)
        return new

    def flatten(self):
        """
            Returns the flatten version of the grid
        """
        return sum(self.grid, [])

    def count_inversions(self):
        """
            Count inversions
        """
        flat = self.flatten()
        flat.remove(None)
        count = 0
        for b in range(1, self.size**2):
            for a in range(b + 1, self.size**2):
                if flat.index(a) < flat.index(b):
                    count += 1
        return count

    def get_coord(self, index):
        """
            Get (i, j) from index
        """
        return (index // self.size, index % self.size)

    def can_be_solved(self):
        """
            Check whether can be solved
        """
        inversions = self.count_inversions()
        if self.size % 2 == 1:
            # ODD
            return inversions %2 == 0
        else:
            # EVEN
            flat = self.flatten()
            none_index = flat.index(None)
            n_i, _ = self.get_coord(none_index)
            diff = (self.size - 1) - n_i
            if ((diff % 2 == 0) and (inversions % 2 == 0)) or ((diff % 2 == 1) and (inversions % 2 == 1)):
                return True
        return False


    def __str__(self):
        buffer = " " + "-" * (self.char_len * self.size + 3 * (self.size - 1)) + "\n"
        for i in range(self.size):
            buffer_line = " "
            for j in range(self.size):
                if (self.size * i + j) + 1 == self.grid[i][j]:
                    buffer_line = buffer_line + "\u001b[32m"
                else:
                    buffer_line = buffer_line + "\u001b[31m"
                if self.grid[i][j] is None:
                    buffer_line = buffer_line + self.char_len * " "
                else:
                    buffer_line = buffer_line + str(self.grid[i][j]).zfill(self.char_len)
                buffer_line = buffer_line + "\u001b[0m"
                if j < self.size - 1:
                    buffer_line = buffer_line + " | "
            buffer = buffer + buffer_line
            buffer = buffer + "\n " + "-" * (self. char_len * self.size + 3 * (self.size - 1)) + "\n"
        return buffer

    def update(self, val):
        """
            Move the [val] tile
        """
        flat = self.flatten()
        i_1, j_1 = self.get_coord(flat.index(None))
        i_2, j_2 = self.get_coord(flat.index(val))
        self.grid[i_1][j_1], self.grid[i_2][j_2] = val, None

    def __hash__(self) -> int:
        return hash("".join([chr(65 + i) if i is not None else chr(65) for i in self.flatten()]))

    def get_next_moves(self):
        """
            Get next possible moves
        """
        i, j = self.get_coord(self.flatten().index(None))
        real_neighbours = [(new_i, new_j) for (new_i, new_j) in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)] if (new_i >= 0) and (new_i < self.size) and (new_j >= 0) and (new_j < self.size)]
        return [self.grid[ri][rj] for (ri, rj) in real_neighbours]

    def is_solved(self):
        """
            Check whether the instance is solved
        """
        flat = self.flatten()
        back = [u == v for (u, v) in zip(flat[:-1], list(range(1, self.size**2)))]
        return reduce(lambda x, y : x and y, back) and flat[-1] is None

    def manhattan_distance(self, value):
        """
            Computes the manhattan distance between the cell and where it should be
        """
        if value is None:
            return 0
        val_index = self.flatten().index(value)
        v_i, v_j = self.get_coord(val_index)
        r_i, r_j = self.get_coord(value - 1)
        return abs(v_i - r_i) + abs(v_j - r_j)

    def manhattan_score(self):
        """
            Computes a score with the Manhattan distance
        """
        return sum([self.manhattan_distance(value) for value in self.flatten()])

    def correct_place(self):
        """
            Correctly placed tiles
        """
        flat = self.flatten()
        score = 0
        for i, e in enumerate(flat[:-1]):
            if i + 1 == e:
                score += 1
        score += int(flat[-1] is None)
        return score

    def hybrid_score(self, man, cor):
        """
            Return a (possibly) hybrid score
        """
        return man * self.manhattan_score() - cor * self.correct_place()
