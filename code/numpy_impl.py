import cProfile
import sys
import numpy as np
import random
import glob


def random_matrix_strategy(lines, columns):
    return [[random.randint(0, 100) for _ in range(columns)] for _ in range(lines)]


def stable_random_matrix_strategy(lines, columns, seed):
    random.seed(seed)
    return [[random.randint(0, 100) for _ in range(columns)] for _ in range(lines)]


def main(lines_a, common_length, columns_b):
    mat_a = np.array(stable_random_matrix_strategy(lines_a, common_length, 102))
    mat_b = np.array(stable_random_matrix_strategy(common_length, columns_b, 42))

    _ = np.dot(mat_a, mat_b)


if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()

    main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))

    profiler.disable()
    counter = len(glob.glob("report/output.numpy-*.pstats"))
    profiler.dump_stats(
        "report/output.numpy-{}-{}-{}_{}.pstats".format(sys.argv[1], sys.argv[2], sys.argv[3], counter)
    )
