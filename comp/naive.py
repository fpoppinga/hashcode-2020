import os
import zipfile

from comp.io import Problem, score, SolutionLibs, Solution
from sample.naive import zipdir


def solve(problem):
    libs = []
    ordered = sorted(list(enumerate(problem.libs)), key=lambda it: it[1].signup_days)
    for id, lib in ordered:
        sol_lib = SolutionLibs(id, lib.book_ids)
        libs.append(sol_lib)
    s = Solution(libs)
    return s


if __name__ == "__main__":
    total_score = 0
    for file in os.listdir("in"):
        print(file)
        p = Problem("in/{}".format(file))
        s = solve(p)
        s.to_file("out/{}".format(file))
        cur_score = score(p, s)
        total_score += cur_score
        print(cur_score)
    print(total_score)

    zipf = zipfile.ZipFile('../submit.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir('.', zipf)
    zipf.close()
