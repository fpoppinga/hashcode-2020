import os
import zipfile
from datetime import datetime, timedelta

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
    remaining_days = problem.num_day
    ordered = []
    used_books = set()
    progress = Progress(problem.num_day)
    remaining_libs = set(range(len(problem.libs)))
    while remaining_days >= 0:
        best_next = None
        for id in remaining_libs:
            plib = problem.libs[id]
            added_books = plib.book_ids.difference(used_books)
            useless_books = plib.book_ids.difference(added_books)
            books_to_add = list(added_books) + list(useless_books)
            added_score = sum(map(lambda it: problem.scores[it], added_books)) / plib.signup_days
            if best_next is None or best_next[1] < added_score:
                best_next = (SolutionLibs(id, books_to_add), added_score)
        if best_next == None:
            print("break!")
            break
        else:
            best_lib = best_next[0]
            remaining_libs.remove(best_lib.lib_id)
            used_books.update(best_lib.book_ids)
            ordered.append(best_next)
            remaining_days -= problem.libs[best_lib.lib_id].signup_days
        progress.update(problem.num_day - remaining_days)

    libs = []
    for s_lib, lib_score in ordered:
        libs.append(s_lib)

    s = Solution(libs)
    return s


class Progress:
    def __init__(self, total, log_interval_ms=5000):
        self.total = total
        self.start = datetime.now()
        self.log_interval = timedelta(milliseconds=log_interval_ms)
        self.current = 0
        self.last = datetime.now()

    def update(self, current):
        now = datetime.now()
        if (now - self.last) > self.log_interval:
            remaining_time = (now - self.start) / current * (self.total - current)
            print("- {} done, {}s remaining".format(current / self.total, remaining_time.total_seconds()))
            self.last = now
        self.current = current


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
