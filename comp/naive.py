import os
import zipfile

from comp.io import Problem, score, SolutionLibs, Solution
from sample.naive import zipdir


def chunks(lst, n, offset):
    if offset > len(lst):
        return lst
    if offset > 0:
        yield lst[0:offset]
    for i in range(0, len(lst), n):
        yield lst[offset + i:offset + i + n]


def solve(problem):
    libs_with_score = []
    for id, lib in enumerate(problem.libs):
        s_lib = SolutionLibs(id, lib.book_ids)
        sol = Solution([s_lib])
        s = score(problem, sol)
        book_score = s / (0.10 * (lib.num_books / lib.books_per_day) + 0.90 * lib.signup_days)
        libs_with_score.append((s_lib, book_score))

    ordered = list(map(lambda it: it[0], sorted(libs_with_score, key=lambda it: -it[1])))

    libs = []
    used_books = set()
    for s_lib in ordered:
        sol_books = sorted(list(set(s_lib.book_ids).difference(used_books)), key=lambda it: -problem.scores[it])
        foo = SolutionLibs(s_lib.lib_id, sol_books)
        used_books.update(foo.book_ids)
        libs.append(foo)
    
    s = Solution(libs)
    return s


if __name__ == "__main__":
    total_score = 0
    for file in os.listdir("in"):
        p = Problem("in/{}".format(file))
        s = solve(p)
        s.to_file("out/{}".format(file))
        cur_score = score(p, s)
        total_score += cur_score
        print(file, cur_score)
    print(total_score)

    zipf = zipfile.ZipFile('../submit.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir('.', zipf)
    zipf.close()
