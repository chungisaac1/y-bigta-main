import sys
from collections import deque
from lib import Trie
from typing import List

MOD = 1000000007
# 트라이 구조를 넓이 우선 bfs 방식으로 탐색하면서 각 노드에서의 경우의 수를 계산하는 알고리즘 
# 각 노드에서 자식 노드의 개수를 기준으로 팩토리얼을 계산하고 그 결과를 누적하여 최종 결과 반환 
factorial_memo = {1: 1} # 메모제이션 > 반복되는 연산을 저장해 두고 , 동일한 연산이 필요할 때 저장된 값을 사용하는 
def factorial(n: int) -> int:
    if n in factorial_memo: # 1이면 바로 반환 
        return factorial_memo[n]
    else: #factorial_memo[n] 은 n의 팩토리얼 값을 의미 
        factorial_memo[n] = (n * factorial(n - 1)) % MOD
        # 재귀함수 > facotrial 실행 될려고 하면 > n-1 해서 실행이 되는 방식 
        # 이제 다시 올라 올 때 factorial 들고 간 숫자들이 리턴 될 때 n으로 되고 그래서 n*n이 되는 거임 그리고 그 n은 키 값도 되고 > value 값도 저장되는 
        return factorial_memo[n] # 한가지씩 값을 가지는 

def bfs(tree: Trie) -> int: # 넓이 우선 탐색 que를 이용해서 
    que: deque[int] = deque([0]) # deque[int] > 타입 힌트 이고 
    # deque([0])은 deque 자체가 클래스임 리스트처럼 동작하지만 양쪽 끝에서 빠른 삽입과 삭제 지원 
    # 큐 초기화: 초기값으로 0을 포함한 deque 객체 생성
    result: int = 1

# 트라이 자료 구조를 넓이 우선 탐색 방식으로 탐색하면서 특정 조건에 따라 결과를 계산 

    while que: # que 가 비어있지 않은 동안 반복 
        cur = que.popleft() # 큐의 왼쪽에서 하나의 요소 (현재 노드의 인덱스) 꺼내기
        node = tree.nodes[cur] # 꺼낸 인덱스를 사용하여 해당 노드를 가져옴 
        if len(node.children) == 0: # 리프 노드 처리 
            # 현재 노드가 리프 노드 라면 (자식 노드가 없는 경우라면) 다음 반복으로 넘어감 
            continue

        if node.is_end: # ㄱ결과 계산  > 단어의 끝이 true면 
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