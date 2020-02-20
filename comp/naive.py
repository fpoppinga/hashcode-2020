import os
import zipfile

from comp.io import Problem, score, SolutionLibs, Solution
from sample.naive import zipdir


def solve(problem):
    libs = []
    for id, lib in enumerate(problem.libs):
        sol_lib = SolutionLibs(id, lib.book_ids)
        libs.append(sol_lib)
    s = Solution(libs)
    return s

if __name__ == "__main__":
    for file in os.listdir("in"):
        print(file)
        p = Problem("in/{}".format(file))
        s = solve(p)
        s.to_file("out/{}".format(file))
        print(score(p, s))

    zipf = zipfile.ZipFile('../submit.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir('.', zipf)
    zipf.close()
