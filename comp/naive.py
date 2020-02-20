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

    sol1 = iterate(problem, ordered, 100, 0)
    sol2 = iterate(problem, sol1, 100, 50)

    libs = []
    for s_lib in sol2:
        libs.append(s_lib)
    s = Solution(libs)
    return s


def iterate(problem, ordered, chunk_size, offset):
    sol = []
    rem_days = problem.num_day
    used_books = set()
    for chunk in chunks(ordered, chunk_size, offset):
        optimized, rem_days, used_books = optimize(problem, rem_days, chunk, used_books)
        before = list(map(lambda it: it.lib_id, chunk))
        after = list(map(lambda it: it.lib_id, optimized))
        if after != before:
            print("yay")
        sol += optimized
    return sol


def optimize(problem, remaining_days, window_libs, used_books):
    slibs = []
    rem_days = remaining_days
    for _ in range(len(window_libs)):
        max_count = -1
        best = None
        for idx, slib in enumerate(window_libs):
            # count = score(problem, Solution(slibs+[slib]))
            count = lib_count(problem, slib, rem_days, used_books)
            if count > max_count:
                # ordered = sorted(filter(lambda it: it not in used_books, slib.book_ids),
                ordered = sorted(slib.book_ids,
                                 key=lambda it: -problem.scores[it])
                best = SolutionLibs(slib.lib_id, ordered)
                best_idx = idx
                max_count = count
        if best is not None:
            slibs.append(best)
            used_books.update(best.book_ids)
            rem_days -= problem.libs[best.lib_id].signup_days
            window_libs = window_libs[0:best_idx] + window_libs[best_idx + 1:]
    return slibs, rem_days, used_books


def lib_count(problem, slib, remaining_days, used_books):
    lib = problem.libs[slib.lib_id]
    lib_rem_days = remaining_days - lib.signup_days
    if lib_rem_days <= 0:
        return 0
    integ = integral(problem, lib, used_books)
    if len(integ) == 0:
        return 0
    # max points for this lib
    if lib_rem_days < len(integ):
        return integ[lib_rem_days]
    else:
        return integ[-1]


def integral(problem, lib, used_books):
    book_ids = list(filter(lambda it: it not in used_books, lib.book_ids))
    ordered = sorted(book_ids, key=lambda it: -problem.scores[it])

    chunked = list(chunks(ordered, lib.books_per_day, 0))
    integ = [0 for _ in range(len(chunked))]
    for day, chunk in enumerate(chunked):
        a = list(map(lambda it: problem.scores[it], chunk))
        x = sum(a)
        # print(chunk, a, x)
        if day == 0:
            integ[0] = x
            continue
        integ[day] = x + integ[day - 1]
    # print(lib, chunked, integ)

    return integ


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
