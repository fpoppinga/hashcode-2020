import os
import zipfile

from sample.io import Problem, score, Solution
from sample.naive import zipdir
from random import random


def iterate(problem, last_solution):
    pizzas = list(filter(lambda it: random() > 0.75, last_solution.types))
    current = sum(map(lambda it: problem.pizzas.types[it], pizzas))

    for id, type in list(enumerate(problem.pizzas.types)):
        if id in pizzas:
            continue
        if (current + type) <= problem.pizzas.max_pizza:
            current += type
            pizzas.append(id)
        else:
            continue

    return Solution(pizzas)


if __name__ == "__main__":

    file = "c_medium.in"
    solution1 = file.replace(".in", ".out")
    p = Problem("in/{}".format(file))
    s1 = Solution.from_file("out/{}".format(solution1))
    while True:
        s = iterate(p, s1)

        s1_score = score(p, s1)
        s_score = score(p, s)
        if s_score > s1_score:
            print("#" * 20, "besser")
            solution1 = s
            s.to_file("out/{}".format(file.replace(".in", ".out")))
            zipf = zipfile.ZipFile('../submit.zip', 'w', zipfile.ZIP_DEFLATED)
            zipdir('.', zipf)
            zipf.close()
        else:
            print("bring nix")
