<<<<<<< HEAD
from typing import List

class SegmentTree:
    def __init__(self, N: int):
        self.size = N
        self.tree: List[int] = [0] * (4 * N)
        self.loc: List[int] = [-1] * (N + 1)

        def _init(start: int, end: int, idx: int):
            if start == end:
                if start < N:
                    self.tree[idx] = 0  # Initialize with 0 for the candy problem
                    self.loc[start] = start
                return
            mid = (start + end) // 2
            _init(start, mid, idx * 2)
            _init(mid + 1, end, idx * 2 + 1)
            self.tree[idx] = self.tree[idx * 2] + self.tree[idx * 2 + 1]

        _init(0, self.size - 1, 1)

    def update(self, target: int, val: int):
        def _update(start: int, end: int, idx: int, target: int, val: int):
            if end < target or start > target:
                return
            if start == end == target:
                self.tree[idx] += val
                return
            mid = (start + end) // 2
            _update(start, mid, idx * 2, target, val)
            _update(mid + 1, end, idx * 2 + 1, target, val)
            self.tree[idx] = self.tree[idx * 2] + self.tree[idx * 2 + 1]
            return

        target_idx = self.loc[target]
        _update(0, self.size - 1, 1, target_idx, val)

    def query(self, rank: int) -> int:
        def _query(start: int, end: int, idx: int, rank: int) -> int:
            if start == end:
                return start
            mid = (start + end) // 2
            if self.tree[idx * 2] >= rank:
                return _query(start, mid, idx * 2, rank)
            else:
                return _query(mid + 1, end, idx * 2 + 1, rank - self.tree[idx * 2])

        return _query(0, self.size - 1, 1, rank)


import sys

def main():
    input_data = sys.stdin.read().split()
    idx = 0
    n = int(input_data[idx])
    idx += 1

    max_taste = 1000000
    seg_tree = SegmentTree(max_taste + 1)
    results = []

    for _ in range(n):
        query_type = int(input_data[idx])
        if query_type == 1:
            rank = int(input_data[idx + 1])
            idx += 2
            taste = seg_tree.query(rank)
            results.append(taste)
            seg_tree.update(taste, -1)
        elif query_type == 2:
            taste = int(input_data[idx + 1])
            count = int(input_data[idx + 2])
            idx += 3
            seg_tree.update(taste, count)

    print("\n".join(map(str, results)))

if __name__ == "__main__":
    main()
=======
from typing import List

class SegmentTree:
    def __init__(self, N: int):
        self.size = N
        self.tree: List[int] = [0] * (4 * N)
        self.loc: List[int] = [-1] * (N + 1)

        def _init(start: int, end: int, idx: int):
            if start == end:
                if start < N:
                    self.tree[idx] = 0  # Initialize with 0 for the candy problem
                    self.loc[start] = start
                return
            mid = (start + end) // 2
            _init(start, mid, idx * 2)
            _init(mid + 1, end, idx * 2 + 1)
            self.tree[idx] = self.tree[idx * 2] + self.tree[idx * 2 + 1]

        _init(0, self.size - 1, 1)

    def update(self, target: int, val: int):
        def _update(start: int, end: int, idx: int, target: int, val: int):
            if end < target or start > target:
                return
            if start == end == target:
                self.tree[idx] += val
                return
            mid = (start + end) // 2
            _update(start, mid, idx * 2, target, val)
            _update(mid + 1, end, idx * 2 + 1, target, val)
            self.tree[idx] = self.tree[idx * 2] + self.tree[idx * 2 + 1]
            return

        target_idx = self.loc[target]
        _update(0, self.size - 1, 1, target_idx, val)

    def query(self, rank: int) -> int:
        def _query(start: int, end: int, idx: int, rank: int) -> int:
            if start == end:
                return start
            mid = (start + end) // 2
            if self.tree[idx * 2] >= rank:
                return _query(start, mid, idx * 2, rank)
            else:
                return _query(mid + 1, end, idx * 2 + 1, rank - self.tree[idx * 2])

        return _query(0, self.size - 1, 1, rank)


import sys

def main():
    input_data = sys.stdin.read().split()
    idx = 0
    n = int(input_data[idx])
    idx += 1

    max_taste = 1000000
    seg_tree = SegmentTree(max_taste + 1)
    results = []

    for _ in range(n):
        query_type = int(input_data[idx])
        if query_type == 1:
            rank = int(input_data[idx + 1])
            idx += 2
            taste = seg_tree.query(rank)
            results.append(taste)
            seg_tree.update(taste, -1)
        elif query_type == 2:
            taste = int(input_data[idx + 1])
            count = int(input_data[idx + 2])
            idx += 3
            seg_tree.update(taste, count)

    print("\n".join(map(str, results)))

if __name__ == "__main__":
    main()
>>>>>>> 8005f5f (4th)
