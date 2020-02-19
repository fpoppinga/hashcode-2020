import argparse

import numpy as np
from sample.io import Problem, Pizzas, Solution, score
import os
import zipfile

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))


def solve(problem):
    pizzas = []
    current = 0
    for id, type in reversed(list(enumerate(problem.pizzas.types))):
        if (current + type) <= problem.pizzas.max_pizza:
            current += type
            pizzas.append(id)
        else:
            continue

    return Solution(pizzas)


if __name__ == "__main__":

    for file in os.listdir("in"):
        p = Problem("in/{}".format(file))
        s = solve(p)
        s.to_file("out/{}".format(file.replace(".in", ".out")))
        score(p, s)

    zipf = zipfile.ZipFile('../submit.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir('.', zipf)
    zipf.close()

