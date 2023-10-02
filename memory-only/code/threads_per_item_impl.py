import cProfile
import sys
import random
from threading import Thread
import glob


def random_matrix_strategy(lines, columns):
    return [[random.randint(0, 100) for _ in range(columns)] for _ in range(lines)]


def stable_random_matrix_strategy(lines, columns, seed):
    random.seed(seed)
    return [[random.randint(0, 100) for _ in range(columns)] for _ in range(lines)]


class MultiplyItemThread(Thread):
    __slots__ = ("result", "line", "columns")
    result: int

    def __init__(self, line, column):
        super().__init__()
        self.result = 0
        self.line = line
        self.column = column

    def run(self):
        self.result = sum(a * b for a, b in zip(self.line, self.column))


class Matrix:
    __slots__ = ("lines", "columns")

    def __init__(self, matrix):
        self.lines = matrix
        self.columns = tuple(zip(*matrix))

    @staticmethod
    def create(lines, columns, strategy):
        return Matrix(strategy(lines, columns))

    def __str__(self):
        s = [[str(e) for e in row] for row in self.lines]
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = "\t".join("{{:{}}}".format(x) for x in lens)
        table = [fmt.format(*row) for row in s]

        return "\n".join(table)

    def __mul__(self, other):
        threads = [
            [
                MultiplyItemThread(self.lines[line_idx], other.columns[column_idx])
                for column_idx in range(len(other.columns))
            ]
            for line_idx in range(len(self.lines))
        ]
        matrix = []

        for thread_list in threads:
            for thread in thread_list:
                thread.start()

        for thread_list in threads:
            for thread in thread_list:
                thread.join()

        for line_idx in range(len(self.lines)):
            matrix.append([])
            for column_idx in range(len(other.columns)):
                matrix[line_idx].append(threads[line_idx][column_idx].result)

        return Matrix(matrix)

    def __getitem__(self, index):
        return self.lines[index[0]][index[1]]


def main(lines_a, common_length, columns_b):
    mat_a = Matrix.create(
        lines_a,
        common_length,
        lambda lines, columns: stable_random_matrix_strategy(lines, columns, 102),
    )
    mat_b = Matrix.create(
        common_length,
        columns_b,
        lambda lines, columns: stable_random_matrix_strategy(lines, columns, 42),
    )

    _ = mat_a * mat_b


if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()

    main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))

    profiler.disable()
    counter = len(glob.glob("report/output.peritem-*.pstats"))
    profiler.dump_stats(
        "report/output.peritem-{}-{}-{}_{}.pstats".format(sys.argv[1], sys.argv[2], sys.argv[3], counter)
    )
