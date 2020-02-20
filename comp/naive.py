import os
import zipfile

from comp.io import Problem, score, SolutionLibs, Solution
from sample.naive import zipdir


def solve(problem):
    libs_with_score = []
    for id, lib in enumerate(problem.libs):
        s_lib = SolutionLibs(id, lib.book_ids)
        sol = Solution([s_lib])
        s = score(problem, sol)
        book_score = s / (0.10 * (lib.num_books / lib.books_per_day) + 0.90 * lib.signup_days)
        libs_with_score.append((s_lib, book_score))

    ordered = sorted(libs_with_score, key=lambda it: -it[1])

    libs_with_score = []
    used_books = set()
    for slib, s in ordered:
        lib = problem.libs[slib.lib_id]
        remaining_books = set(slib.book_ids).difference(used_books)
        slib_ = SolutionLibs(slib.lib_id, list(remaining_books))
        used_books.update(remaining_books)
        sol = Solution([slib_])
        s = score(problem, sol)
        book_score = s / (0.10 * (lib.num_books / lib.books_per_day) + 0.90 * lib.signup_days)
        libs_with_score.append((slib_, book_score))

    ordered = sorted(libs_with_score, key=lambda it: -it[1])

    libs = []
    for s_lib, s in ordered:
        libs.append(s_lib)
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
