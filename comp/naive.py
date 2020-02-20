import os
import zipfile

from comp.io import Problem, score, SolutionLibs, Solution
from sample.naive import zipdir


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def solve(problem):
    libs_with_score = []
    for id, lib in enumerate(problem.libs):
        s_lib = SolutionLibs(id, lib.book_ids)
        sol = Solution([s_lib])
        s = score(problem, sol)
        book_score = s / (0.10 * (lib.num_books / lib.books_per_day) + 0.90 * lib.signup_days)
        libs_with_score.append((s_lib, book_score))

    ordered = list(map(lambda it: it[0], sorted(libs_with_score, key=lambda it: -it[1])))

    sol = []
    rem_days = problem.num_day
    for chunk in chunks(ordered, 100):
        optimized, rem_days = optimize(problem, rem_days, chunk)
        before = list(map(lambda it: it.lib_id, chunk))
        after = list(map(lambda it: it.lib_id, optimized))
        if after != before:
            print("yay")
        sol += optimized

    libs = []
    for s_lib in sol:
        libs.append(s_lib)
    s = Solution(libs)
    return s


def optimize(problem, remaining_days, window_libs):
    slibs = []
    rem_days = remaining_days
    for _ in range(len(window_libs)):
        max_count = -1
        for idx, slib in enumerate(window_libs):
            count = lib_count(problem, slib, rem_days)
            if count > max_count:
                best = slib
                best_idx = idx
                max_count = count
        slibs.append(best)
        rem_days -= problem.libs[best.lib_id].signup_days
        window_libs = window_libs[0:best_idx] + window_libs[best_idx + 1:]
    return slibs, rem_days


def lib_count(problem, slib, remaining_days):
    lib = problem.libs[slib.lib_id]
    lib_rem_days = remaining_days - lib.signup_days
    if lib_rem_days < 0:
        return 0
    integ = integral(problem, lib)
    # max points for this lib
    if lib_rem_days < len(integ):
        return integ[lib_rem_days]
    else:
        return integ[-1]


def integral(problem, lib):
    ordered = sorted(lib.book_ids, key=lambda it: -problem.scores[it])
    integ = list(map(lambda it: problem.scores[it], ordered))
    for idx, book_id in enumerate(ordered[1:]):
        integ[idx + 1] += integ[idx]
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
