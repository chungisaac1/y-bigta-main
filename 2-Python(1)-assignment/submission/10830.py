import sys
from typing import Callable
import copy

class Matrix:
    MOD = 1000

    def __init__(self, matrix: list[list[int]]) -> None:
        self.matrix = matrix

    @staticmethod
    def full(n: int, shape: tuple[int, int]) -> 'Matrix':
        return Matrix([[n] * shape[1] for _ in range(shape[0])])

    @staticmethod
    def zeros(shape: tuple[int, int]) -> 'Matrix':
        return Matrix.full(0, shape)

    @staticmethod
    def ones(shape: tuple[int, int]) -> 'Matrix':
        return Matrix.full(1, shape)

    @staticmethod
    def eye(n: int) -> 'Matrix':
        matrix = Matrix.zeros((n, n))
        for i in range(n):
            matrix[i, i] = 1
        return matrix

    @property
    def shape(self) -> tuple[int, int]:
        return (len(self.matrix), len(self.matrix[0]))

    def clone(self) -> 'Matrix':
        return Matrix(copy.deepcopy(self.matrix))

    def __getitem__(self, key: tuple[int, int]) -> int:
        return self.matrix[key[0]][key[1]]

    def __setitem__(self, key: tuple[int, int], value: int) -> None:
        self.matrix[key[0]][key[1]] = value % self.MOD

    def __matmul__(self, matrix: 'Matrix') -> 'Matrix':
        x, m = self.shape
        m1, y = matrix.shape
        assert m == m1

        result = self.zeros((x, y))

        for i in range(x):
            for j in range(y):
                for k in range(m):
                    result[i, j] += self[i, k] * matrix[k, j]

        return result

    def __pow__(self, n: int) -> 'Matrix':
        result = Matrix.eye(len(self.matrix))
        base = self

        while n > 0:
            if n % 2 == 1:
                result = result @ base
            base = base @ base
            n //= 2
        
        return result

    def __repr__(self) -> str:
        return '\n'.join([' '.join(map(str, row)) for row in self.matrix])


def main() -> None:
    intify: Callable[[str], list[int]] = lambda l: [*map(int, l.split())]
    lines: list[str] = sys.stdin.readlines()

    N, B = intify(lines[0])
    matrix: list[list[int]] = [*map(intify, lines[1:])]

    Matrix.MOD = 1000
    modmat = Matrix(matrix)
    print(modmat ** B)

if __name__ == "__main__":
    main()