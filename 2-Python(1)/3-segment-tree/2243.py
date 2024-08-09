from typing import List

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