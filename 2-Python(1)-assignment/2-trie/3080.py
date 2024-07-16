import sys
from collections import deque
from lib import Trie
from typing import List

MOD = 1000000007

factorial_memo = {1: 1}
def factorial(n: int) -> int:
    if n in factorial_memo:
        return factorial_memo[n]
    else:
        factorial_memo[n] = (n * factorial(n - 1)) % MOD
        return factorial_memo[n]

def bfs(tree: Trie) -> int:
    que: deque[int] = deque([0])
    result: int = 1

    while que:
        cur = que.popleft()
        node = tree.nodes[cur]
        if len(node.children) == 0:
            continue

        if node.is_end:
            result = (result * factorial(len(node.children) + 1)) % MOD
        else:
            result = (result * factorial(len(node.children))) % MOD

        for child in node.children.values():
            que.append(child)

    return result

def diff(s1: str, s2: str) -> int:
    min_len = min(len(s1), len(s2))
    for i in range(min_len):
        if s1[i] != s2[i]:
            return i
    return min_len

def main() -> None:
    input = sys.stdin.read
    data = input().strip().split('\n')
    n = int(data[0].strip())
    args = [line.strip() for line in data[1:n + 1]]
    args.sort()

    tree = Trie()
    prev_lcp = 0
    for i in range(n - 1):
        cur_lcp = diff(args[i], args[i + 1])
        cutted = list(map(ord, args[i][:max(prev_lcp, cur_lcp) + 1]))
        tree.push(cutted)
        prev_lcp = cur_lcp
    tree.push(list(map(ord, args[-1])))

    answer = bfs(tree)
    print(answer % MOD)

if __name__ == "__main__":
    main()