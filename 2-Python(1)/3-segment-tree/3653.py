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

class MovieSegmentTree(SegmentTree):
    def __init__(self, N: int, M: int):
        super().__init__(N + M)
        self.size = N + M
        self.tree: List[int] = [0] * (4 * (N + M))
        self.loc: List[int] = [-1] * (N + 1)
        self.idx = N

        def _init(start: int, end: int, idx: int):
            if start == end:
                if start < N:
                    self.tree[idx] = 1
                    self.loc[N - start] = start
                return
            mid = (start + end) // 2
            _init(start, mid, idx * 2)
            _init(mid + 1, end, idx * 2 + 1)
            self.tree[idx] = self.tree[idx * 2] + self.tree[idx * 2 + 1]

        _init(0, self.size - 1, 1)

    def update(self, target: int, val: int = 1):
        def _update(start: int, end: int, idx: int, target: int, val: int):
            if end < target or start > target:
                return
            if start == end == target:
                self.tree[idx] = val
                return
            mid = (start + end) // 2
            _update(start, mid, idx * 2, target, val)
            _update(mid + 1, end, idx * 2 + 1, target, val)
            self.tree[idx] = self.tree[idx * 2] + self.tree[idx * 2 + 1]
            return

        target_idx = self.loc[target]
        _update(0, self.size - 1, 1, target_idx, 0)
        _update(0, self.size - 1, 1, self.idx, val)
        self.loc[target] = self.idx
        self.idx += 1

    def search(self, target: int) -> int:
        target_idx = self.loc[target]

        def _search(start: int, end: int, idx: int) -> int:
            if end < target_idx:
                return 0
            if target_idx <= start:
                return self.tree[idx]
            mid = (start + end) // 2
            return _search(start, mid, idx * 2) + _search(mid + 1, end, idx * 2 + 1)

        return _search(0, self.size - 1, 1) - 1

def main():
    input_data = sys.stdin.read().split()
    idx = 0
    T = int(input_data[idx])
    idx += 1

    results = []
    for _ in range(T):
        N, M = map(int, input_data[idx:idx + 2])
        idx += 2
        queries = list(map(int, input_data[idx:idx + M]))
        idx += M

        seg_tree = MovieSegmentTree(N, M)
        answer = []

        for dvd_num in queries:
            answer.append(seg_tree.search(dvd_num))
            seg_tree.update(dvd_num)

        results.append(' '.join(map(str, answer)))

    print('\n'.join(results))

if __name__ == "__main__":
    main()
