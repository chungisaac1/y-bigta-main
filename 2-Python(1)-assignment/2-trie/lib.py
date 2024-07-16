from dataclasses import dataclass, field
from typing import TypeVar, Generic, Optional, Iterable, Dict

T = TypeVar("T")


@dataclass
class TrieNode(Generic[T]):
    body: Optional[T] = None
    children: Dict[T, int] = field(default_factory=lambda: {})
    is_end: bool = False


class Trie(Generic[T]):
    def __init__(self) -> None:
        self.nodes = [TrieNode(body=None)]

    def push(self, seq: Iterable[T]) -> None:
        pointer = 0
        for element in seq:
            if element not in self.nodes[pointer].children:
                new_node = TrieNode(body=element)
                self.nodes[pointer].children[element] = len(self.nodes)
                self.nodes.append(new_node)
            pointer = self.nodes[pointer].children[element]
        self.nodes[pointer].is_end = True
