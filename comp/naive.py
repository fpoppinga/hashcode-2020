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
    book_sort = lambda it: -problem.scores[it]
    # init: all days are remaining, now libs selected, no books used, all libs remaining
    remaining_days = problem.num_day
    ordered = []
    used_books = set()
    remaining_libs = set(range(len(problem.libs)))
    # init progress logger
    progress = Progress(problem.num_day)
    while remaining_days >= 0:
        # as long as we have time left, find the next best lib
        best_next = None
        best_score = -1
        # from all remaining libraries
        for id in remaining_libs:
            plib = problem.libs[id]
            # find books this library offers and are not uses yet
            added_books = sorted(plib.book_ids.difference(used_books), key=book_sort)[
                          :(remaining_days - plib.signup_days) * plib.books_per_day]
            # calculate the 'best'-heuristic:
            # score this library adds relative to it's setup time
            added_score = sum(map(lambda it: problem.scores[it], added_books)) / plib.signup_days
            if best_score < added_score:
                # if we pick this library, take books with higher score first
                best_next = SolutionLibs(id, added_books)
                best_score = added_score
        # if we have picked all libraries, we can stop the search
        if best_next == None:
            break
        else:
            remaining_libs.remove(best_next.lib_id)
            used_books.update(best_next.book_ids)
            ordered.append(best_next)
            remaining_days -= problem.libs[best_next.lib_id].signup_days
        progress.update(problem.num_day - remaining_days)

    s = Solution(ordered)
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
