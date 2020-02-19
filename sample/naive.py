import argparse

import numpy as np
from sample.io import Problem, Pizzas, Solution, score


def solve(problem):
    pizzas = []
    current = 0
    for id, type in reversed(list(enumerate(problem.pizzas.types))):
        print("{}: {}".format(id, type))
        if (current + type) <= problem.pizzas.max_pizza:
            current += type
            pizzas.append(id)
        else:
            break

    return Solution(pizzas)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--problem", default="in/a_example.in")
    parser.add_argument("--solution", default="out/a_example.out")
    args = parser.parse_args()

    p = Problem(args.problem)
    s = solve(p)
    s.to_file(args.solution)
    score(p, s)
