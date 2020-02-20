import numpy as np
import argparse


class Library:
    def __init__(self, num_books, signup_days, books_per_day, book_ids):
        self.num_books = num_books
        self.signup_days = signup_days
        self.books_per_day = books_per_day
        self.book_ids = list(set(book_ids))

    def __str__(self):
        return "Lib({}, {}, {}, {})".format(self.num_books, self.signup_days, self.books_per_day, self.book_ids)


class SolutionLibs:
    def __init__(self, lib_id, book_ids):
        self.lib_id = lib_id
        self.book_ids = book_ids

    def __str__(self):
        return "{} {}\n{}".format(self.lib_id, len(self.book_ids), " ".join(map(str,self.book_ids)))

class Solution:
    def __init__(self, libs):
        self.libs = libs

    def __str__(self):
        return "{}\n{}".format(len(self.libs), "\n".join(map(str, self.libs)))

    def to_file(self, path):
        with open(path, "w") as result_file:
            result_file.write("{}\n".format(self))

    @staticmethod
    def from_file(path):
        with open(path, "r") as result_file:
            num_libs = int(result_file.readline())
            libs = []
            for lib in range(num_libs):
                preamble = result_file.readline().split()
                [lib_id, num_books] = map(int, preamble)
                preamble = result_file.readline().split()
                book_ids = list(map(int, preamble))
                libs.append(SolutionLibs(lib_id, book_ids))
            return Solution(libs)


class Problem:
    def __init__(self, path):
        with open(path, "r") as f:
            preamble = f.readline().split()
            [num_books, num_libs, num_day] = map(int, preamble)
            self.num_books = num_books
            self.num_libs = num_libs
            self.num_day = num_day

            preamble = f.readline().split()
            self.scores = list(map(int, preamble))

            self.libs = []
            for lib in range(num_libs):
                preamble = f.readline().split()
                [num_books, signup_days, books_per_day] = map(int, preamble)
                preamble = f.readline().split()
                book_ids = list(map(int, preamble))
                self.libs.append(Library(num_books, signup_days, books_per_day, book_ids))

    def __str__(self):
        return "Problem({},{},{},{},{})".format(self.num_books, self.num_libs, self.num_day, self.scores, list(map(str,self.libs)))


def score(problem: Problem, solution: Solution):
    num_days = problem.num_day
    book_ids = set()
    for lib in solution.libs:
        prob_lib = problem.libs[lib.lib_id]
        num_days -= prob_lib.signup_days
        if num_days < 0:
            break
        book_ids.update(lib.book_ids[:(num_days*prob_lib.books_per_day)])
    score = 0
    for book in book_ids:
        score += problem.scores[book]
    return score

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--problem", default="in/a_example.txt")
    parser.add_argument("--solution", default="out/a_example.txt")
    args = parser.parse_args()

    p = Problem(args.problem)
    print(p)
    s = Solution.from_file(args.solution)
    print(s)

    print(score(p, s))
