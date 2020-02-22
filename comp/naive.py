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


def add(map, key, value):
    if key in map:
        map[key] += value
    else:
        map[key] = value


def solve(problem):
    libs_with_score = []
    for id, lib in enumerate(problem.libs):
        s_lib = SolutionLibs(id, lib.book_ids)
        s = score(problem, Solution([s_lib]))
        book_score = s / lib.signup_days
        libs_with_score.append((s_lib, book_score))

    ordered = sorted(libs_with_score, key=lambda it: -it[1])
    ordered = improve(problem, ordered)

    libs = []
    for s_lib, lib_score in ordered:
        sol_books = sorted(s_lib.book_ids, key=lambda it: -problem.scores[it])
        sol_lib = SolutionLibs(s_lib.lib_id, sol_books)
        libs.append(sol_lib)

    s = Solution(libs)
    return s


def improve(problem, ordered):
    # filter by deadline
    remaining_days = problem.num_day
    used_books = {}
    reverse_ordered = []
    rest = []
    for slib, lib_score in ordered:
        lib = problem.libs[slib.lib_id]
        remaining_days -= lib.signup_days
        if remaining_days < 0:
            rest.append((slib, lib_score))
        else:
            reverse_ordered.insert(0, (slib, lib_score))
            for book_id in lib.book_ids:
                add(used_books, book_id, 1)

    # check which libs can be dropped
    reverse_filtered = []
    for slib, lib_score in reverse_ordered:
        sol_books = []
        for book in slib.book_ids:
            if used_books[book] == 1:
                # this book should be used!
                sol_books.append(book)
                del used_books[book]
            else:
                # this book is used by a better lib!
                assert used_books[book] > 1
                used_books[book] -= 1
        if len(sol_books) == 0:
            # lib has no useful books → filter!
            rest.append((slib, lib_score))
            continue
        new_slib = SolutionLibs(slib.lib_id, sol_books)
        s = score(problem, Solution([new_slib]))
        reverse_filtered.append((new_slib, s))

    return sorted(reverse_filtered, key=lambda it: -it[1]) + rest


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
