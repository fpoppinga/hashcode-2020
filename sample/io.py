import numpy as np
import argparse


class Pizzas:
    def __init__(self, max_pizza, num_types, types):
        self.max_pizza = max_pizza
        self.num_types = num_types
        self.types = types
        assert num_types == len(types)

    def __str__(self):
        return "Pizza({}, {})".format(self.max_pizza, self.types)


class Solution:
    def __init__(self, types):
        self.types = types

    def __str__(self):
        return "{}\n{}".format(len(self.types), " ".join(map(str, self.types)))

    def to_file(self, path):
        with open(path, "w") as result_file:
            result_file.write("{}\n".format(self))

    @staticmethod
    def from_file(path):
        with open(path, "r") as result_file:
            num_types = int(result_file.readline())
            types = list(map(int, result_file.readline().split()))
            assert num_types == len(types)
            return Solution(types)


class Problem:
    def __init__(self, path):
        with open(path, "r") as f:
            preamble = f.readline().split()
            [max_pizza, num_types] = map(int, preamble)
            types = list(map(int, f.readline().split()))

            self.pizzas = Pizzas(max_pizza, num_types, types)
            print(self.pizzas)


def score(problem: Problem, solution: Solution):
    score = 0
    for type in solution.types:
        score += problem.pizzas.types[type]
    assert score <= problem.pizzas.max_pizza
    print("Score: {}".format(score))
    return score


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--problem", default="in/a_example.in")
    parser.add_argument("--solution", default="out/a_example.out")
    args = parser.parse_args()

    p = Problem(args.problem)
    s = Solution.from_file(args.solution)

    print(score(p, s))
