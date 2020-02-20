import os
import zipfile
from random import shuffle

from comp.io import Problem, score, SolutionLibs, Solution
from sample.naive import zipdir


def solve(problem):
    libs = []
    kack = list(enumerate(problem.libs))
    shuffle(kack)
    for id, lib in kack:
        sol_lib = SolutionLibs(id, lib.book_ids)
        libs.append(sol_lib)
    s = Solution(libs)
    return s


if __name__ == "__main__":
    max_score = -1
    while True:
        total_score = 0
        sols = []
        for file in os.listdir("in"):
            p = Problem("in/{}".format(file))
            s = solve(p)
            sols.append(s)
            total_score += score(p, s)
            if total_score > max_score:
                print("# {}".format(total_score))
                max_score = total_score
                s.to_file("out/{}".format(file))
                zipf = zipfile.ZipFile('../submit.zip', 'w', zipfile.ZIP_DEFLATED)
                zipdir('.', zipf)
                zipf.close()
