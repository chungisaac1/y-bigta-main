import sys
from lib import Trie
from typing import List

def count(trie: Trie, query_seq: str) -> int:
    pointer = 0
    cnt = 1  # 첫 글자는 반드시 눌러야 하므로 1부터 시작

    for i, element in enumerate(query_seq):
        if i > 0 and (len(trie.nodes[pointer].children) > 1 or trie.nodes[pointer].is_end):
            cnt += 1
        pointer = trie.nodes[pointer].children[element]

    return cnt

def main() -> None:
    input = sys.stdin.read
    data = input().strip().split('\n')
    index = 0
    
    while index < len(data):
        N = int(data[index])
        index += 1
        words = data[index:index + N]
        index += N
        
        trie = Trie()
        for word in words:
            trie.push(word)
        
        total_presses = sum(count(trie, word) for word in words)
        average_presses = total_presses / N
        print(f"{average_presses:.2f}")

if __name__ == "__main__":
    main()
