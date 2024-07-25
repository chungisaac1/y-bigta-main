from dataclasses import dataclass, field
from typing import TypeVar, Generic, Optional, Iterable, Dict, List

T = TypeVar("T")


@dataclass
class TrieNode(Generic[T]):
    body: Optional[T] = None
    children: Dict[T, int] = field(default_factory=lambda: {})
    is_end: bool = False


class Trie(Generic[T]):
    def __init__(self) -> None:
        self.nodes: List[TrieNode[T]] = [TrieNode(body=None)]

    def push(self, seq: Iterable[T]) -> None:
        pointer = 0
        for element in seq:
            if element not in self.nodes[pointer].children:
                new_node = TrieNode(body=element)
                self.nodes[pointer].children[element] = len(self.nodes)
                self.nodes.append(new_node)
            pointer = self.nodes[pointer].children[element]
        self.nodes[pointer].is_end = True


import sys

def count(trie: Trie[str], query_seq: str) -> int:
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
        
        trie: Trie[str] = Trie()
        for word in words:
            trie.push(word)
        
        total_presses = sum(count(trie, word) for word in words)
        average_presses = total_presses / N
        print(f"{average_presses:.2f}")

if __name__ == "__main__":
    main()
