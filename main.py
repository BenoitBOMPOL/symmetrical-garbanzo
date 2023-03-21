#!/usr/bin/env python3
"""
    Hello
"""
import matplotlib.pyplot as plt
import TaquInstance as taq

def minmin(instance : taq.TaquInstance, remaining_depth, alpha, beta, instances):
    """
        Minmin solver
    """
    best_move = None
    best_scor = instance.hybrid_score(alpha, beta)
    if remaining_depth > 0:
        best_scor = float("inf")
        for next_move in instance.get_next_moves():
            copy_grid = instance.duplicate()
            copy_grid.update(next_move)
            if hash(copy_grid) not in instances:
                _, bcs = minmin(copy_grid, remaining_depth - 1, alpha, beta, instances)
                if bcs < best_scor:
                    best_scor = bcs
                    best_move = next_move

    return (best_move, best_scor)

def solver(instance : taq.TaquInstance, depth, alpha, beta):
    """
        minmin_solver from instance
    """
    assert instance.can_be_solved()
    visited = [hash(instance)]
    scores = [instance.hybrid_score(alpha, beta)]

    while not instance.is_solved():
        assert instance.can_be_solved()
        current_score = instance.hybrid_score(alpha, beta)
        # print(f"\u001b[35mHashed Grid : \u001b[0m{hash(instance)}")
        # print(f"\u001b[35mCurrent Score : \u001b[0m{current_score}")
        # print(instance)
        scores.append(current_score)
        next_move, _ = minmin(instance, depth, alpha, beta, visited)
        if next_move is None:
            return []
        instance.update(next_move)
        visited.append(hash(instance))
    scores.append(instance.hybrid_score(alpha, beta))
    # print("\n " + (instance.char_len * instance.size + 3 * (instance.size - 1)) * "#")
    # print(instance)
    # print(" " + (instance.char_len * instance.size + 3 * (instance.size - 1)) * "#")
    # print(f"Solved in : {len(scores)} moves.")
    return scores

def get_valid_instance(size):
    """
        Create a solvable instance of [size]
    """
    is_solvable = False
    while not is_solvable:
        instance = taq.TaquInstance(size)
        is_solvable = instance.can_be_solved()
    return instance

def hist_from_data(data, depth, alpha, beta):
    """
        Draw histogram
    """
    data = [d for d in data if d > 0]
    plt.hist(data)
    plt.title(f"{depth=}, {alpha=}, {beta=}")
    plt.show()


def main():
    """
        minmin test
    """
    size = 3
    nb_solv = 10_000
    nb_moves = []
    for index in range(nb_solv):
        print(f"{index}-th iteration")
        instance = get_valid_instance(size)
        depth, alpha, beta = 4, 2, 3
        nb_moves.append(len(solver(instance, depth, alpha, beta)))
    hist_from_data(nb_moves, depth, alpha, beta)

if __name__ == "__main__":
    main()
