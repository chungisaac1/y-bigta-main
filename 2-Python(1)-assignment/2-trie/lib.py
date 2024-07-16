from dataclasses import dataclass, field
from typing import TypeVar, Generic, Optional, Iterable, Dict

T = TypeVar("T") # 


@dataclass # 데이터를 저장하기 위한 클래스 init 생성 , 자동비교 메서드 
class TrieNode(Generic[T]): # 타입에 대한 힌트 > 어떤 기능이 있는건 아님 
    body: Optional[T] = None # body 변수가 t 타입의 값을 가질 수 도 있고 none 일 수 도 있다 일단은 none (기본 값)
    children: Dict[T, int] = field(default_factory=lambda: {}) 
    # chil > 키를 t로 받고 int 값을 가지는 딕셔너리 , fil > dataclass 모듈에서 제공되는 함수로 필드의 기본값, 초기화, 여부 설정간으 
    # default > field  함수의 인자로 사용되며 , 기본값 설정하는 defalt 에 지정된 함수는 객체가 생성될 때 호출되어 필드의 기본값 제공 
    is_end: bool = False


class Trie(Generic[T]):
    def __init__(self) -> None:
        self.nodes = [TrieNode(body=None)] # self.nodes 는 tirenode 객체들을 담고 있는 리스트 (포도알 보관하는)
        # body=none 은 trienode 객체의 body 속성을 none으로 초기화 

    def push(self, seq: Iterable[T]) -> None: # seq push 메서드에 전달되는 이터러블 객체 , 트라이에 추가하려는 시퀸스 
        # iterable > 제네릭 타입 t의 요소들을 담고 있는 반복가능한 객체 
        pointer = 0 # 현재 처리 중인 노드의 인덱스 가리키는거 
        for element in seq: # 자식 녿에 요소가 없으면 새로운 노드 추가 
            if element not in self.nodes[pointer].children: # 현재 가리키는 객체에 children 이 없다면 
                new_node = TrieNode(body=element)
                self.nodes[pointer].children[element] = len(self.nodes)
                self.nodes.append(new_node)
            pointer = self.nodes[pointer].children[element]
        self.nodes[pointer].is_end = True
# 주어진 시퀸스를 트라이 자료 구조에 추가하는 역할 